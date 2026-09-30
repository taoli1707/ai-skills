#!/usr/bin/env python3
"""Build a complete page from a body fragment, then run the checker.

Usage:
    python3 build_page.py body.html --title "Compound Interest Explained" --out page.html
           [--kind explainer|report|dashboard] [--no-check]

You write only the content that goes inside <main>. This script adds the document head,
the standard styles (assets/page.css), and the standard script (assets/page.js). So the
styles are always identical, and you do not need to read or copy them.

The body fragment may contain its own <style> or <script> elements, for example for a
calculator. Put them at the end of the fragment.

Placeholders that the script fills in the body:
    {{minutes}}             reading time of the page, in minutes
    {{main_path_minutes}}   reading time of the main path, in minutes
    {{today}}               the date of today, for example 2026-09-27
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("body", help="file with the content for <main>")
    ap.add_argument("--title", required=True, help="page name of 2 to 4 words, for <title>")
    ap.add_argument("--out", required=True, help="path of the page to write")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--kind", default="explainer",
                    choices=["explainer", "report", "dashboard", "product"])
    ap.add_argument("--no-check", action="store_true", help="do not run the checker")
    args = ap.parse_args()

    with open(args.body, encoding="utf-8") as fh:
        raw_body = fh.read()
    body = raw_body.strip()
    lead = raw_body[: len(raw_body) - len(raw_body.lstrip())].count("\n")
    if re.search(r"<(?:!doctype|html|head|body)\b", body, re.IGNORECASE):
        sys.exit("The body file must contain only the content for <main>. "
                 "Remove <!doctype>, <html>, <head>, and <body>.")
    body = re.sub(r"^\s*<main[^>]*>|</main>\s*$", "", body, flags=re.IGNORECASE).strip()

    with open(os.path.join(ASSETS, "page.css"), encoding="utf-8") as fh:
        css = fh.read().rstrip()
    with open(os.path.join(ASSETS, "page.js"), encoding="utf-8") as fh:
        js = fh.read().rstrip()
    title = args.title.replace("&", "&amp;").replace("<", "&lt;")

    # Fill the placeholders. A placeholder is one word, and its value is one word,
    # so the word count does not change when the values go in.
    sys.path.insert(0, HERE)
    import check_page
    running, core, has_core = check_page.measure_text(f"<main>{body}</main>")
    body = (body.replace("{{minutes}}", str(-(-running // 120)))
                .replace("{{main_path_minutes}}", str(-(-core // 120)))
                .replace("{{today}}", datetime.date.today().isoformat()))

    page = f"""<!doctype html>
<html lang="{args.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<main>

{body}

</main>
<script>
{js}
</script>
</body>
</html>
"""
    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(f"Built {args.out} ({len(page.encode('utf-8')):,} bytes).\n")

    if args.no_check:
        return
    # The checker reports the line numbers of the body file, not of the built page.
    offset = page[: page.index("<main>")].count("\n") + 2 - lead
    result = subprocess.run([sys.executable, os.path.join(HERE, "check_page.py"), args.out,
                             "--kind", args.kind, "--line-offset", str(offset),
                             "--source", os.path.basename(args.body)])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
