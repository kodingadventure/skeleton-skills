#!/usr/bin/env python3
"""Review page helper.

  page.py new <topic> [--lang LANG] [--main FILE] [--title TEXT]
        write <tmpdir>/review-page/<topic>-<YYYYMMDD-HHMM>.html from the template, its fixed strings
        in LANG (default en); with --main, FILE's <main>...</main> replaces the template's example. Prints the path.
  page.py check <file>
        report rule violations; exit 1 when any ERROR is found
  page.py decide <file> <radio-name>=<letter> ...   (or <radio-name>=other:<the user's own answer>,
        or <radio-name>=follow-up when the item continues in the follow-up section)
        record answers: set data-chosen on each named decision
  page.py refresh <file> [--lang LANG]
        rebuild a page on the current template, keeping its <title> and <main>

Fixed strings live in strings/<lang>.json; add a language by copying en.json and translating it.
"""
import argparse
import html
import json
import re
import sys
import tempfile
import time
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "template.html"
STRINGS = ROOT / "strings"
MAX_ITEMS = 7
MAX_LR_NODES = 4
MAX_FANOUT = 3
MAX_LABEL_LINE = 25
# The start of a label Mermaid's Markdown renderer draws as "Unsupported markdown: <type>" instead of
# the text: a list item, heading, or quote ("1. Go", "2) Go", "- Go", "# Go", "> Go"), or a rule ("---").
# Only the label's start counts: Mermaid reads a line after <br/> as part of the same paragraph.
MD_UNSUPPORTED_START = re.compile(r"(\d+[.)]|[-*+]|#{1,6}|>)\s|(-{3,}|\*{3,}|_{3,})$")


def render(lang, main=None, title=None):
    """The template with `main` and `title` swapped in, then every [[key]] filled from strings/<lang>.json."""
    path = STRINGS / f"{lang}.json"
    if not path.exists():
        sys.exit(f"No strings for '{lang}'. Add {path} by copying en.json and translating it.")
    strings = json.loads(path.read_text(encoding="utf-8"))
    out = TEMPLATE.read_text(encoding="utf-8")
    if main:
        out = re.sub(r"<main>.*</main>", lambda _: main, out, count=1, flags=re.S)
    if title:
        out = re.sub(r"<title>.*?</title>", lambda _: title, out, count=1, flags=re.S)
    out = out.replace("[[js_strings]]", json.dumps(strings["js"], ensure_ascii=False))

    def fill(m):
        key = m.group(1)
        if key not in strings:
            sys.exit(f"{path.name} lacks the key '{key}'.")
        return html.escape(strings[key], quote=True)

    return re.sub(r"\[\[([a-z_]+)\]\]", fill, out)


def main_block(text, source):
    m = re.search(r"<main>.*</main>", text, re.S)
    if not m:
        sys.exit(f"{source} has no <main>...</main> block.")
    return m.group(0)


def cmd_new(args):
    body = main_block(Path(args.main).read_text(encoding="utf-8"), args.main) if args.main else None
    title = f"<title>{html.escape(args.title)}</title>" if args.title else None
    out = render(args.lang, body, title)
    topic = re.sub(r"[^a-z0-9]+", "-", args.topic.lower()).strip("-") or "review"
    folder = Path(tempfile.gettempdir()) / "review-page"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{topic}-{time.strftime('%Y%m%d-%H%M')}.html"
    if path.exists():
        path = folder / f"{topic}-{time.strftime('%Y%m%d-%H%M%S')}.html"
    path.write_text(out, encoding="utf-8")
    print(path)


def cmd_decide(args):
    path = Path(args.file)
    page = path.read_text(encoding="utf-8")
    for pair in args.answers:
        name, _, letter = pair.partition("=")
        if not letter:
            sys.exit(f"'{pair}' is not <radio-name>=<letter>.")
        found = False
        for m in re.finditer(r'<div class="opts"[^>]*>', page):
            radio = re.search(r'<input[^>]*\bname="([^"]+)"', page[m.end():])
            if not radio or radio.group(1) != name:
                continue
            tag = re.sub(r'\s+data-(chosen|other)="[^"]*"', "", m.group(0))
            letter, _, other = letter.partition(":")
            if letter == "other" and not other.strip():
                sys.exit(f"'{pair}' has no answer text; write <radio-name>=other:<the user's own answer>.")
            extra = f' data-other="{html.escape(other.strip())}"' if letter == "other" else ""
            tag = tag[:-1] + f' data-chosen="{html.escape(letter)}"{extra}>'
            page = page[: m.start()] + tag + page[m.end():]
            found = True
            break
        if not found:
            sys.exit(f"No decision uses the radio name '{name}'.")
    path.write_text(page, encoding="utf-8")
    print(path)


def cmd_refresh(args):
    path = Path(args.file)
    page = path.read_text(encoding="utf-8")
    lang = args.lang or (re.search(r'<html[^>]*\blang="([^"]+)"', page) or [None, None])[1]
    if not lang:
        sys.exit("The page has no <html lang>; pass --lang.")
    title = re.search(r"<title>.*?</title>", page, re.S)
    main = re.search(r"<main>.*</main>", page, re.S)
    if not (title and main):
        sys.exit("The page needs a <title> and a <main> to refresh.")
    body = re.sub(r"<header(?:\s+id=\"[^\"]*\")?>", '<header id="top">', main.group(0), count=1)
    out = render(lang, body, title.group(0))
    path.write_text(out, encoding="utf-8")
    print(path)


class Structure(HTMLParser):
    """Collects the parts of a page the rules look at."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.nav_links = []
        self.sections = []
        self.groups = []
        self.mermaid = []
        self.has_decided = False
        self.has_answer = False
        self._stack = []
        self._group = None
        self._group_depth = 0
        self._mermaid = None
        self.raw_br_in_mermaid = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if a.get("id"):
            self.ids.add(a["id"])
        if "decided" in cls:
            self.has_decided = True
        if "answer" in cls:
            self.has_answer = True
        if tag == "a" and "nav" in self._stack and (a.get("href") or "").startswith("#"):
            self.nav_links.append(a["href"][1:])
        if tag == "section" and self._stack[-1:] == ["main"]:
            self.sections.append({"id": a.get("id"), "ask": "data-ask" in a, "groups": 0, "chip": False, "risk": False})
        sec = self.sections[-1] if self.sections and "section" in self._stack + [tag] else None
        if sec and "chip" in cls:
            sec["chip"] = True
        if sec and "risk" in cls:
            sec["risk"] = True
        if tag == "div" and "opts" in cls:
            self._group = {
                "name": a.get("data-name"),
                "chosen": a.get("data-chosen"),
                "other": a.get("data-other"),
                "num": a.get("data-num"),
                "follow": bool(sec and sec["id"] == "follow-up"),
                "options": [],
            }
            self._group_depth = 0
            self.groups.append(self._group)
            if sec:
                sec["groups"] += 1
        elif tag == "div" and self._group is not None:
            self._group_depth += 1
        if tag == "label" and self._group is not None:
            self._group["options"].append({"rec": "rec" in cls})
        if tag == "input" and self._group is not None and self._group["options"]:
            self._group["options"][-1].update(name=a.get("name"), value=a.get("value"), checked="checked" in a)
        if tag == "br" and self._mermaid is not None:
            self.raw_br_in_mermaid += 1
        if tag == "pre" and "mermaid" in cls:
            self._mermaid = []
        if tag not in ("input", "br", "meta", "link", "img"):
            self._stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "div" and self._group is not None:
            if self._group_depth == 0:
                self._group = None
            else:
                self._group_depth -= 1
        if tag == "pre" and self._mermaid is not None:
            self.mermaid.append("".join(self._mermaid))
            self._mermaid = None
        if tag in self._stack:
            while self._stack and self._stack.pop() != tag:
                pass

    def handle_data(self, data):
        if self._mermaid is not None:
            self._mermaid.append(data)


ARROW = re.compile(r"\s*(?:<?-+\.?-*>|<?=+>|-{3,}|-\.-)\s*")


def check_label(n, label, err, warn):
    plain = label.strip('"').strip()
    if MD_UNSUPPORTED_START.match(plain) or "`" in plain:
        err(f"diagram {n}: label {label!r} holds Markdown that Mermaid renders as 'Unsupported markdown'. "
            "Start it with plain words, write 'Step 1' or '1:' instead of '1. ', and leave out backticks")
    for part in re.split(r"<br\s*/?>", label):
        if len(part) > MAX_LABEL_LINE:
            warn(f"diagram {n}: label line over {MAX_LABEL_LINE} characters, break it: {part!r}")


def check_mermaid(n, text, err, warn):
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    if not lines:
        return
    head = lines[0].split()
    if head[0] not in ("flowchart", "graph"):
        return
    direction = head[1] if len(head) > 1 else "TD"
    nodes, fanout, subgraphs = set(), {}, 0
    for line in lines[1:]:
        if line.startswith("subgraph"):
            subgraphs += 1
            continue
        if re.match(r"(classDef|class|style|linkStyle|end\b|%%|click)", line):
            continue
        for label in re.findall(r"\[(.*?)\]|\((.*?)\)|\{(.*?)\}", line):
            # findall gives "" for the shapes that did not match; strip the rest of a shape like A([x]) or A((x)).
            label = next((x for x in label if x), "").strip("()[]{}")
            if '"' in label and not (label.startswith('"') and label.endswith('"')):
                err(f"diagram {n}: a double quote inside the label [{label}] ends it early; use single quotes")
            check_label(n, label, err, warn)
        for label in re.findall(r"\|(.*?)\|", line):
            check_label(n, label, err, warn)
        bare = re.sub(r"\[.*?\]|\(.*?\)|\{.*?\}|\|.*?\|", "", line)
        bare = re.sub(r"--\s[^>]*?-->|-\.\s[^>]*?\.->", "-->", bare)
        chain = [t.strip() for t in ARROW.split(bare)]
        ids = [t for t in chain if re.fullmatch(r"\w+", t)]
        nodes.update(ids)
        if len(ids) == len(chain):
            for a, b in zip(ids, ids[1:]):
                fanout.setdefault(a, set()).add(b)
    if direction in ("LR", "RL") and len(nodes) > MAX_LR_NODES:
        err(f"diagram {n}: left-to-right with {len(nodes)} nodes; use flowchart TD (left-to-right holds {MAX_LR_NODES} at most)")
    if subgraphs > 1:
        err(f"diagram {n}: {subgraphs} subgraphs sit side by side and shrink; keep one at most")
    for a, b in fanout.items():
        if len(b) > MAX_FANOUT:
            warn(f"diagram {n}: node {a} fans out to {len(b)} nodes in one row; split the diagram or stack them")


def cmd_check(args):
    page = Path(args.file).read_text(encoding="utf-8")
    errors, warnings = [], []
    err, warn = errors.append, warnings.append
    no_comments = re.sub(r"<!--.*?-->", "", page, flags=re.S)

    title = re.search(r"<title>(.*?)</title>", page, re.S)
    if not title or not title.group(1).strip() or "{{" in title.group(1):
        err("the page has no real <title>")
    if not re.search(r'<html[^>]*\blang="[^"]+"', page):
        warn("<html> has no lang attribute")
    for m in sorted(set(re.findall(r"\{\{[^}]*\}\}|\[\[[^\]]*\]\]", no_comments))):
        err(f"placeholder left unfilled: {m}")
    if re.search(r"\[\[[a-z_]+\]\]", page):
        err("fixed strings left unfilled; create pages with 'page.py new'")

    visible = re.sub(r"<(script|style|code)\b.*?</\1>", " ", no_comments, flags=re.S)
    visible = html.unescape(re.sub(r"<[^>]+>", " ", visible))
    visible = re.sub(r"#[0-9A-Fa-f]{3,8}\b", " ", visible)  # diagram colours
    for tok in sorted(set(re.findall(r"\b(?:[A-Z]{2,5}-?\d{1,4}|[A-Z]-\d{1,4})\b", visible))):
        err(f"ID-shaped code in the text: {tok}; name the thing in everyday words")
    for tok in sorted(set(re.findall(r"\b\d+\.\d+\.\d+(?:\.\d+)*\b", visible))):
        warn(f"section-number-like token in the text: {tok}; name what the section says, unless it is a real version or amount")
    for tok in sorted(set(m.group(0) for m in re.finditer(r"(?<![\w/])[\w./-]*[\w-]\.(?:md|html|py|tsx?|jsx?|go|json|ya?ml|css|sql|figcraft)\b", visible))):
        err(f"file path in the text: {tok}; name what it holds, or put it in <code> where a caller allows paths")

    s = Structure()
    s.feed(page)
    if len(s.groups) > MAX_ITEMS:
        err(f"{len(s.groups)} decisions on one page; keep {MAX_ITEMS} at most and move the rest to the next round")
    radio_names = {}
    for i, g in enumerate(s.groups, 1):
        label = g["name"] or f"group {i}"
        if not g["name"]:
            err(f"decision {i} has no data-name; the answer box needs it")
        if len(g["options"]) < 2:
            err(f"{label}: fewer than two options")
            continue
        recs = [o for o in g["options"] if o["rec"]]
        if len(recs) != 1 or not g["options"][0]["rec"]:
            err(f"{label}: exactly one option must be recommended (class rec), and it comes first")
        names = {o.get("name") for o in g["options"]}
        if len(names) != 1 or None in names:
            err(f"{label}: every option needs the same radio name")
        else:
            name = names.pop()
            if name in radio_names:
                err(f"{label}: radio name '{name}' is also used by {radio_names[name]}")
            radio_names[name] = label
        values = [o.get("value") for o in g["options"]]
        if g["chosen"] is not None and g["chosen"] not in values + ["other", "follow-up"]:
            err(f"{label}: data-chosen=\"{g['chosen']}\" matches no option ({', '.join(map(str, values + ['other', 'follow-up']))})")
        if g["chosen"] == "follow-up" and "follow-up" not in s.ids:
            err(f"{label}: data-chosen=\"follow-up\" but the page has no #follow-up section")
        if g["follow"] and not g["num"]:
            warn(f"{label}: a follow-up decision needs data-num, the number of the item it continues")
        if "other" in values:
            err(f"{label}: an option uses the value 'other'; the script adds Another answer itself, so leave it out of the draft")
        if g["chosen"] == "other" and not (g["other"] or "").strip():
            err(f"{label}: data-chosen=\"other\" has no data-other; record the user's own answer as <radio-name>=other:<text>")
        if g["chosen"] is None and not g["options"][0].get("checked"):
            warn(f"{label}: the recommended option should start checked")

    for target in s.nav_links:
        if target not in s.ids:
            err(f"the item list links to #{target}, which does not exist")
    for sec in s.sections:
        if sec["groups"] and sec["id"] not in s.nav_links:
            warn(f"section #{sec['id']} holds a decision but is missing from the item list")
        if sec["chip"] and not sec["risk"] and sec["groups"]:
            warn(f"section #{sec['id']} is flagged but has no risk box saying why")
    if any(g["chosen"] for g in s.groups) and not s.has_decided:
        err("answers are recorded (data-chosen) but the page has no decided banner")
    if s.has_answer:
        for needed in ("answer-text", "copy", "copy-status"):
            if needed not in s.ids:
                err(f"the answer box lacks #{needed}; run 'page.py refresh' and fix its ids")

    if s.raw_br_in_mermaid:
        err(f"{s.raw_br_in_mermaid} raw <br/> tag(s) inside a diagram; write &lt;br/&gt; so Mermaid receives the line break")
    for n, text in enumerate(s.mermaid, 1):
        check_mermaid(n, html.unescape(text), err, warn)

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)" if errors or warnings else "ok")
    sys.exit(1 if errors else 0)


def main():
    p = argparse.ArgumentParser(description="Review page helper.")
    sub = p.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="create a page from the template in the temp directory")
    n.add_argument("topic")
    n.add_argument("--lang", default="en")
    n.add_argument("--main", help="file holding the page's <main>...</main>")
    n.add_argument("--title", help="the page's <title>")
    n.set_defaults(func=cmd_new)
    d = sub.add_parser("decide", help="record answers as data-chosen")
    d.add_argument("file")
    d.add_argument("answers", nargs="+", metavar="NAME=LETTER")
    d.set_defaults(func=cmd_decide)
    c = sub.add_parser("check", help="report rule violations")
    c.add_argument("file")
    c.set_defaults(func=cmd_check)
    r = sub.add_parser("refresh", help="rebuild a page on the current template")
    r.add_argument("file")
    r.add_argument("--lang")
    r.set_defaults(func=cmd_refresh)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
