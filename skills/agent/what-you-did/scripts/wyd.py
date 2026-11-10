#!/usr/bin/env python3
"""what-you-did page helper.

  wyd.py collect [REVS] [--slug SLUG]
        Snapshot the changes to explain into <tmpdir>/what-you-did/<slug>-<YYYYMMDD-HHMM>/:
        source.json, hunks.json and changes.patch. REVS is a git range (A..B), or one commit
        (that commit alone). Without REVS: every uncommitted change (staged, unstaged and
        untracked, each labelled), or the last commit when nothing is uncommitted.
        Prints the snapshot path and a hunk index for the agent to group.
        A repository without commits is compared against the empty tree, so new files still show;
        a repository whose only commit has no parent shows that commit against the empty tree.
  wyd.py new <snapshot> --groups FILE [--lang LANG]
        Validate FILE (the agent's grouping, see SKILL.md) against the snapshot and render the
        page next to the snapshot; the code on the page comes from the snapshot, never from FILE.
        Prints the page path, then WARN lines. Exit 1 on any ERROR, and no page is written.

Fixed strings live in strings/<lang>.json; add a language by copying en.json and translating it.
Generated-file patterns live in generated.txt in this skill's folder (portable defaults), plus
.claude/what-you-did-generated.txt and what-you-did-generated.txt at the repo root when they exist
(the project's own; skill updates leave them alone).
"""
import argparse
import fnmatch
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "template.html"
STRINGS = ROOT / "strings"
GENERATED = ROOT / "generated.txt"
PROJECT_GENERATED = (Path(".claude") / "what-you-did-generated.txt", Path("what-you-did-generated.txt"))
SOURCES = {"conversation", "commit", "plan", "inferred"}
KINDS = {"change", "supporting", "outside-plan"}
MAX_GROUPS = 7
MAX_LABEL_LINE = 25
MAX_FANOUT = 3
MAX_LR_NODES = 4
HUNK_HEAD = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@ ?(.*)$")


# ---------- git and diff parsing ----------

def run_git(*args, input=None):
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", input=input)
    except FileNotFoundError:
        sys.exit("git is not installed or not on PATH: this skill reads changes through git")


def git(*args, ok=(0,)):
    p = run_git(*args)
    if p.returncode not in ok:
        sys.exit(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p.stdout


def git_try(*args):
    """The output of a git command, or None when it fails."""
    p = run_git(*args)
    return p.stdout if p.returncode == 0 else None


def empty_tree():
    """The id of git's empty tree: the base for a repository with no earlier commit."""
    return run_git("hash-object", "-t", "tree", "--stdin", input="").stdout.strip()


def rev_range(base, head):
    """`base..head`, or everything up to `head` when `base` is the empty tree (a root commit has no parent)."""
    return head if base == empty_tree() else f"{base}..{head}"


def generated_patterns(top):
    """The skill's portable patterns, then the repo's own list, which `skills update` never overwrites."""
    out = []
    for f in (GENERATED, *(Path(top) / p for p in PROJECT_GENERATED)):
        if f.exists():
            out += [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    return out


def is_generated(path, patterns):
    return any(fnmatch.fnmatch(path, p) or fnmatch.fnmatch(Path(path).name, p) for p in patterns)


def parse_diff(text, label, patterns, hunks):
    """Append one dict per hunk of the unified diff `text` to `hunks`; a binary file is one hunk without lines."""
    files = re.split(r"(?m)^diff --git ", text)
    for block in files[1:]:
        lines = block.split("\n")
        m = re.match(r'"?a/(.*?)"? "?b/(.*?)"?$', lines[0])
        old_path, new_path = (m.group(1), m.group(2)) if m else (lines[0], lines[0])
        status = "modified"
        i = 1
        while i < len(lines) and not lines[i].startswith("@@"):
            l = lines[i]
            if l.startswith("new file mode"):
                status = "added"
            elif l.startswith("deleted file mode"):
                status = "deleted"
            elif l.startswith("rename from"):
                status = "renamed"
            elif l.startswith("Binary files") or l.startswith("GIT binary patch"):
                status = "binary"
            elif l.startswith("--- ") and l[4:] != "/dev/null":
                old_path = re.sub(r'^"?a/', "", l[4:]).rstrip('"')
            elif l.startswith("+++ ") and l[4:] != "/dev/null":
                new_path = re.sub(r'^"?b/', "", l[4:]).rstrip('"')
            i += 1
        path = old_path if status == "deleted" else new_path
        base = {"file": path, "old_file": old_path, "status": status, "label": label,
                "generated": is_generated(path, patterns)}
        if i >= len(lines):
            hunks.append({**base, "old_start": 0, "old_len": 0, "new_start": 0, "new_len": 0,
                          "context": "", "lines": [], "adds": 0, "dels": 0})
            continue
        cur = None
        for l in lines[i:]:
            h = HUNK_HEAD.match(l)
            if h:
                o, ol, n, nl = int(h.group(1)), int(h.group(2) or 1), int(h.group(3)), int(h.group(4) or 1)
                cur = {**base, "old_start": o, "old_len": ol, "new_start": n, "new_len": nl,
                       "context": h.group(5), "lines": [], "adds": 0, "dels": 0}
                hunks.append(cur)
                on, nn = o, n
                continue
            if cur is None or l == "" or l.startswith("\\"):
                continue
            t, body = l[0], l[1:]
            if t == "+":
                cur["lines"].append(["+", None, nn, body]); nn += 1; cur["adds"] += 1
            elif t == "-":
                cur["lines"].append(["-", on, None, body]); on += 1; cur["dels"] += 1
            elif t == " ":
                cur["lines"].append([" ", on, nn, body]); on += 1; nn += 1


def first_line(h):
    """The line a reader jumps to: the first added line, else the first removed one (old numbering)."""
    for t, o, n, _ in h["lines"]:
        if t == "+":
            return n
        if t == "-":
            return o if h["status"] == "deleted" else max(h["new_start"], 1)
    return max(h["new_start"], 1)


REF = re.compile(r"^(h\d+)(?::(\d+)-(\d+))?$")


def parse_ref(ref):
    """'h12' is the whole hunk; 'h12:30-45' only its lines 30 to 45 (new numbering; old for a deleted file)."""
    m = REF.match(ref)
    if not m:
        return None
    return m.group(1), (int(m.group(2)), int(m.group(3))) if m.group(2) else None


def slice_lines(h, rng):
    if rng is None:
        return h["lines"]
    if h["status"] == "deleted":
        return [l for l in h["lines"] if rng[0] <= l[1] <= rng[1]]
    out, pos = [], h["new_start"] + h["new_len"]
    for l in reversed(h["lines"]):
        if l[0] != "-":
            pos = l[2]
        if rng[0] <= pos <= rng[1]:
            out.append(l)
    return out[::-1]


def attribute(source, hunks):
    """Record which commits of the range wrote each hunk: blame for added lines, the file's log otherwise.

    h["blame"] maps an added line (new numbering) to its commit; h["touched"] lists every commit of the
    range that changed the file, the fallback for removed lines, which blame cannot place.
    """
    base, head = source["base"], source["head"]
    span_rev = rev_range(base, head)
    root = ["--root"] if span_rev == head else []
    file_log = {}
    for h in hunks:
        path = h["file"]
        if path not in file_log:
            file_log[path] = [l[:9] for l in git("log", "--format=%H", "--follow", span_rev, "--", path).split()]
        h["touched"] = file_log[path]
        h["blame"] = {}
        added = [l[2] for l in h["lines"] if l[0] == "+"]
        if not added or h["status"] == "deleted":
            continue
        spans, start, prev = [], added[0], added[0]
        for n in added[1:] + [None]:
            if n != (prev + 1 if prev is not None else None):
                spans += ["-L", f"{start},{prev}"]
                start = n
            prev = n
        out = git("blame", "-l", "-s", *root, *spans, span_rev, "--", path, ok=(0, 128))
        for line in out.splitlines():
            m = re.match(r"(\^?)([0-9a-f]{40})\s+(?:\S+\s+)?(\d+)\)", line)
            if m and not m.group(1):
                h["blame"][str(int(m.group(3)))] = m.group(2)[:9]


def commit_log(base, head):
    out = git("log", "--reverse", "--format=%H%x1f%s%x1f%b%x1e", rev_range(base, head))
    commits = []
    for rec in out.split("\x1e"):
        rec = rec.strip("\n")
        if rec:
            sha, subject, body = (rec.split("\x1f") + ["", ""])[:3]
            commits.append({"sha": sha[:9], "subject": subject, "body": body.strip()})
    return commits


def hunk_commits(h, rng=None):
    """Commits behind a hunk, or behind lines start-end of it.

    Added lines name their commit through blame. Removed lines cannot be blamed, so a slice holding
    any (or no blamed line at all) also lists every commit of the range that changed the file.
    """
    if "blame" not in h:
        return []
    lines = slice_lines(h, rng)
    found = list(dict.fromkeys(h["blame"][str(l[2])] for l in lines if l[0] == "+" and str(l[2]) in h["blame"]))
    if not found or any(l[0] == "-" for l in lines):
        found += [c for c in h["touched"] if c not in found]
    return found


def cmd_collect(args):
    p = run_git("rev-parse", "--show-toplevel")
    if p.returncode != 0:
        if "not a git repository" in p.stderr:
            sys.exit("not a git repository: this skill reads changes through git")
        sys.exit(f"git rev-parse --show-toplevel failed: {p.stderr.strip()}")
    top = p.stdout.strip()
    os.chdir(top)
    patterns = generated_patterns(top)
    # No commit yet: compare against the empty tree, so new files still show.
    head_out = git_try("rev-parse", "--verify", "-q", "HEAD")
    has_commits = head_out is not None
    head = head_out.strip() if has_commits else empty_tree()
    hunks, patch, commits = [], [], []
    flags = ["--no-color", "--no-ext-diff", "-M", "-U3"]
    if args.revs:
        if not has_commits:
            sys.exit("This repository has no commits yet, so there is no commit or range to show. Run collect without a range to see the uncommitted files.")
        if ".." in args.revs:
            a, b = args.revs.split("..", 1)
            a, b = git("rev-parse", a or "HEAD").strip(), git("rev-parse", b or "HEAD").strip()
        else:
            b = git("rev-parse", args.revs).strip()
            parent = git_try("rev-parse", "--verify", "-q", f"{b}^")
            a = parent.strip() if parent else empty_tree()
        source = {"kind": "range", "base": a, "head": b, "range": f"{a[:9]}..{b[:9]}"}
        d = git("diff", *flags, a, b)
        patch.append(d)
        parse_diff(d, "committed", patterns, hunks)
    else:
        staged = git("diff", "--cached", *flags)
        unstaged = git("diff", *flags)
        untracked = [f for f in git("ls-files", "--others", "--exclude-standard", "-z").split("\0") if f]
        if staged or unstaged or untracked:
            source = {"kind": "uncommitted", "base": head, "head": None, "range": None}
            for d, label in ((staged, "staged"), (unstaged, "unstaged")):
                patch.append(d)
                parse_diff(d, label, patterns, hunks)
            for f in untracked:
                d = git("diff", *flags, "--no-index", "--", "/dev/null", f, ok=(0, 1))
                patch.append(d)
                parse_diff(d, "untracked", patterns, hunks)
        else:
            if not has_commits:
                sys.exit("No changes found: this repository has no commits yet and no files to show.")
            parent = git_try("rev-parse", "--verify", "-q", "HEAD^")
            a = parent.strip() if parent else empty_tree()
            source = {"kind": "range", "base": a, "head": head, "range": f"{a[:9]}..{head[:9]}"}
            d = git("diff", *flags, a, head)
            patch.append(d)
            parse_diff(d, "committed", patterns, hunks)
    if source["kind"] == "range":
        commits = commit_log(source["base"], source["head"])
        attribute(source, hunks)
    if not hunks:
        sys.exit("No changes found for that source.")
    for n, h in enumerate(hunks, 1):
        h["id"] = f"h{n}"
        h["jump"] = first_line(h)
    source.update({"repo": top, "commits": commits, "created": time.strftime("%Y-%m-%d %H:%M")})
    slug = re.sub(r"[^a-z0-9-]+", "-", (args.slug or "changes").lower()).strip("-") or "changes"
    stem = Path(tempfile.gettempdir()) / "what-you-did" / f"{slug}-{time.strftime('%Y%m%d-%H%M%S')}"
    snap, n = stem, 1
    while snap.exists():
        n += 1
        snap = stem.with_name(f"{stem.name}-{n}")
    snap.mkdir(parents=True)
    source["snapshot"] = str(snap)
    (snap / "source.json").write_text(json.dumps(source, indent=2), encoding="utf-8")
    (snap / "hunks.json").write_text(json.dumps(hunks), encoding="utf-8")
    (snap / "changes.patch").write_text("".join(patch), encoding="utf-8")
    print(snap)
    what = source["range"] or f"uncommitted changes on {head[:9]}"
    print(f"source: {what}" + (f" ({len(commits)} commits)" if commits else ""))
    for c in commits:
        print(f"  commit {c['sha']} {c['subject']}")
        for line in c["body"].splitlines():
            print(f"         {line}")
    gen = {}
    for h in hunks:
        if h["generated"]:
            g = gen.setdefault(h["file"], [0, 0, 0])
            g[0] += 1; g[1] += h["adds"]; g[2] += h["dels"]
            continue
        changed = next((b for t, _, _, b in h["lines"] if t != " " and b.strip()), "")
        span = f"{h['jump']}" if h["status"] != "binary" else "binary"
        by = ",".join(hunk_commits(h))
        by = f" by {by}" if by else ""
        print(f"{h['id']:>5}  {h['file']}:{span}  +{h['adds']} -{h['dels']}  [{h['label']}, {h['status']}{by}]  {changed.strip()[:70]}")
    for f, (n, a, d) in gen.items():
        print(f"  gen  {f}  {n} hunks  +{a} -{d}  (folded automatically)")


# ---------- validation ----------

ARROW = re.compile(r"\s*(?:<?-+\.?-*>|<?=+>|-{3,}|-\.-)\s*")


def check_mermaid(where, text, err, warn):
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    if not lines:
        return err(f"{where}: empty diagram")
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
            label = next((x for x in label if x), "")
            if '"' in label and not (label.startswith('"') and label.endswith('"')):
                err(f"{where}: a double quote inside the label [{label}] ends it early; use single quotes")
            for part in re.split(r"<br\s*/?>", label):
                if len(part) > MAX_LABEL_LINE:
                    warn(f"{where}: label line over {MAX_LABEL_LINE} characters, break it with <br/>: {part!r}")
        bare = re.sub(r"\[.*?\]|\(.*?\)|\{.*?\}|\|.*?\|", "", line)
        chain = [t.strip() for t in ARROW.split(bare)]
        ids = [t for t in chain if re.fullmatch(r"[\w,]+", t)]
        nodes.update(ids)
        if len(ids) == len(chain):
            for a, b in zip(ids, ids[1:]):
                fanout.setdefault(a, set()).add(b)
    if direction in ("LR", "RL") and len(nodes) > MAX_LR_NODES:
        err(f"{where}: left-to-right with {len(nodes)} nodes; use flowchart TD")
    if subgraphs > 1:
        err(f"{where}: {subgraphs} subgraphs; keep one at most")
    for a, b in fanout.items():
        if len(b) > MAX_FANOUT:
            warn(f"{where}: node {a} fans out to {len(b)} nodes; split the diagram")


def validate(spec, hunks, err, warn):
    by_id = {h["id"]: h for h in hunks}
    focus = spec.get("focus")
    seen, sliced = {}, {}
    for k in ("title", "lead"):
        if not str(spec.get(k, "")).strip():
            err(f"'{k}' is missing")
    groups = spec.get("groups") or []
    if not groups:
        err("'groups' is empty")
    for gi, g in enumerate(groups, 1):
        where = f"group {gi} ({g.get('title', '?')})"
        for k in ("title", "purpose"):
            if not str(g.get(k, "")).strip():
                err(f"{where}: '{k}' is missing")
        if g.get("source") not in SOURCES:
            err(f"{where}: 'source' must be one of {sorted(SOURCES)}")
        if g.get("kind", "change") not in KINDS:
            err(f"{where}: 'kind' must be one of {sorted(KINDS)}")
        if g.get("source") == "commit" and g.get("mismatch"):
            err(f"{where}: source 'commit' and a 'mismatch' contradict each other; a purpose the code contradicts is not its source")
        if g.get("source") == "commit" and not group_commits(g, by_id):
            err(f"{where}: source 'commit' but none of its hunks comes from a commit")
        if g.get("source") == "plan" and not spec.get("workspace"):
            err(f"{where}: source 'plan' needs a 'workspace'")
        if spec.get("workspace") and g.get("kind", "change") == "change" and not g.get("plan_item") and not focus:
            warn(f"{where}: in a workspace a change group names its 'plan_item'; else make it 'supporting' or 'outside-plan'")
        if not g.get("hunks") and not g.get("excerpts"):
            err(f"{where}: shows no code (no 'hunks', no 'excerpts')")
        for ref in g.get("hunks", []):
            parsed = parse_ref(ref)
            if not parsed or parsed[0] not in by_id:
                err(f"{where}: unknown hunk reference {ref} (write h7, or h7:30-45 for some of its lines)")
                continue
            hid, rng = parsed
            if rng and not slice_lines(by_id[hid], rng):
                err(f"{where}: {ref} holds no lines of {hid}")
            if not focus:
                if rng is None and hid in seen:
                    err(f"{where}: hunk {hid} is also in group {seen[hid]}; a whole hunk sits in exactly one group")
                if rng is None and hid in sliced:
                    err(f"{where}: hunk {hid} is shown whole here and in slices in group {sliced[hid]}")
                if rng is not None and hid in seen:
                    err(f"{where}: {ref} slices hunk {hid}, which group {seen[hid]} shows whole")
            (sliced if rng else seen).setdefault(hid, gi)
        for x in g.get("excerpts", []):
            if not {"file", "start", "end"} <= set(x) or x["start"] < 1 or x["end"] < x["start"]:
                err(f"{where}: an excerpt needs 'file', 'start' <= 'end' (1-based)")
        if g.get("diagram"):
            check_mermaid(f"{where} diagram", g["diagram"], err, warn)
    omitted = set()
    for o in spec.get("omitted", []):
        if o.get("hunk") not in by_id or not str(o.get("reason", "")).strip():
            err(f"omitted entry {o}: needs a known 'hunk' id and a 'reason'")
        elif o["hunk"] in seen or o["hunk"] in sliced:
            err(f"hunk {o['hunk']} is omitted but also shown in group {seen.get(o['hunk']) or sliced.get(o['hunk'])}")
        omitted.add(o.get("hunk"))
    if not focus:
        missing = [h["id"] for h in hunks if not h["generated"] and h["id"] not in seen and h["id"] not in sliced and h["id"] not in omitted]
        if missing:
            err(f"hunks in no group: {', '.join(missing)}; every hunk sits in exactly one group")
    regular = [g for g in groups if g.get("kind", "change") == "change"]
    if len(regular) > MAX_GROUPS:
        warn(f"{len(regular)} change groups (over {MAX_GROUPS}): the page renders as an overview with code folded")
    if spec.get("no_code") and not spec.get("workspace"):
        err("'no_code' lists plan items, so it needs a 'workspace'")


# ---------- rendering ----------

def esc(s):
    return html.escape(str(s), quote=True)


def read_excerpt(source, x):
    rev = x.get("rev", "worktree")
    if rev == "worktree":
        p = Path(source["repo"]) / x["file"]
        if not p.exists():
            return None
        text = p.read_text(encoding="utf-8", errors="replace")
    else:
        try:
            text = subprocess.run(["git", "-C", source["repo"], "show", f"{rev}:{x['file']}"],
                                  capture_output=True, text=True, check=True, encoding="utf-8", errors="replace").stdout
        except subprocess.CalledProcessError:
            return None
    lines = text.split("\n")
    if x["end"] > len(lines):
        return None
    return lines[x["start"] - 1:x["end"]]


def split_rows(lines):
    """Pair removed and added lines of each change block for the side-by-side view."""
    rows, dels, adds = [], [], []

    def flush():
        for k in range(max(len(dels), len(adds))):
            rows.append((dels[k] if k < len(dels) else None, adds[k] if k < len(adds) else None))
        dels.clear(); adds.clear()

    for ln in lines:
        if ln[0] == "-":
            dels.append(ln)
        elif ln[0] == "+":
            adds.append(ln)
        else:
            flush()
            rows.append((ln, ln))
    flush()
    return rows


def cell(ln, side):
    if ln is None:
        return '<td class="n"></td><td class="c empty"></td>'
    t, o, n, body = ln
    cls = {"+": "add", "-": "del", " ": "ctx"}[t]
    if side == "uni":
        nums = f'<td class="n">{o or ""}</td><td class="n">{n or ""}</td>'
    else:
        num = o if side == "old" else n
        nums = f'<td class="n">{num or ""}</td>'
    return f'{nums}<td class="c {cls}"><span class="sig">{"" if t == " " else t}</span>{esc(body)}</td>'


def render_hunk(ref, by_id, s, source):
    hid, rng = parse_ref(ref)
    h = by_id[hid]
    lines = slice_lines(h, rng)
    line = rng[0] if rng else h["jump"]
    jump = f"{h['file']}:{line}"
    vs = f"vscode://file/{source['repo']}/{h['file']}:{line}"
    adds = sum(1 for l in lines if l[0] == "+")
    dels = sum(1 for l in lines if l[0] == "-")
    label = s["label_" + h["label"]]
    status = s["status_" + h["status"]] if h["status"] != "modified" else ""
    shas = " ".join(hunk_commits(h, rng))
    meta = " · ".join(x for x in (label, status, f"+{adds} −{dels}", shas) if x)
    head = (f'<div class="hunk-head"><code class="path">{esc(jump)}</code><span class="meta">{esc(meta)}</span>'
            f'<span class="tools"><button type="button" class="copy-path" data-copy="{esc(jump)}">{esc(s["copy_path"])}</button>'
            f'<a href="{esc(vs)}">{esc(s["open_vscode"])}</a>'
            f'<button type="button" class="explain" data-hunks="{ref}" data-where="{esc(jump)}">{esc(s["explain"])}</button></span></div>')
    hid_attr = f' id="{hid}"' if rng is None else ""
    if h["status"] == "binary" or not lines:
        return f'<div class="hunk"{hid_attr}>{head}<p class="note">{esc(s["no_text"])}</p></div>'
    uni = "".join(f"<tr>{cell(ln, 'uni')}</tr>" for ln in lines)
    split = "".join(f"<tr>{cell(a, 'old')}{cell(b, 'new')}</tr>" for a, b in split_rows(lines))
    ctx = f'<div class="ctx-line">{esc(h["context"])}</div>' if h["context"].strip() and rng is None else ""
    return (f'<div class="hunk"{hid_attr}>{head}{ctx}<div class="code">'
            f'<table class="uni">{uni}</table><table class="split">{split}</table></div></div>')


def render_excerpt(x, s, source):
    lines = read_excerpt(source, x)
    jump = f"{x['file']}:{x['start']}"
    if lines is None:
        return f'<div class="hunk"><div class="hunk-head"><code class="path">{esc(jump)}</code></div><p class="note">{esc(s["excerpt_missing"])}</p></div>'
    vs = f"vscode://file/{source['repo']}/{x['file']}:{x['start']}"
    rev = x.get("rev", "worktree")
    meta = s["excerpt_now"] if rev == "worktree" else s["excerpt_at"].replace("{rev}", rev[:9])
    rows = "".join(f'<tr><td class="n">{x["start"] + k}</td><td class="c ctx"><span class="sig"></span>{esc(b)}</td></tr>' for k, b in enumerate(lines))
    cap = f'<p class="note">{x["caption"]}</p>' if x.get("caption") else ""
    return (f'<div class="hunk excerpt"><div class="hunk-head"><code class="path">{esc(jump)}</code><span class="meta">{esc(meta)}</span>'
            f'<span class="tools"><button type="button" class="copy-path" data-copy="{esc(jump)}">{esc(s["copy_path"])}</button>'
            f'<a href="{esc(vs)}">{esc(s["open_vscode"])}</a></span></div>{cap}<div class="code"><table class="uni">{rows}</table></div></div>')


def ref_where(ref, by_id):
    hid, rng = parse_ref(ref)
    h = by_id[hid]
    return f"{h['file']}:{rng[0]}-{rng[1]}" if rng else f"{h['file']}:{h['jump']}"


def group_commits(g, by_id):
    out = []
    for ref in g.get("hunks", []):
        parsed = parse_ref(ref)
        if parsed and parsed[0] in by_id:
            out += [c for c in hunk_commits(by_id[parsed[0]], parsed[1]) if c not in out]
    return out


def render_commits(g, by_id, source, s):
    """The commit messages behind a group, quoted as git holds them, so the reader can weigh them."""
    known = {c["sha"]: c for c in source.get("commits", []) if isinstance(c, dict)}
    items = []
    for sha in group_commits(g, by_id):
        c = known.get(sha)
        if not c:
            continue
        body = f'<details><summary>{esc(s["commit_body"])}</summary><pre class="msg">{esc(c["body"])}</pre></details>' if c["body"] else ""
        items.append(f'<li><code>{esc(sha)}</code> {esc(c["subject"])}{body}</li>')
    if not items:
        return ""
    return f'<div class="commits"><b>{esc(s["commits_label"])}</b><ul class="plain">{"".join(items)}</ul></div>'


def render_group(n, g, by_id, s, source, folded):
    kind = g.get("kind", "change")
    chip = {"supporting": f'<span class="chip soft">{esc(s["kind_supporting"])}</span>',
            "outside-plan": f'<span class="chip">{esc(s["kind_outside"])}</span>'}.get(kind, "")
    src = f'<span class="src src-{g["source"]}">{esc(s["source_" + g["source"]])}</span>'
    parts = [f'<h2>{n}. {esc(g["title"])} {chip}</h2>']
    if g.get("plan_item"):
        parts.append(f'<p class="plan"><b>{esc(s["plan_item"])}</b> {esc(g["plan_item"])}</p>')
    parts.append(f'<p class="purpose">{src} {g["purpose"]}</p>')
    if g.get("mismatch"):
        parts.append(f'<p class="risk"><strong>{esc(s["mismatch_label"])}</strong> {g["mismatch"]}</p>')
    parts.append(render_commits(g, by_id, source, s))
    if g.get("links"):
        items = "".join(f'<li><a href="{esc(l["href"])}">{esc(l["text"])}</a></li>' if l.get("href") else f"<li>{esc(l['text'])}</li>" for l in g["links"])
        parts.append(f'<div class="links"><b>{esc(s["links"])}</b><ul class="plain">{items}</ul></div>')
    if g.get("diagram"):
        parts.append(f'<div class="diagram"><pre class="mermaid">{esc(g["diagram"])}</pre></div>')
    if g.get("notes"):
        parts.append(f'<div class="notes">{g["notes"]}</div>')
    if g.get("how_to_see"):
        parts.append(f'<p class="see"><b>{esc(s["how_to_see"])}</b> {g["how_to_see"]}</p>')
    code = "".join(render_excerpt(x, s, source) for x in g.get("excerpts", []))
    code += "".join(render_hunk(r, by_id, s, source) for r in g.get("hunks", []))
    ids = ",".join(g.get("hunks", []))
    where = "; ".join(ref_where(r, by_id) for r in g.get("hunks", []))
    count = len(g.get("hunks", [])) + len(g.get("excerpts", []))
    summary = s["show_code"].replace("{n}", str(count))
    parts.append(f'<details class="codebox"{"" if folded else " open"}><summary>{esc(summary)}</summary>{code}</details>')
    parts.append(f'<div class="group-tools"><button type="button" class="explain" data-hunks="{ids}" data-where="{esc(where)}" data-part="{esc(g["title"])}">{esc(s["explain_group"])}</button></div>')
    # Each group folds to its heading; it starts open so its diagram renders at full size.
    return (f'<section id="g{n}" class="group kind-{kind}"><details class="gbox" open><summary>{parts[0]}</summary>'
            f'<div class="gbody">{"".join(parts[1:])}</div></details></section>')


def render(spec, hunks, source, s):
    by_id = {h["id"]: h for h in hunks}
    groups = spec["groups"]
    regular = [g for g in groups if g.get("kind", "change") == "change"]
    folded = len(regular) > MAX_GROUPS
    out = []
    focus = spec.get("focus")
    back = f'<a class="back" href="{esc(spec["back"])}">← {esc(spec.get("back_title") or s["back"])}</a>' if spec.get("back") else ""
    if source["kind"] == "range":
        what = s["source_range"].replace("{range}", source["range"]).replace("{n}", str(len(source["commits"])))
    else:
        what = s["source_uncommitted"].replace("{sha}", source["base"][:9])
    ws = f' · {esc(s["workspace"])} <b>{esc(spec["workspace"])}</b>' if spec.get("workspace") else ""
    fq = ""
    if focus:
        fq = f'<blockquote><b>{esc(s["focus_on"])}</b> {esc(focus.get("part", ""))}' + (f'<br/>{esc(focus["question"])}' if focus.get("question") else "") + "</blockquote>"
    nav = "".join(
        f'<li><a href="#g{i}">{esc(g["title"])}</a>' + (f' <span class="chip">{esc(s["kind_outside"])}</span>' if g.get("kind") == "outside-plan" else "") + "</li>"
        for i, g in enumerate(groups, 1))
    gen = [h for h in hunks if h["generated"]]
    if gen and not focus:
        nav += f'<li><a href="#generated">{esc(s["generated"])}</a></li>'
    if spec.get("omitted"):
        nav += f'<li><a href="#omitted">{esc(s["omitted"])}</a></li>'
    if spec.get("no_code"):
        nav += f'<li><a href="#no-code">{esc(s["no_code"])}</a> <span class="chip">!</span></li>'
    out.append(f'<header id="top">{back}<h1>{esc(spec["title"])}</h1><p class="srcline">{esc(what)}{ws}</p>{fq}<p class="lead">{spec["lead"]}</p>'
               f'<p class="guide">{esc(s["guide"])}</p>'
               f'<nav aria-label="{esc(s["nav"])}"><ol>{nav}</ol></nav></header>')
    if spec.get("no_code"):
        items = "".join(f"<li>{esc(t)}</li>" for t in spec["no_code"])
        out.append(f'<section id="no-code"><h2>{esc(s["no_code"])}</h2><p class="risk">{esc(s["no_code_help"])}</p><ul class="plain">{items}</ul></section>')
    for i, g in enumerate(groups, 1):
        out.append(render_group(i, g, by_id, s, source, folded))
    if spec.get("omitted"):
        items = "".join(f"<li><code>{esc(by_id[o['hunk']]['file'])}</code>: {esc(o['reason'])}</li>" for o in spec["omitted"])
        out.append(f'<section id="omitted"><h2>{esc(s["omitted"])}</h2><ul class="plain">{items}</ul></section>')
    if gen and not focus:
        rows = {}
        for h in gen:
            r = rows.setdefault(h["file"], [0, 0])
            r[0] += h["adds"]; r[1] += h["dels"]
        items = "".join(f"<li><code>{esc(f)}</code> +{a} −{d}</li>" for f, (a, d) in rows.items())
        out.append(f'<section id="generated"><h2>{esc(s["generated"])}</h2><p class="note">{esc(s["generated_help"])}</p><ul class="plain">{items}</ul></section>')
    data = {"snapshot": source["snapshot"], "range": source["range"], "base": source["base"][:9],
            "workspace": spec.get("workspace"), "page": spec["title"]}
    return "<main>" + "".join(out) + "</main>", data


def render_bar(spec, s):
    """The sticky bar: page title, code view switch, and one button folding or opening every group."""
    j = s["js"]
    jump = (f'<div class="jump"><button type="button" class="step" data-step="-1" aria-label="{esc(j["prev"])}" title="{esc(j["prev"])} (k)">◀</button>'
            f'<button type="button" class="cur" aria-haspopup="true" aria-expanded="false"><span class="cur-text">{esc(j["nav_menu"])}</span> ▾</button>'
            f'<button type="button" class="step" data-step="1" aria-label="{esc(j["next"])}" title="{esc(j["next"])} (j)">▶</button>'
            f'<div class="menu" hidden><ol></ol><p class="note">{esc(j["keys_hint"])}</p></div></div>')
    return (f'<div class="topbar"><a class="bar-title" href="#top">{esc(spec["title"])}</a>{jump}'
            f'<div class="bar-tools"><div class="view" role="group" aria-label="{esc(s["view"])}">'
            f'<button type="button" data-view="uni" aria-pressed="true">{esc(s["view_uni"])}</button>'
            f'<button type="button" data-view="split" aria-pressed="false">{esc(s["view_split"])}</button></div>'
            f'<button type="button" id="fold-all">{esc(s["js"]["collapse_all"])}</button></div></div>')


def cmd_new(args):
    snap = Path(args.snapshot)
    source = json.loads((snap / "source.json").read_text(encoding="utf-8"))
    hunks = json.loads((snap / "hunks.json").read_text(encoding="utf-8"))
    spec = json.loads(Path(args.groups).read_text(encoding="utf-8"))
    path = STRINGS / f"{args.lang}.json"
    if not path.exists():
        print(f"WARN  No strings for '{args.lang}'; using 'en'. To add '{args.lang}', copy {STRINGS / 'en.json'} to {path} and translate it.", file=sys.stderr)
        path = STRINGS / "en.json"
    s = json.loads(path.read_text(encoding="utf-8"))
    errors, warnings = [], []
    validate(spec, hunks, errors.append, warnings.append)
    for g in spec.get("groups", []):
        for x in g.get("excerpts", []):
            if {"file", "start", "end"} <= set(x) and read_excerpt(source, x) is None:
                errors.append(f"excerpt {x['file']}:{x['start']}-{x['end']} at {x.get('rev', 'worktree')} does not exist")
    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        for e in errors:
            print(f"ERROR {e}")
        sys.exit(1)
    main, data = render(spec, hunks, source, s)
    page = TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("[[title]]", esc(spec["title"])).replace("[[lang]]", esc(s["lang"]))
    page = page.replace("[[bar]]", render_bar(spec, s))
    page = page.replace("[[main]]", main)
    page = page.replace("[[data]]", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    page = page.replace("[[js_strings]]", json.dumps(s["js"], ensure_ascii=False).replace("</", "<\\/"))
    name = snap.name + (f"-focus-{time.strftime('%H%M%S')}" if spec.get("focus") else "") + ".html"
    out = snap.parent / name
    out.write_text(page, encoding="utf-8")
    print(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("revs", nargs="?")
    c.add_argument("--slug")
    n = sub.add_parser("new")
    n.add_argument("snapshot")
    n.add_argument("--groups", required=True)
    n.add_argument("--lang", default="en")
    a = ap.parse_args()
    {"collect": cmd_collect, "new": cmd_new}[a.cmd](a)


if __name__ == "__main__":
    main()
