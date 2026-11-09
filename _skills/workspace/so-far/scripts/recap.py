#!/usr/bin/env python3
"""So-far recap page helper.

  recap.py new <slug> [--lang LANG] [--main FILE] [--title TEXT]
        write <tmpdir>/so-far/<slug>-<YYYYMMDD-HHMM>.html from the template, its fixed strings
        in LANG (default en) and [[slug]] filled; with --main, FILE's <main>...</main> replaces
        the template's example. Prints the path.
  recap.py check <file>
        report rule violations; exit 1 when any ERROR is found

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
SECTIONS = ["timeline", "happened", "why-next", "next", "open"]
PROVENANCE = {"reviewed", "recommendation", "unrecorded", "unread", "skipped"}
SLIPPED = {"unread", "skipped"}
MAX_DAYS = 7
MIN_REASONS, MAX_REASONS = 2, 3
VOID = {"input", "br", "meta", "link", "img", "hr", "source", "wbr"}


def load_strings(lang):
    path = STRINGS / f"{lang}.json"
    if not path.exists():
        sys.exit(f"No strings for '{lang}'. Add {path} by copying en.json and translating it.")
    return path, json.loads(path.read_text(encoding="utf-8"))


def render(lang, slug, main=None, title=None):
    """The template with `main` and `title` swapped in, then every [[key]] filled from strings/<lang>.json."""
    path, strings = load_strings(lang)
    out = TEMPLATE.read_text(encoding="utf-8")
    if main:
        out = re.sub(r"<main>.*</main>", lambda _: main, out, count=1, flags=re.S)
    if title:
        out = re.sub(r"<title>.*?</title>", lambda _: title, out, count=1, flags=re.S)
    out = out.replace("[[js_strings]]", json.dumps(strings["js"], ensure_ascii=False))
    values = {**strings, "slug": slug}

    def fill(m):
        key = m.group(1)
        if not isinstance(values.get(key), str):
            sys.exit(f"{path.name} lacks the key '{key}'.")
        return html.escape(values[key], quote=True)

    return re.sub(r"\[\[([a-z_]+)\]\]", fill, out)


def main_block(text, source):
    m = re.search(r"<main>.*</main>", text, re.S)
    if not m:
        sys.exit(f"{source} has no <main>...</main> block.")
    return m.group(0)


def cmd_new(args):
    body = main_block(Path(args.main).read_text(encoding="utf-8"), args.main) if args.main else None
    title = f"<title>{html.escape(args.title)}</title>" if args.title else None
    out = render(args.lang, args.slug, body, title)
    name = re.sub(r"[^a-z0-9]+", "-", args.slug.lower()).strip("-") or "recap"
    folder = Path(tempfile.gettempdir()) / "so-far"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}-{time.strftime('%Y%m%d-%H%M')}.html"
    if path.exists():
        path = folder / f"{name}-{time.strftime('%Y%m%d-%H%M%S')}.html"
    path.write_text(out, encoding="utf-8")
    print(path)


class Structure(HTMLParser):
    """Collects the parts of a recap the rules look at."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.sections = []
        self.days = 0
        self.here = 0
        self.next_chips = 0
        self.stage_links = []
        self.stage_cards = []
        self.badges = []
        self.slipped_callout = False
        self.none_callout = False
        self.reasons = 0
        self.steps = []
        self._stack = []

    def _inside(self, *classes):
        return any(set(classes) <= cls for _, cls, _ in self._stack)

    def _section(self):
        return next((id_ for tag, _, id_ in reversed(self._stack) if tag == "section"), None)

    def _card(self):
        return next((id_ for _, cls, id_ in reversed(self._stack) if "stage-card" in cls), None)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get("class") or "").split())
        parent = self._stack[-1] if self._stack else (None, set(), None)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "section" and parent[0] == "main":
            self.sections.append(a.get("id"))
        if tag == "li" and "day" in cls:
            self.days += 1
        if "here" in cls:
            self.here += 1
        if "stage" in cls and "next" in cls:
            self.next_chips += 1
        if tag == "a" and "stage" in cls:
            self.stage_links.append((a.get("href") or "", cls))
        if "stage-card" in cls:
            self.stage_cards.append(a.get("id"))
        if "badge" in cls:
            self.badges.append((cls & PROVENANCE, self._inside("callout", "slipped"), self._card()))
        if "callout" in cls and "slipped" in cls:
            self.slipped_callout = True
        if "callout" in cls and "none" in cls and self._section() == "happened":
            self.none_callout = True
        if tag == "li" and parent[0] == "ol" and "reasons" in parent[1]:
            self.reasons += 1
        if tag == "li" and "step" in cls:
            self.steps.append(False)
        if "who" in cls and self.steps and self._inside("step"):
            self.steps[-1] = True
        if tag not in VOID:
            self._stack.append((tag, cls, a.get("id")))

    def handle_endtag(self, tag):
        if any(t == tag for t, _, _ in self._stack):
            while self._stack and self._stack.pop()[0] != tag:
                pass


def check_text(page, strings, err, warn):
    """Wording rules: IDs, codes and file paths stay in the files."""
    no_comments = re.sub(r"<!--.*?-->", "", page, flags=re.S)
    visible = re.sub(r"<(script|style|code)\b.*?</\1>", " ", no_comments, flags=re.S)
    visible = html.unescape(re.sub(r"<[^>]+>", " ", visible))
    for tok in sorted(set(re.findall(r"\b(?:[A-Z]{2,5}-?\d{1,4}|[A-Z]-\d{1,4})\b", visible))):
        err(f"ID-shaped code in the text: {tok}; name the thing in everyday words")
    for tok in sorted(set(re.findall(r"\b[A-Z]\d{1,2}\b", visible))):
        warn(f"phase-code-like token in the text: {tok}; name the phase, unless it is a real product name")
    words = strings.get("id_words", []) if strings else []
    if words:
        pattern = r"\b(?:" + "|".join(map(re.escape, words)) + r")\s+#?\d+\b"
        for tok in sorted(set(re.findall(pattern, visible, re.I))):
            warn(f"numbered reference in the text: '{tok}'; say what was decided or asked instead")
    for tok in sorted(set(re.findall(r"#\d+\b", visible))):
        warn(f"numbered reference in the text: {tok}; say what it is instead")
    for tok in sorted(set(m.group(0) for m in re.finditer(r"(?<![\w/])[\w./-]*[\w-]\.(?:md|html|py|tsx?|jsx?|go|json|ya?ml|css|sql)\b", visible))):
        err(f"file path in the text: {tok}; name what it holds, or put it in <code> where the user would open it")


def cmd_check(args):
    page = Path(args.file).read_text(encoding="utf-8")
    errors, warnings = [], []
    err, warn = errors.append, warnings.append
    no_comments = re.sub(r"<!--.*?-->", "", page, flags=re.S)

    title = re.search(r"<title>(.*?)</title>", page, re.S)
    if not title or not title.group(1).strip() or "{{" in title.group(1):
        err("the page has no real <title>")
    lang = re.search(r'<html[^>]*\blang="([^"]+)"', page)
    if not lang:
        warn("<html> has no lang attribute")
    for m in sorted(set(re.findall(r"\{\{[^}]*\}\}|\[\[[^\]]*\]\]", no_comments))):
        err(f"placeholder left unfilled: {m}")
    if re.search(r"\[\[[a-z_]+\]\]", page):
        err("fixed strings left unfilled; create pages with 'recap.py new'")

    strings = None
    if lang and (STRINGS / f"{lang.group(1)}.json").exists():
        strings = load_strings(lang.group(1))[1]
    check_text(page, strings, err, warn)

    s = Structure()
    s.feed(page)
    present = [x for x in s.sections if x in SECTIONS]
    for name in SECTIONS:
        if name not in present:
            err(f"section #{name} is missing")
    if present != [x for x in SECTIONS if x in present]:
        err(f"sections are out of order: {', '.join(present)}; keep {', '.join(SECTIONS)}")

    if s.here != 1:
        err(f"the timeline needs exactly one 'you are here' marker (.here), found {s.here}")
    if s.next_chips != 1:
        err(f"the timeline needs exactly one next-step chip (.stage.next), found {s.next_chips}")
    if s.days > MAX_DAYS + 1:
        warn(f"{s.days - 1} day rows; collapse the older days to one line each (at most {MAX_DAYS})")
    for href, _ in s.stage_links:
        if not href.startswith("#") or href[1:] not in s.ids:
            err(f"a stage chip links to '{href}', which is not a section or card on this page")
    linked = {h[1:] for h, _ in s.stage_links}
    for card in s.stage_cards:
        if not card:
            err("a stage card has no id; its timeline chip needs one to link to")
        elif card not in linked:
            warn(f"stage card #{card} has no chip in the timeline")

    in_cards = in_callout = 0
    for kinds, callout, _ in s.badges:
        if len(kinds) != 1:
            err(f"a badge needs exactly one of: {', '.join(sorted(PROVENANCE))}")
            continue
        if kinds & SLIPPED:
            if callout:
                in_callout += 1
            else:
                in_cards += 1
    if in_cards and not s.slipped_callout:
        err(f"{in_cards} decision(s) approved unread or skipped, but no .callout.slipped lists them before the stage cards")
    elif s.slipped_callout and in_cards != in_callout:
        warn(f"the unread/skipped callout lists {in_callout} decision(s), the stage cards hold {in_cards}; list each once in both")
    if not (s.slipped_callout or s.none_callout or in_cards):
        warn("say in one line that nothing was approved unread or skipped (.callout.none)")
    slipped_cards = {card for kinds, _, card in s.badges if kinds & SLIPPED and card}
    for href, cls in s.stage_links:
        if href[1:] in slipped_cards and "flag" not in cls:
            warn(f"stage card {href} holds an unread or skipped decision, but its timeline chip lacks the flag class")
        elif "flag" in cls and href[1:] not in slipped_cards:
            warn(f"the timeline chip for {href} is flagged, but its card holds no unread or skipped decision")

    if not MIN_REASONS <= s.reasons <= MAX_REASONS:
        warn(f"'why the next step' holds {s.reasons} reason(s); give {MIN_REASONS} or {MAX_REASONS}")
    if not s.steps:
        err("'what comes next' has no steps (li.step)")
    for i, has_who in enumerate(s.steps, 1):
        if not has_who:
            err(f"next step {i} has no who chip (.who, or .who.you for the user's own step)")
    if "/resume-here" not in page:
        warn("the page has no /resume-here line to continue with")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)" if errors or warnings else "ok")
    sys.exit(1 if errors else 0)


def main():
    p = argparse.ArgumentParser(description="So-far recap page helper.")
    sub = p.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="create a recap page from the template in the temp directory")
    n.add_argument("slug")
    n.add_argument("--lang", default="en")
    n.add_argument("--main", help="file holding the page's <main>...</main>")
    n.add_argument("--title", help="the page's <title>; defaults to the translated 'So far: <slug>'")
    n.set_defaults(func=cmd_new)
    c = sub.add_parser("check", help="report rule violations")
    c.add_argument("file")
    c.set_defaults(func=cmd_check)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
