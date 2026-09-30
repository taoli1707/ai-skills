#!/usr/bin/env python3
"""Check an HTML page against the mechanical rules of the explainer-html skill.

Usage:
    python3 check_page.py page.html [--kind explainer|report|dashboard|product]
    python3 check_page.py --words          (print the word lists that the checker uses)

Normally you do not call this file. build_page.py builds the page and then runs the checker.

Names in capital letters (brand names, product names) are not abbreviations. Tell the
checker about them with a comment in the page:   <!-- names: LEGO, NASA -->

Exit code: 0 = no FAIL, 1 = at least one FAIL, 2 = the file cannot be read.

The checker uses only the Python standard library. It cannot judge meaning.
It finds the problems that a program can find: long sentences, risky expressions,
hidden content, external resources, and missing parts.
"""
import argparse
import re
import sys
from html.parser import HTMLParser

BLOCK_TAGS = {
    "p", "li", "dd", "dt", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "div", "section",
    "article", "main", "header", "footer", "nav", "aside", "figure", "figcaption", "summary",
    "details", "caption", "blockquote", "ul", "ol", "dl", "table", "thead", "tbody", "tr",
    "body", "html", "form", "fieldset", "label", "button",
}
SKIP_TAGS = {"script", "style", "svg", "pre", "template", "noscript", "head", "title"}
VOID_TAGS = {"br", "img", "hr", "meta", "link", "input", "source", "col", "area", "base",
             "embed", "track", "wbr"}

MAX_WORDS = 25
AVG_TARGET = 20

IDIOMS = [
    "under the hood", "out of the box", "rule of thumb", "rules of thumb", "ballpark",
    "boil down to", "boils down to", "boiled down to", "at the end of the day",
    "low-hanging fruit", "low hanging fruit", "in a nutshell", "deep dive", "dive into",
    "dives into", "diving into", "dive deep", "silver bullet", "on the fly", "from scratch",
    "bottom line", "big picture", "tip of the iceberg", "piece of cake", "game changer",
    "game-changer", "heavy lifting", "rabbit hole", "sweet spot", "pain point",
    "bird's-eye", "bird's eye", "double-edged sword", "elephant in the room",
    "move the needle", "on the same page", "square one", "best of both worlds",
    "hit the ground running", "bang for the buck", "bang for your buck", "apples to apples",
    "apples and oranges", "grain of salt", "devil is in the details", "red flag",
    "green light", "at a glance", "by and large", "so to speak", "kick off", "kicks off",
    "kicked off", "wrap up", "wraps up", "make the cut", "makes the cut", "get the hang of",
    "in the long run", "off the shelf", "off-the-shelf", "spin up", "spins up", "fire up",
    "plug and play", "plug-and-play", "secret sauce", "no-brainer", "no brainer", "gotcha",
    "gotchas", "tl;dr", "when it comes to", "bear in mind", "one-size-fits-all",
    "one size fits all", "across the board", "up and running", "up to speed",
    "behind the scenes", "cherry-pick", "cherry pick", "cherry-picked", "hand in hand",
    "lion's share", "level playing field", "touch base", "outside the box", "raise the bar",
    "raises the bar", "crystal clear", "on top of that", "in the wild", "the catch",
    "a catch", "here's the thing", "here is the thing", "long story short", "for good",
    "out of thin air", "cut corners", "cuts corners", "the whole nine yards", "home run",
    "slam dunk", "touchdown", "monday morning quarterback", "hail mary", "curveball",
    "curve ball", "step up to the plate", "cover all the bases", "cover your bases",
    "in the same boat", "the ball is in", "back of the envelope", "back-of-the-envelope",
    "sanity check", "happy path", "magic number", "like magic", "automagically",
    "bells and whistles", "nuts and bolts", "bread and butter", "snake oil",
    "food for thought", "take it with", "jump in", "jumps in", "let's dive", "let us dive",
    "buckle up", "spoiler", "fun fact", "pro tip", "heads up", "heads-up",
]

# base verb -> extra forms (irregular). Regular forms are generated.
IRREGULAR = {
    "find": ["found"], "come": ["came"], "get": ["got", "gotten"], "go": ["went", "gone", "goes"],
    "run": ["ran"], "leave": ["left"], "put": [], "bring": ["brought"], "take": ["took", "taken"],
    "make": ["made"], "give": ["gave", "given"], "keep": ["kept"], "break": ["broke", "broken"],
    "set": [], "show": ["shown"],
}
PHRASAL = {
    "figure out": "determine", "find out": "learn, determine", "carry out": "perform",
    "get rid of": "remove", "come up with": "create, propose", "end up": "finally become",
    "turn out": "prove to be", "look into": "examine", "break down": "divide, analyze",
    "set up": "configure, prepare", "point out": "state, show", "rule out": "exclude",
    "go over": "review", "work out": "calculate, solve", "sort out": "solve, organize",
    "run into": "meet", "leave out": "omit", "put off": "delay", "bring up": "mention",
    "deal with": "handle", "get around": "avoid", "give up": "stop", "keep up": "continue",
    "look up": "search for", "show up": "appear", "take on": "accept", "take over": "replace",
    "pick up": "collect, learn", "make up": "form, compose", "go through": "read, pass through",
    "come across": "find", "catch up": "reach", "fall back": "return", "get back": "return",
    "hold on": "wait", "try out": "test", "use up": "consume", "add up": "sum",
    "cut down": "reduce", "back up": "support, copy", "fill in": "complete", "fill out": "complete",
}

UNCOMMON = {
    "utilize": "use", "utilizes": "uses", "utilized": "used", "utilizing": "using",
    "leverage": "use", "leverages": "uses", "leveraged": "used", "leveraging": "using",
    "mitigate": "reduce", "mitigates": "reduces", "mitigated": "reduced",
    "facilitate": "help", "facilitates": "helps", "robust": "reliable, strong",
    "seamless": "without problems", "seamlessly": "without problems",
    "streamline": "simplify", "streamlined": "simplified", "myriad": "many",
    "plethora": "many", "albeit": "although", "whilst": "while",
    "aforementioned": "(name the thing again)", "henceforth": "from now on",
    "nuance": "small difference", "nuances": "small differences", "nuanced": "detailed",
    "delve": "examine", "delves": "examines", "granular": "detailed", "holistic": "complete",
    "paradigm": "model, approach", "synergy": "combined effect", "ubiquitous": "very common",
    "pivotal": "important", "paramount": "most important", "encompass": "include",
    "encompasses": "includes", "commence": "start", "commences": "starts",
    "ascertain": "determine", "elucidate": "explain", "endeavor": "try",
    "tricky": "difficult", "straightforward": "simple", "caveat": "limit, warning",
    "caveats": "limits, warnings", "boilerplate": "standard repeated text",
    "cumbersome": "difficult to use", "daunting": "difficult", "akin": "similar",
    "bolster": "support", "bolsters": "supports", "garner": "get", "glean": "learn",
    "hinder": "slow, block", "hinders": "slows, blocks", "inadvertently": "by accident",
    "juxtapose": "compare", "moot": "not important", "nascent": "new",
    "quintessential": "typical", "salient": "important", "superfluous": "not needed",
    "tantamount": "equal", "underpin": "support", "underpins": "supports",
    "wherein": "in which", "whereby": "by which", "notwithstanding": "in spite of",
    "heretofore": "until now", "vis-a-vis": "compared with", "nitty-gritty": "details",
    "kinda": "rather", "gonna": "going to", "wanna": "want to", "stuff": "things, material",
    "super": "very", "tons": "many", "bunch": "several", "crunch": "calculate",
    "tweak": "change", "tweaks": "changes", "hefty": "large", "pricey": "expensive",
    "snappy": "fast", "blazing": "very fast", "nifty": "useful", "neat": "useful",
    "grok": "understand", "via": "through, by",
}
WORDY = {
    "in order to": "to", "prior to": "before", "subsequent to": "after",
    "in the event that": "if", "with regard to": "about", "with respect to": "about, for",
    "a number of": "several", "due to the fact that": "because",
    "at this point in time": "now", "for the purpose of": "to, for",
    "in spite of the fact that": "although", "is able to": "can",
    "has the ability to": "can", "in terms of": "(name the measure)",
    "as well as": "and", "whether or not": "whether",
}
LATIN = [
    (r"\be\.\s?g\.", 'write "for example"'),
    (r"\bi\.\s?e\.", 'write "that is"'),
    (r"\betc\b\.?", "write the complete list, or \"and other ...\""),
    (r"\band/or\b", 'write "A or B or both"'),
    (r"\bvs\b\.?", 'write "compared with" or "against"'),
    (r"\bper se\b", "remove, or write \"by itself\""),
    (r"\bvice versa\b", "write the reverse statement in full"),
    (r"\bad hoc\b", 'write "for this one case"'),
    (r"\bde facto\b", 'write "in practice"'),
    (r"\bw/o?\b", 'write "with" or "without"'),
    (r"\bapprox\.", 'write "about" or "approximately"'),
    (r"\bN\.?B\.", 'write "Note:"'),
    (r"\ba\.?k\.?a\.?\b", 'write "also named"'),
]
GENERIC_HEADINGS = {
    "introduction", "overview", "background", "analysis", "results", "conclusion",
    "conclusions", "summary", "details", "discussion", "notes", "context", "data",
    "findings", "methodology", "methods", "key takeaways", "takeaways", "final thoughts",
    "wrapping up", "getting started",
}
KNOWN_ABBR = {
    "US", "USD", "UK", "EU", "OK", "ID", "AM", "PM", "UTC", "USA", "EUR", "GBP", "CNY", "JPY",
    "A", "I", "II", "III", "IV", "X", "Y", "Z", "N", "AI",
    # units are not abbreviations
    "KB", "MB", "GB", "TB", "PB", "KG", "KM", "CM", "MM", "MS", "HZ", "KW", "KWH", "PX",
}

NUMERIC_CELL = re.compile(r"^[~≈<>+\-−]?\s?(US\$|[$€£¥])?\s?[\d][\d,. ]*\s?(%|[kKmMbB]|ms|s|px|x|×)?$")
AMBIGUOUS_DATE = re.compile(r"\b\d{1,2}/\d{1,2}/(?:\d{4}|\d{2})\b")
CONTRACTION = re.compile(
    r"\b(?:\w+n['’]t|\w+['’](?:re|ve|ll|d|m)|(?:it|that|there|what|here|let|who|he|she|how|where)['’]s)\b",
    re.IGNORECASE)
NEGATIVE_WORDS = (
    "uncommon unlikely unusual unable unknown unnecessary unimportant unreasonable unclear "
    "unrelated unsafe unstable unexpected unaffected unavailable unchanged unhelpful unlike "
    "impossible improbable inaccurate incorrect insignificant invalid incomplete inconsistent "
    "irrelevant inefficient ineffective infrequent inadequate incapable incompatible "
    "irregular irreversible nonexistent nontrivial non-trivial without"
).split()
DOUBLE_NEG = re.compile(r"\b(?:not|never|no|cannot|can't|n't)\s+(?:be\s+)?(?:"
                        + "|".join(map(re.escape, NEGATIVE_WORDS)) + r")\b", re.IGNORECASE)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⭐⭕️]")
ABBR = re.compile(r"\b[A-Z][A-Z0-9]{1,5}s?\b")
# A new sentence starts with a capital letter, a digit, a quotation mark, a bracket, a
# currency sign, or the placeholder of inline code.
SENT_SPLIT = re.compile(r"(?<=[.!?])[\"”’)]?\s+(?=[A-Z0-9\"“‘($\[])")
EXTERNAL = re.compile(r"""(?:src|href)\s*=\s*["']\s*(?:https?:)?//""", re.IGNORECASE)


def words(text):
    return [w for w in re.split(r"\s+", text.strip()) if re.search(r"[A-Za-z0-9]", w)]


def verb_forms(verb):
    forms = {verb, verb + "s", verb + "ing"}
    if verb.endswith("e"):
        forms |= {verb + "d", verb[:-1] + "ing"}
    elif verb.endswith("y") and verb[-2] not in "aeiou":
        forms |= {verb[:-1] + "ied", verb[:-1] + "ies"}
    else:
        forms |= {verb + "ed"}
        if re.search(r"[^aeiou][aeiou][^aeiouwxy]$", verb):
            forms |= {verb + verb[-1] + "ing", verb + verb[-1] + "ed"}
    forms |= set(IRREGULAR.get(verb, []))
    return forms


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # entries: dict(tag, classes, uid, attrs)
        self.uid = 0
        self.skip_depth = 0
        self.buf = []
        self.buf_ctx = None
        self.buf_line = 0
        self.blocks = []         # dict(text, tag, classes, ancestors, line)
        self.bold_words = 0
        self.total_words = 0
        self.classes_seen = set()
        self.tags_seen = {}
        self.details = []        # dict(uid, in_check, line)
        self.figures = []        # dict(uid, line)
        self.svgs = []           # dict(line, role, label, in_figure, texts)
        self.svg_depth = 0
        self.tables = []         # dict(uid, line, wrapped, max_cols)
        self.title_attrs = []    # (line, tag, text)
        self.images = []         # (line, src)
        self.lang = None
        self.title_text = None
        self.in_title = False
        self.viewport = False
        self.role_tabs = 0
        self.media = []
        self.row_cols = 0
        # Do not name this attribute "offset": the parser uses that name for the column.
        self.line_shift = 0      # lines before the body in a built page
        self.names = set()       # capital-letter names that are not abbreviations
        self.dfns = []           # dict(term, block_index, line, in_short)
        self.cur_dfn = None
        self.cells = {}          # uid of td/th -> (table uid, column index)
        self.ids = {}            # id -> count
        self.anchors = []        # (line, target)
        self.svg_small = []      # (line, font size)
        self.svg_words = []      # dict(text, line), labels inside figures
        self.svg_text_buf = None
        self.part_count = 0      # number of <p class="part"> seen so far
        self.core_targets = []   # ids of the sections on the main path
        self.heading_ids = {}    # uid of a heading element -> id

    def line_no(self):
        return max(1, self.getpos()[0] - self.line_shift)

    def handle_comment(self, data):
        m = re.match(r"\s*names\s*:\s*(.+)", data, re.DOTALL)
        if m:
            self.names.update(n.strip() for n in m.group(1).split(",") if n.strip())

    # ----- helpers
    def ancestors(self):
        return [(e["tag"], e["classes"], e["uid"]) for e in self.stack]

    def has_ancestor_class(self, name):
        return any(name in e["classes"] for e in self.stack)

    def has_ancestor_tag(self, name):
        return any(e["tag"] == name for e in self.stack)

    def flush(self):
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text and self.buf_ctx is not None:
            own = None
            for e in reversed(self.buf_ctx):
                if e[0] in BLOCK_TAGS:
                    own = e
                    break
            self.blocks.append({
                "text": text,
                "tag": own[0] if own else "",
                "classes": own[1] if own else [],
                "uid": own[2] if own else -1,
                "ancestors": self.buf_ctx,
                "line": self.buf_line,
            })
        self.buf = []
        self.buf_ctx = None

    # ----- parser events
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        line = self.line_no()
        self.tags_seen[tag] = self.tags_seen.get(tag, 0) + 1
        self.classes_seen.update(classes)

        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title" and self.svg_depth == 0:
            self.in_title = True
            self.title_text = ""
        if tag == "meta" and (a.get("name") or "").lower() == "viewport":
            self.viewport = True
        if a.get("role") in ("tab", "tablist", "tabpanel"):
            self.role_tabs += 1
        if tag in ("video", "audio"):
            self.media.append((line, tag, "autoplay" in a))
        if tag == "img":
            self.images.append((line, a.get("src") or ""))
        if "title" in a and self.svg_depth == 0 and tag not in ("html", "head", "iframe"):
            if a["title"] and len(a["title"].split()) >= 2:
                self.title_attrs.append((line, tag, a["title"]))

        if a.get("id"):
            self.ids[a["id"]] = self.ids.get(a["id"], 0) + 1
        if tag == "a" and (a.get("href") or "").startswith("#") and len(a["href"]) > 1:
            self.anchors.append((line, a["href"][1:]))
            if any("core" in e["classes"] for e in self.stack):
                self.core_targets.append(a["href"][1:])
        if tag == "dfn" and self.svg_depth == 0:
            self.cur_dfn = []

        if tag == "svg":
            self.svg_depth += 1
            if self.svg_depth == 1:
                vb = re.split(r"[\s,]+", (a.get("viewBox") or "").strip())
                self.svgs.append({
                    "line": line, "role": a.get("role"),
                    "label": a.get("aria-label") or a.get("aria-labelledby"),
                    "in_figure": self.has_ancestor_tag("figure"), "texts": 0,
                    "decorative": a.get("aria-hidden") == "true",
                    "in_scroll": self.has_ancestor_class("fig-scroll"),
                    "vb_width": float(vb[2]) if len(vb) == 4 and re.match(r"^[\d.]+$", vb[2]) else None,
                })
        elif self.svg_depth and tag in ("text", "tspan") and self.svgs:
            if tag == "text":
                self.svgs[-1]["texts"] += 1
                self.svg_text_buf = {"text": "", "line": line}
            size = a.get("font-size") or ""
            m = re.match(r"^([\d.]+)(px)?$", size.strip())
            if m and float(m.group(1)) < 12:
                self.svg_small.append((line, size))

        if tag in BLOCK_TAGS:
            self.flush()
        if tag in VOID_TAGS:
            if tag == "br":
                self.buf.append(" ")
            return

        self.uid += 1
        entry = {"tag": tag, "classes": classes, "uid": self.uid, "attrs": a}
        if "part" in classes:
            self.part_count += 1
        if tag in ("h2", "h3") and a.get("id"):
            self.heading_ids[self.uid] = a["id"]
        if tag == "details":
            self.details.append({"uid": self.uid, "line": line, "summary": "",
                                 "in_check": self.has_ancestor_class("check"),
                                 "optional": "optional" in classes,
                                 "nested": self.has_ancestor_tag("details")})
        if tag == "figure":
            self.figures.append({"uid": self.uid, "line": line, "diagram": "diagram" in classes})
        if tag == "table":
            self.tables.append({"uid": self.uid, "line": line, "max_cols": 0,
                                "wrapped": self.has_ancestor_class("table-wrap")})
        if tag == "tr":
            self.row_cols = 0
        if tag in ("td", "th"):
            if self.tables:
                self.cells[self.uid] = (self.tables[-1]["uid"], self.row_cols)
            self.row_cols += int(a.get("colspan") or 1) if (a.get("colspan") or "1").isdigit() else 1
            if self.tables:
                self.tables[-1]["max_cols"] = max(self.tables[-1]["max_cols"], self.row_cols)
        self.stack.append(entry)
        if tag in SKIP_TAGS:
            self.skip_depth += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "svg" and self.svg_depth:
            self.svg_depth -= 1
        if tag == "text" and self.svg_text_buf is not None:
            text = re.sub(r"\s+", " ", self.svg_text_buf["text"]).strip()
            if text:
                self.svg_words.append({"text": text, "line": self.svg_text_buf["line"],
                                       "tag": "svg", "classes": [], "uid": -1, "ancestors": []})
            self.svg_text_buf = None
        if tag == "dfn" and self.cur_dfn is not None:
            term = re.sub(r"\s+", " ", "".join(self.cur_dfn)).strip()
            if term:
                self.dfns.append({"term": term, "block_index": len(self.blocks),
                                  "part": self.part_count,
                                  "line": self.line_no(),
                                  "in_short": self.has_ancestor_class("bottom-line")})
            self.cur_dfn = None
        if tag in VOID_TAGS:
            return
        if tag in BLOCK_TAGS:
            self.flush()
        # pop to the matching tag, if it exists
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                for e in self.stack[i:]:
                    if e["tag"] in SKIP_TAGS:
                        self.skip_depth -= 1
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.in_title and self.title_text is not None:
            self.title_text += data
            return
        if self.svg_text_buf is not None:
            self.svg_text_buf["text"] += data
        if self.skip_depth > 0:
            return
        if self.cur_dfn is not None:
            self.cur_dfn.append(data)
        if not data.strip():
            self.buf.append(" ")
            return
        if self.buf_ctx is None:
            self.buf_ctx = self.ancestors()
            self.buf_line = self.line_no()
        if any(e["tag"] in ("code", "kbd", "samp", "var") for e in self.stack):
            self.buf.append(" [code] ")
            self.total_words += 1
            return
        if any("quoted" in e["classes"] for e in self.stack):
            # Text copied from a source. It counts as words, but the language rules skip it.
            n = len(words(data))
            self.buf.append(" " + " ".join(["[quoted]"] * max(1, n)) + " ")
            self.total_words += n
            return
        self.buf.append(data)
        n = len(words(data))
        self.total_words += n
        if any(e["tag"] in ("strong", "b") for e in self.stack):
            self.bold_words += n


class Report:
    def __init__(self):
        self.items = []   # (section, level, message, examples)

    def add(self, section, level, message, examples=None):
        self.items.append((section, level, message, examples or []))

    def count(self, level):
        return sum(1 for i in self.items if i[1] == level)

    def render(self, header):
        out = [header, ""]
        section = None
        for sec, level, message, examples in self.items:
            if sec != section:
                out.append(sec.upper())
                section = sec
            out.append(f"  {level:<4}  {message}")
            for ex in examples[:8]:
                out.append(f"          - {ex}")
            if len(examples) > 8:
                out.append(f"          - ... and {len(examples) - 8} more")
        out.append("")
        out.append(f"SUMMARY: {self.count('FAIL')} FAIL, {self.count('WARN')} WARN, "
                   f"{self.count('PASS')} PASS")
        if self.count("FAIL"):
            out.append("Fix every FAIL. Read every WARN and decide.")
        return "\n".join(out)


def short(text, n=110):
    text = text.strip()
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def find_phrases(blocks, phrases):
    hits = []
    for b in blocks:
        low = b["text"].lower().replace("’", "'")
        for ph in phrases:
            if re.search(r"(?<![a-z])" + re.escape(ph) + r"(?![a-z])", low):
                hits.append((ph, b))
    return hits


def measure(page):
    """Count the words of running text: on the whole page, and on the main path.

    Running text is what the reader reads in order. Tables, the contents list, the glossary,
    and the list of sources are reference material, so they do not count. The main path is
    the top of the page plus the sections that the contents list marks with class "core".
    """
    def has_class(b, name):
        return any(name in c for (_, c, _) in b["ancestors"])

    def is_reference(b):
        return (any(t in ("table", "nav") for (t, _, _) in b["ancestors"])
                or any(has_class(b, c) for c in ("glossary", "sources", "contents")))
    running, core, in_core, seen_h2 = 0, 0, True, False
    for b in page.blocks:
        if b["tag"] == "h2" or "part" in b["classes"]:
            seen_h2 = True
            in_core = page.heading_ids.get(b["uid"]) in page.core_targets
        if is_reference(b):
            continue
        n = len(words(b["text"]))
        running += n
        if in_core or not seen_h2:
            core += n
    return running, core


def measure_text(raw):
    page = Page()
    page.feed(raw)
    page.flush()
    return measure(page) + (bool(page.core_targets),)


def check(path, kind, offset=0, source=None):
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as err:
        print(f"Cannot read {path}: {err}", file=sys.stderr)
        sys.exit(2)

    page = Page()
    page.line_shift = offset
    page.feed(raw)
    page.flush()
    rep = Report()
    if source:
        rep.add("text", "INFO", f"Line numbers refer to {source}.")

    def in_class(block, name):
        return any(name in c for (_, c, _) in block["ancestors"])

    def in_tag(block, name):
        return any(t == name for (t, _, _) in block["ancestors"])

    # Text that the language rules apply to. Quoted wrong ideas are excluded from nothing:
    # the reader still has to read them.
    text_blocks = [b for b in page.blocks if not in_tag(b, "code") and not in_class(b, "quoted")
                   and "quoted" not in b["classes"]]
    label_blocks = text_blocks + page.svg_words   # words inside figures follow the same rules

    # ---------------------------------------------------------------- TEXT
    sentences = []
    prose = []
    for b in text_blocks:
        if b["tag"] in ("th", "dt", "caption"):
            continue
        for part in re.split(r"\s[·•|]\s", b["text"]):
            for s in SENT_SPLIT.split(part):
                n = len(words(s))
                if n >= 3:
                    sentences.append((n, s, b["line"]))
                    if b["tag"] in ("p", "li", "dd", "blockquote", "div") and n >= 5:
                        prose.append(n)
    if sentences:
        avg = sum(prose) / len(prose) if prose else 0
        long_ones = sorted([s for s in sentences if s[0] > MAX_WORDS], reverse=True)
        rep.add("text", "INFO", f"{len(sentences)} sentences. Average length in running text: "
                                f"{avg:.1f} words. Limits: average at most {AVG_TARGET}, one "
                                f"sentence at most {MAX_WORDS}. A short sentence is good. "
                                "Do not make sentences longer to reach a number.")
        if long_ones:
            rep.add("text", "FAIL", f"Sentences longer than {MAX_WORDS} words: {len(long_ones)}. "
                                    "Divide each one.",
                    [f"line {ln}, {n} words: \"{short(s)}\"" for n, s, ln in long_ones])
        else:
            rep.add("text", "PASS", f"No sentence is longer than {MAX_WORDS} words.")
        if avg > AVG_TARGET:
            rep.add("text", "WARN", f"Average sentence length {avg:.1f} is above {AVG_TARGET} words. "
                                    "Divide the longest sentences.")
    else:
        rep.add("text", "WARN", "No sentences found in the page.")

    running, core = measure(page)
    minutes = -(-running // 120)
    rep.add("text", "INFO", f"Words of running text: {running:,}. Reading time in minutes: about "
                            f"{minutes} (at 120 words per minute). Tables, contents, glossary, and "
                            f"sources are not counted ({page.total_words - running:,} more words).")
    if page.core_targets:
        level = "WARN" if core > 3000 else "INFO"
        rep.add("text", level, f"Main path: words {core:,}, reading time in minutes about "
                               f"{-(-core // 120)}. The main path is the top of the page plus "
                               f"the {len(set(page.core_targets))} marked sections. Limit: 3,000 "
                               "words.")
    page.total_words = running
    if kind in ("explainer", "report"):
        if page.total_words > 6000:
            rep.add("text", "WARN", "The page has more than 6,000 words of running text. Consider a series of pages, "
                                    "one question per page. If one page is necessary, mark the main "
                                    "path in the contents list (class \"core\") and state its "
                                    "reading time in the header.")
        elif page.total_words > 3500 and "core" not in page.classes_seen:
            rep.add("text", "WARN", "The page has more than 3,500 words of running text and no marked main path. "
                                    "Mark the sections of the main path in the contents list "
                                    "(class \"core\").")

    long_par = []
    for b in text_blocks:
        if b["tag"] == "p":
            n = len(words(b["text"]))
            ns = len([s for s in SENT_SPLIT.split(b["text"]) if len(words(s)) >= 3])
            if n > 150 or ns > 6:
                long_par.append(f"line {b['line']}, {ns} sentences, {n} words: \"{short(b['text'], 70)}\"")
    if long_par:
        rep.add("text", "WARN", "Long paragraphs (more than 6 sentences or 150 words). "
                                "One topic per paragraph.", long_par)

    hits = find_phrases(label_blocks, IDIOMS)
    if hits:
        rep.add("text", "FAIL", f"Idioms or informal expressions: {len(hits)}. Replace each one "
                                "with literal words.",
                [f"line {b['line']}: \"{ph}\" in \"{short(b['text'], 80)}\"" for ph, b in hits])
    else:
        rep.add("text", "PASS", "No idiom from the list was found. (The list is not complete. "
                                "Read the text yourself as well.)")

    ph_hits = []
    for phrase, better in PHRASAL.items():
        verb, rest = phrase.split(" ", 1)
        pattern = r"\b(?:" + "|".join(sorted(map(re.escape, verb_forms(verb)))) + r")\s+" + re.escape(rest) + r"\b"
        for b in text_blocks:
            if re.search(pattern, b["text"], re.IGNORECASE):
                ph_hits.append(f"line {b['line']}: \"{phrase}\" -> {better}. In: \"{short(b['text'], 70)}\"")
    if ph_hits:
        rep.add("text", "WARN", f"Phrasal verbs: {len(ph_hits)}. Use a one-word verb when the "
                                "meaning stays the same.", ph_hits)

    lat_hits = []
    for pattern, advice in LATIN:
        for b in label_blocks:
            m = re.search(pattern, b["text"], re.IGNORECASE if pattern[2].islower() else 0)
            if m:
                lat_hits.append(f"line {b['line']}: \"{m.group(0)}\" -> {advice}")
    if lat_hits:
        rep.add("text", "FAIL", f"Latin or symbol abbreviations: {len(lat_hits)}.", lat_hits)

    unc = []
    for b in text_blocks:
        for w in re.findall(r"[A-Za-z][A-Za-z\-]+", b["text"]):
            if w.lower() in UNCOMMON:
                unc.append(f"line {b['line']}: \"{w}\" -> {UNCOMMON[w.lower()]}")
    for ph, b in find_phrases(text_blocks, WORDY.keys()):
        unc.append(f"line {b['line']}: \"{ph}\" -> {WORDY[ph]}")
    if unc:
        rep.add("text", "WARN", f"Uncommon or wordy expressions: {len(unc)}. Use the common word, "
                                "unless the word is a key term of the topic.", unc)

    con = []
    for b in text_blocks:
        for m in CONTRACTION.finditer(b["text"]):
            con.append(f"line {b['line']}: \"{m.group(0)}\"")
    if con:
        rep.add("text", "WARN", f"Contractions: {len(con)}. Write the full form.", con)

    dn = [f"line {b['line']}: \"{m.group(0)}\"" for b in text_blocks
          for m in DOUBLE_NEG.finditer(b["text"])]
    if dn:
        rep.add("text", "WARN", "Possible double negatives. Write a positive statement.", dn)

    dates = [f"line {b['line']}: \"{m.group(0)}\"" for b in page.blocks
             for m in AMBIGUOUS_DATE.finditer(b["text"])]
    if dates:
        rep.add("text", "FAIL", "Ambiguous dates. Write \"27 September 2026\" or \"2026-09-27\".", dates)

    big = [f"line {b['line']}: \"{short(b['text'], 80)}\"" for b in text_blocks
           if re.search(r"\b(?:billion|trillion)s?\b", b["text"], re.IGNORECASE)
           and not re.search(r"\d{1,3}(?:[,  ]\d{3}){2,}|10\^?\d|10<sup>", b["text"])]
    shown = any(re.search(r"\b(?:billion|trillion)s?\b", b["text"], re.IGNORECASE)
                and re.search(r"\d{1,3}(?:[,  ]\d{3}){2,}", b["text"]) for b in text_blocks)
    if big and not shown:
        rep.add("text", "WARN", "\"billion\" or \"trillion\" without the digits. Show the digits "
                                "once, for example \"2 billion (2,000,000,000)\".", big)

    visible = " ".join(b["text"] for b in text_blocks)
    abbrs = {}
    for m in ABBR.finditer(visible):
        tok = m.group(0)
        base = tok[:-1] if tok.endswith("s") and tok[:-1].isupper() else tok
        if base in KNOWN_ABBR or base.isdigit() or base in page.names or tok in page.names:
            continue
        abbrs[base] = abbrs.get(base, 0) + 1
    undefined = [a for a in sorted(abbrs)
                 if not re.search(r"\(\s*" + re.escape(a) + r"s?\s*[),;]", visible)
                 and not re.search(r"\b" + re.escape(a) + r"s?\s*\(", visible)]
    if undefined:
        rep.add("text", "WARN", f"Abbreviations without the full form next to them: "
                                f"{len(undefined)}. Spell out each one at first use. Ignore an "
                                "abbreviation only if this reader certainly knows it. For a name "
                                "(brand, product, model), add the comment <!-- names: NAME --> to "
                                "the page.",
                [", ".join(undefined)])

    if page.total_words:
        ratio = page.bold_words / page.total_words
        if ratio > 0.12:
            rep.add("text", "WARN", f"{ratio:.0%} of the words are bold. Signals work only when they "
                                    "are used sparingly. Target: below 10%.")

    emo = [f"line {b['line']}: \"{short(b['text'], 60)}\"" for b in page.blocks if EMOJI.search(b["text"])]
    if emo:
        rep.add("text", "WARN", "Emoji or symbol characters. Remove decoration. A symbol that "
                                "carries meaning needs a text label.", emo)

    per_part = {}
    for d in page.dfns:
        per_part[d["part"]] = per_part.get(d["part"], 0) + 1
    crowded = {k: v for k, v in per_part.items() if v > 15}
    if crowded and kind == "explainer":
        where = ", ".join((f"part {k}: {v} terms" if page.part_count else f"{v} terms")
                          for k, v in sorted(crowded.items()))
        rep.add("text", "WARN", f"Too many defined terms ({where}). One part can teach about 12 new "
                                "terms. Remove terms that the explanation does not need, or divide "
                                "the content into more parts.")
    elif page.dfns:
        rep.add("text", "INFO", f"Defined terms: {len(page.dfns)}"
                                + (f", in {page.part_count} parts." if page.part_count else "."))
    early = []
    for d in page.dfns:
        if d["in_short"]:
            continue
        pat = re.compile(r"(?<![A-Za-z])" + re.escape(d["term"].lower()) + r"(?:s|es)?(?![A-Za-z])")
        for b in page.blocks[:d["block_index"]]:
            if b["tag"] in ("h1", "h2", "h3", "summary") or in_tag(b, "nav") or in_tag(b, "code"):
                continue
            if any(in_class(b, c) for c in ("bottom-line", "assume", "meta", "contents")):
                continue
            if pat.search(b["text"].lower()):
                early.append(f"\"{d['term']}\" is used at line {b['line']}, but defined at line "
                             f"{d['line']}")
                break
    if early:
        rep.add("text", "WARN", "Terms used before their definition. Move the definition to the "
                                "first use. (The short answer and the headings are exempt.)", early)

    if kind == "product":
        return rep

    # ----------------------------------------------------------- STRUCTURE
    h1 = [b for b in page.blocks if b["tag"] == "h1"]
    if len(h1) != 1:
        rep.add("structure", "FAIL", f"The page has {len(h1)} <h1> elements. It needs exactly 1.")
    elif len(words(h1[0]["text"])) < 4:
        rep.add("structure", "WARN", f"The <h1> \"{h1[0]['text']}\" is a topic, not a question or a "
                                     "claim.")

    generic = [f"line {b['line']}: \"{b['text']}\"" for b in page.blocks
               if b["tag"] in ("h2", "h3")
               and re.sub(r"^[\d.\s]+", "", b["text"]).strip().lower().rstrip(":") in GENERIC_HEADINGS]
    if generic:
        rep.add("structure", "WARN", "Generic headings. Write a statement that gives the main point "
                                     "of the section.", generic)

    def need(cls, level, message):
        if cls in page.classes_seen:
            rep.add("structure", "PASS", f"Found: {message} (class \"{cls}\").")
        else:
            rep.add("structure", level, f"Missing: {message} (class \"{cls}\"). See assets/example-body.html.")

    if kind in ("explainer", "report"):
        need("bottom-line", "FAIL", "the short answer box at the top")
        need("sources", "FAIL", "the list of sources with confidence labels")
        need("limits", "WARN", "the limits box")
    if kind == "explainer":
        need("example", "FAIL", "a worked example")
        need("check", "FAIL", "self-check questions")
        if "check" in page.classes_seen and not any(d["in_check"] for d in page.details):
            rep.add("structure", "FAIL", "The self-check has no hidden answers. Put each answer in "
                                         "<details>.")
        if "mistake" not in page.classes_seen:
            rep.add("structure", "INFO", "No \"common wrong idea\" box. Add one if a common wrong "
                                         "belief about this topic exists.")
        if "compare" not in page.classes_seen:
            rep.add("structure", "INFO", "No side-by-side comparison. Two cases side by side help "
                                         "the reader (d = 0.50).")
        steps = sum(1 for b in page.blocks if b["tag"] == "li"
                    and any(t == "ol" and "steps" in c for (t, c, _) in b["ancestors"]))
        if "steps" in page.classes_seen and "why" not in page.classes_seen:
            rep.add("structure", "WARN", f"{steps} numbered steps, but no step has a reason "
                                         "(class \"why\").")

    if "dfn" in page.tags_seen and "glossary" not in page.classes_seen and kind == "explainer":
        rep.add("structure", "WARN", "Key terms are defined in the text, but the page has no "
                                     "glossary (class \"glossary\").")
    if kind == "explainer" and "dfn" not in page.tags_seen:
        rep.add("structure", "WARN", "No <dfn> element. Define each key term in the sentence where "
                                     "it first appears.")

    # ----------------------------------------------------- HIDDEN CONTENT
    outside = [d for d in page.details if not d["in_check"] and not d["optional"]]
    optional = [d for d in page.details if d["optional"]]
    if optional:
        rep.add("hidden content", "INFO", f"{len(optional)} blocks of optional depth "
                                          "(details with class \"optional\").")
    for d in page.details:
        for b in page.blocks:
            if b["tag"] == "summary" and any(u == d["uid"] for (_, _, u) in b["ancestors"]):
                d["summary"] = b["text"]
                break
    if outside:
        rep.add("hidden content", "WARN", f"{len(outside)} <details> outside the self-check and "
                                          "without class \"optional\". If the content is "
                                          "essential, make it visible. If it is optional depth, "
                                          "add class \"optional\".",
                [f"line {d['line']}: \"{short(d['summary'], 70)}\"" for d in outside])
    nested = [d for d in page.details if d["nested"]]
    if nested:
        rep.add("hidden content", "FAIL", f"{len(nested)} <details> inside another <details>. "
                                          "Hidden content may have one level only.",
                [f"line {d['line']}" for d in nested])
    if page.title_attrs:
        rep.add("hidden content", "WARN", "\"title\" attributes create hover text. Most readers never "
                                          "see hover text. Put the content in visible text.",
                [f"line {ln}: <{tag} title=\"{short(t, 60)}\">" for ln, tag, t in page.title_attrs])
    risky = sorted(c for c in page.classes_seen
                   if re.search(r"(^|[-_])(tabs?|tab-?panel|carousel|accordion|tooltip|popover|slider|"
                                r"collaps\w*)($|[-_])", c, re.IGNORECASE))
    if risky or page.role_tabs:
        rep.add("hidden content", "WARN", "The page seems to use tabs, a carousel, an accordion, or "
                                          "tooltips. Essential content must be visible without a "
                                          "click.", [", ".join(risky)] if risky else [])
    styles = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", raw, re.DOTALL | re.IGNORECASE))
    if re.search(r":hover[^{}]*\{[^}]*(?:display|visibility|opacity)\s*:", styles):
        rep.add("hidden content", "WARN", "A CSS :hover rule changes display, visibility, or opacity. "
                                          "Do not show content only on hover.")
    if not (outside or page.title_attrs or risky or page.role_tabs):
        rep.add("hidden content", "PASS", "No essential content seems to be hidden.")

    # ------------------------------------------------------------ FIGURES
    for f in page.figures:
        titles = [b for b in page.blocks if "fig-title" in b["classes"]
                  and any(u == f["uid"] for (_, _, u) in b["ancestors"])]
        if not titles:
            rep.add("figures", "WARN", f"line {f['line']}: the figure has no title "
                                       "(class \"fig-title\").")
            continue
        t = titles[0]["text"]
        if len(words(t)) < 5:
            rep.add("figures", "WARN", f"line {f['line']}: the figure title \"{short(t, 70)}\" is a "
                                       "topic. Write a sentence that states the main point.")
        elif not f["diagram"] and not re.search(r"\d", t):
            rep.add("figures", "WARN", f"line {f['line']}: the title of a chart \"{short(t, 70)}\" "
                                       "must state the finding with its number. If this figure is a "
                                       "diagram and not a chart, add class \"diagram\" to <figure>.")
        reads = [b for b in page.blocks if "fig-read" in b["classes"]
                 and any(u == f["uid"] for (_, _, u) in b["ancestors"])]
        if not reads:
            rep.add("figures", "WARN", f"line {f['line']}: the figure has no \"How to read this\" "
                                       "line (class \"fig-read\").")
    for s in page.svgs:
        if s["decorative"]:
            continue
        if s["role"] != "img" or not s["label"]:
            rep.add("figures", "WARN", f"line {s['line']}: the <svg> needs role=\"img\" and an "
                                       "aria-label that states the finding.")
        if s["texts"] == 0:
            rep.add("figures", "WARN", f"line {s['line']}: the <svg> has no <text> labels. Put the "
                                       "labels inside the figure.")
        if s["in_figure"] and not s["in_scroll"]:
            rep.add("figures", "WARN", f"line {s['line']}: put the <svg> inside "
                                       "<div class=\"fig-scroll\">. Without it, the labels become "
                                       "too small on a phone.")
        if s["vb_width"] and s["vb_width"] > 720:
            rep.add("figures", "WARN", f"line {s['line']}: the viewBox is {s['vb_width']:.0f} wide. "
                                       "Use a width of 560 to 720, so that a label of 13 px stays "
                                       "readable in the text column.")
        if not s["in_figure"]:
            rep.add("figures", "INFO", f"line {s['line']}: the <svg> is not inside a <figure> with a "
                                       "title.")
    if page.svg_small:
        rep.add("figures", "WARN", f"{len(page.svg_small)} labels inside figures are smaller than "
                                   "12 px. Use 13 px or more.",
                [f"line {ln}: font-size {size}" for ln, size in page.svg_small])
    if any(re.search(r"(^|[-_])legend($|[-_])", c) for c in page.classes_seen):
        rep.add("figures", "WARN", "The page has a legend. Label each series directly, at the end of "
                                   "the line or on the bar.")
    if page.figures and not any(i[0] == "figures" and i[1] in ("WARN", "FAIL") for i in rep.items):
        rep.add("figures", "PASS", f"Figures with a finding title and a reading line: "
                                   f"{len(page.figures)}.")

    # ------------------------------------------------------------- TABLES
    columns = {}
    for b in page.blocks:
        if b["tag"] == "td" and b["uid"] in page.cells:
            col = columns.setdefault(page.cells[b["uid"]], [0, 0])
            col[0] += 1
            col[1] += 1 if NUMERIC_CELL.match(b["text"]) else 0
    unaligned = [b for b in page.blocks if b["tag"] == "td" and NUMERIC_CELL.match(b["text"])
                 and "num" not in b["classes"] and b["uid"] in page.cells
                 and columns[page.cells[b["uid"]]][1] / columns[page.cells[b["uid"]]][0] >= 0.6]
    if unaligned:
        rep.add("tables", "WARN", f"Number cells without class \"num\": {len(unaligned)}. Numbers "
                                  "must be right-aligned.",
                [f"line {b['line']}: \"{b['text']}\"" for b in unaligned])
    wide = [t for t in page.tables if not t["wrapped"]]
    if wide:
        rep.add("tables", "WARN", "Put every table inside <div class=\"table-wrap\">. Without it, a "
                                  "wide table breaks the page on a narrow screen.",
                [f"line {t['line']}: {t['max_cols']} columns" for t in wide])
    if page.tables:
        rep.add("tables", "INFO", "The checker cannot see if a table is wider than the text column. "
                                  "Look at the pictures from render_page.py.")
    if page.tables and not unaligned and not wide:
        rep.add("tables", "PASS", f"Tables: {len(page.tables)}. Numbers are aligned, and each "
                                  "table has a scroll frame.")

    # ---------------------------------------------------------- TECHNICAL
    ext = [short(m.group(0), 60) for m in EXTERNAL.finditer(raw)
           if not re.search(r"<a\s[^>]*$", raw[max(0, m.start() - 300):m.start()])]
    if re.search(r"@import\s", styles) or re.search(r"url\(\s*[\"']?(?:https?:)?//", styles):
        ext.append("@import or url(...) in CSS")
    if ext:
        rep.add("technical", "FAIL", f"External resources: {len(ext)}. The page must work without "
                                     "a network. Put everything inline.", ext)
    else:
        rep.add("technical", "PASS", "No external resources.")
    dup = sorted(i for i, n in page.ids.items() if n > 1)
    if dup:
        rep.add("technical", "FAIL", "The same id is used more than one time.", [", ".join(dup)])
    broken = [f"line {ln}: #{t}" for ln, t in page.anchors if t not in page.ids]
    if broken:
        rep.add("technical", "FAIL", "Links to a place that does not exist on the page.", broken)
    files = [f"line {ln}: {short(src, 60)}" for ln, src in page.images
             if src and not src.startswith("data:")]
    if files:
        rep.add("technical", "WARN", "Images from files. Use inline SVG or a data URI, so the page "
                                     "is one file.", files)
    if not page.lang:
        rep.add("technical", "FAIL", "<html> has no lang attribute. Write <html lang=\"en\">.")
    if not page.viewport:
        rep.add("technical", "FAIL", "The viewport meta element is missing. The page will not fit a "
                                     "phone.")
    tw = len(words(page.title_text or ""))
    if tw == 0:
        rep.add("technical", "FAIL", "The <title> is missing.")
    elif not 2 <= tw <= 4:
        rep.add("technical", "WARN", f"The <title> has {tw} words. Use a name of 2 to 4 words. The "
                                     "long question goes in <h1>.")
    if re.search(r"text-align\s*:\s*justify", raw, re.IGNORECASE):
        rep.add("technical", "FAIL", "Justified text. Use left-aligned text.")
    if re.search(r"animation[^;{}]*\binfinite\b", styles) or any(a for _, _, a in page.media):
        rep.add("technical", "WARN", "Automatic animation or autoplay. Show a process as numbered "
                                     "static frames.")
    if "prefers-color-scheme" not in styles:
        rep.add("technical", "WARN", "No dark theme. Build the page with build_page.py.")
    if "beforeprint" not in raw and page.details:
        rep.add("technical", "WARN", "Hidden answers will not print. Build the page with "
                                     "build_page.py.")
    return rep


def main():
    ap = argparse.ArgumentParser(description="Check an HTML page against the explainer-html rules.")
    ap.add_argument("path", nargs="?")
    ap.add_argument("--kind", choices=["explainer", "report", "dashboard", "product"],
                    default="explainer")
    ap.add_argument("--line-offset", type=int, default=0, help=argparse.SUPPRESS)
    ap.add_argument("--source", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--words", action="store_true", help="print the word lists and stop")
    args = ap.parse_args()
    if args.words:
        print("IDIOMS AND INFORMAL EXPRESSIONS (FAIL)\n  " + ", ".join(IDIOMS))
        print("\nLATIN AND SYMBOL ABBREVIATIONS (FAIL)\n  e.g., i.e., etc., and/or, vs., per se, "
              "vice versa, ad hoc, de facto, w/, w/o, approx., N.B., a.k.a.")
        print("\nPHRASAL VERBS (WARN)\n  " + ", ".join(f"{k} -> {v}" for k, v in PHRASAL.items()))
        print("\nUNCOMMON WORDS (WARN)\n  " + ", ".join(f"{k} -> {v}" for k, v in UNCOMMON.items()))
        print("\nWORDY EXPRESSIONS (WARN)\n  " + ", ".join(f"{k} -> {v}" for k, v in WORDY.items()))
        return
    if not args.path:
        ap.error("the path of the page is required")
    rep = check(args.path, args.kind, args.line_offset, args.source)
    print(rep.render(f"explainer-html check: {args.path}  (kind: {args.kind})"))
    sys.exit(1 if rep.count("FAIL") else 0)


if __name__ == "__main__":
    main()
