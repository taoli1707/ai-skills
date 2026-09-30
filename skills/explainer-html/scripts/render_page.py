#!/usr/bin/env python3
"""Make pictures of a page, so that you can look at the layout and at every figure.

Usage:
    python3 render_page.py page.html --out-dir shots/ [--full] [--only figure-2]

Output (PNG files in the output folder):
    top-light.png, top-dark.png     the first screen of the page, 1100 px wide
    phone-top.png                   the first screen at a width of 320 px
    figure-N-light.png, figure-N-dark.png, figure-N-phone.png   each <figure> alone
    table-N.png, table-N-phone.png  each table alone, in the width of the text column
    code-N.png                      each code block alone
    full-NN.png                     with --full: the whole page in slices of 1400 px

With --only NAME the script writes only the pictures whose name starts with NAME,
for example --only figure-2 or --only table. Use it after you changed one figure.

Then open the PNG files with your image reading tool. Look for: labels that overlap,
text that is cut, text that is too small, and colours that are hard to see.

The script needs Google Chrome, Chromium, Microsoft Edge, or Brave. If no browser is
found, the script says so and stops with exit code 3. In that case, tell the user that
the layout was not checked visually.
"""
import argparse
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge",
]
TIMEOUT = 45
PHONE = 320      # the narrowest width that the page must support


def find_browser():
    for c in CANDIDATES:
        if os.path.isabs(c):
            if os.path.exists(c):
                return c
        else:
            found = shutil.which(c)
            if found:
                return found
    return None


def shot(browser, profile, url, out, width, height):
    cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
           "--no-default-browser-check", f"--user-data-dir={profile}",
           "--allow-file-access-from-files", f"--window-size={width},{height}",
           f"--screenshot={out}", url]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                            start_new_session=True)
    try:
        # The browser often stays alive after it has written the picture. So do not wait
        # for the process to end. Wait until the file exists and its size is stable.
        waited, last, stable = 0.0, -1, 0
        while waited < TIMEOUT and proc.poll() is None:
            time.sleep(0.25)
            waited += 0.25
            size = os.path.getsize(out) if os.path.exists(out) else 0
            stable = stable + 1 if size > 0 and size == last else 0
            last = size
            if stable >= 4:
                break
    finally:
        # The browser sometimes stays alive after the picture is written. Stop our own
        # process group only. The normal browser of the user is a different group.
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
    return os.path.exists(out) and os.path.getsize(out) > 0


def themed(html, theme):
    return re.sub(r"<html\b([^>]*)>",
                  lambda m: "<html" + re.sub(r'\sdata-theme="[^"]*"', "", m.group(1))
                  + f' data-theme="{theme}">', html, count=1)


def frame(src, width, height):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>body{{margin:0;'
            f'background:#777}}iframe{{width:{width}px;height:{height}px;border:0;display:block}}'
            f'</style></head><body><iframe src="{src}"></iframe></body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--only", default=None, help="write only pictures whose name starts with this")
    ap.add_argument("--full", action="store_true",
                    help="also write the whole page in slices (full-01.png, full-02.png, ...)")
    args = ap.parse_args()

    browser = find_browser()
    if not browser:
        print("No browser found (Chrome, Chromium, Edge, or Brave). The layout was not checked.")
        sys.exit(3)

    with open(args.page, encoding="utf-8") as fh:
        html = fh.read()
    os.makedirs(args.out_dir, exist_ok=True)
    out_dir = os.path.abspath(args.out_dir)
    work = tempfile.mkdtemp(prefix="render-page-")
    profile = os.path.join(work, "profile")
    made, failed = [], []

    def write(name, text):
        path = os.path.join(work, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return "file://" + path

    def take(name, url, width, height):
        if args.only and not name.startswith(args.only):
            return
        out = os.path.join(out_dir, name)
        if os.path.exists(out):
            os.remove(out)
        (made if shot(browser, profile, url, out, width, height) else failed).append(name)

    try:
        for theme in ("light", "dark"):
            take(f"top-{theme}.png", write(f"page-{theme}.html", themed(html, theme)), 1100, 1500)
        write("page-light.html", themed(html, "light"))
        take("phone-top.png", write("phone.html", frame("page-light.html", PHONE, 1500)), PHONE, 1500)

        head = re.search(r"<head\b.*?</head>", html, re.DOTALL | re.IGNORECASE)
        head = head.group(0) if head else "<head><meta charset='utf-8'></head>"
        # Styles that the writer added at the end of the body belong to every picture too.
        rest = html[html.lower().find("</head>"):] if "</head>" in html.lower() else html
        extra = "".join(re.findall(r"<style\b.*?</style>", rest, re.DOTALL | re.IGNORECASE))
        head = head.replace("</head>", extra + "</head>")
        # The scripts of the page run in each picture too (for example the script that marks
        # a table that is wider than its frame).
        scripts = "".join(re.findall(r"<script\b.*?</script>", rest, re.DOTALL | re.IGNORECASE))
        figures = re.findall(r"<figure\b.*?</figure>", html, re.DOTALL | re.IGNORECASE)
        for i, fig in enumerate(figures, 1):
            for theme in ("light", "dark"):
                doc = (f'<!doctype html><html lang="en" data-theme="{theme}">{head}'
                       f'<body><main style="padding-top:16px;padding-bottom:16px">{fig}</main>'
                       f'{scripts}</body></html>')
                url = write(f"figure-{i}-{theme}.html", doc)
                take(f"figure-{i}-{theme}.png", url, 800, 760)
            take(f"figure-{i}-phone.png",
                 write(f"figure-{i}-phone.html", frame(f"figure-{i}-light.html", PHONE, 760)),
                 PHONE, 760)

        def alone(name, fragment, height):
            doc = (f'<!doctype html><html lang="en" data-theme="light">{head}'
                   f'<body><main style="padding-top:16px;padding-bottom:16px">{fragment}</main>'
                   f'{scripts}</body></html>')
            write(f"{name}.html", doc)
            take(f"{name}.png", "file://" + os.path.join(work, f"{name}.html"), 800, height)
            return f"{name}.html"

        tables = re.findall(r'<div class="table-wrap">.*?</table>\s*</div>(?:\s*<p class="table-read">.*?</p>)?',
                            html, re.DOTALL | re.IGNORECASE)
        for i, tab in enumerate(tables, 1):
            rows = len(re.findall(r"<tr\b", tab, re.IGNORECASE))
            src = alone(f"table-{i}", tab, min(1600, 220 + 56 * rows))
            take(f"table-{i}-phone.png", write(f"table-{i}-phone.html", frame(src, PHONE, 760)), PHONE, 760)
        blocks = re.findall(r"<pre\b.*?</pre>", html, re.DOTALL | re.IGNORECASE)
        for i, pre in enumerate(blocks, 1):
            alone(f"code-{i}", pre, min(1400, 120 + 28 * (pre.count("\n") + 1)))

        if args.full:
            # A slice is a window on a very tall frame. The slice after the end of the page
            # is empty, and an empty slice always has the same bytes. So stop at that slice.
            slice_h, max_slices = 1400, 40
            tall = slice_h * (max_slices + 2)
            def slice_url(n):
                doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;'
                       f'overflow:hidden;background:#fff}}iframe{{width:1100px;height:{tall}px;border:0;'
                       f'display:block;margin-top:-{n * slice_h}px}}</style></head><body>'
                       f'<iframe src="page-light.html"></iframe></body></html>')
                return write(f"slice-{n}.html", doc)
            ref = os.path.join(work, "empty.png")
            if not args.only or "full".startswith(args.only) or args.only.startswith("full"):
                shot(browser, profile, slice_url(max_slices + 1), ref, 1100, slice_h)
            empty = open(ref, "rb").read() if os.path.exists(ref) else b""
            for n in range(max_slices if os.path.exists(ref) else 0):
                name = f"full-{n + 1:02d}.png"
                take(name, slice_url(n), 1100, slice_h)
                path = os.path.join(out_dir, name)
                if name in made and open(path, "rb").read() == empty:
                    os.remove(path)
                    made.remove(name)
                    break
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print(f"Pictures written to {out_dir}:")
    for name in made:
        print(f"  {name}")
    for name in failed:
        print(f"  FAILED: {name}")
    print(f"\n{len(figures)} figures, {len(tables)} tables, {len(blocks)} code blocks. "
          "Now open each picture and look at it.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
