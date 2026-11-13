#!/usr/bin/env python3
"""Regenerate index.html (the self-contained GitHub Pages bundle) from BMLS Lab.html.

Usage:  python3 build_index.py

What it copies from BMLS Lab.html into index.html:
- the <script type="text/babel"> app code;
- the whole <head> (styles, @font-face rules, meta tags), keeping the bundle's
  embedded copies of React / ReactDOM / Babel in place of the CDN <script> tags;
- the block between <!-- shell-head:start --> and <!-- shell-head:end -->
  (favicons, social-preview tags, font preloads) into the small loader page that
  browsers see first, plus the <title> and the loading-screen thumbnail;
- every file listed in a <meta name="ext-resource-dependency" ...> tag
  (e.g. uploads/saba-sohrabi.jpg), embedded so it is available as
  window.__resources[id]. Resources whose local file is missing (e.g. the
  original profile photo) keep whatever is already in the bundle.

Embedded files that nothing references any more are dropped from the bundle.
Files referenced by plain relative URLs (fonts/, uploads/favicon-32.png,
files/CV_EU.pdf) are NOT embedded: commit them alongside index.html.
"""
import base64, json, mimetypes, os, re, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "BMLS Lab.html"), os.path.join(HERE, "index.html")
mimetypes.add_type("image/svg+xml", ".svg")
UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

src = open(SRC, encoding="utf-8").read()
s = open(OUT, encoding="utf-8").read()

def span(text, tag):
    i = text.find(tag); assert i >= 0, tag
    i = text.find(">", i) + 1
    return i, text.find("</script>", i)

def head(text):
    i = text.index("<head"); i = text.index(">", i) + 1
    return i, text.index("</head>", i)

ti, tj = span(s, '<script type="__bundler/template">')
mi, mj = span(s, '<script type="__bundler/manifest">')
ei, ej = span(s, '<script type="__bundler/ext_resources">')
tpl = json.loads(s[ti:tj]); man = json.loads(s[mi:mj]); ext = json.loads(s[ei:ej])

# ── app code ──────────────────────────────────────────────
a, b = span(tpl, '<script type="text/babel">'), span(src, '<script type="text/babel">')
tpl = tpl[:a[0]] + src[b[0]:b[1]] + tpl[a[1]:]

# ── <head> ────────────────────────────────────────────────
hi, hj = head(tpl)
embedded = re.findall(r'<script src="' + UUID + r'"[^>]*></script>', tpl[hi:hj])
si, sj = head(src)
h = src[si:sj]
h = re.sub(r'\s*<meta name="ext-resource-dependency"[^>]*>', "", h)
h = re.sub(r'\s*<template id="__bundler_thumbnail".*?</template>', "", h, flags=re.S)
cdn = re.findall(r'<script src="https?://[^"]+"[^>]*></script>', h)
assert len(cdn) == len(embedded), f"{len(cdn)} CDN scripts in BMLS Lab.html but {len(embedded)} embedded in index.html"
for k, tag in enumerate(cdn):          # same order: React, ReactDOM, Babel
    h = h.replace(tag, embedded[k], 1)
tpl = tpl[:hi] + h + "\n" + tpl[hj:]

# ── resources ─────────────────────────────────────────────
by_id = {e["id"]: e for e in ext}
for path, rid in re.findall(r'<meta name="ext-resource-dependency" content="([^"]+)" data-resource-id="([^"]+)"', src):
    fp = os.path.join(HERE, path)
    if not os.path.exists(fp):
        if rid not in by_id: print(f"warning: {path} missing and not in bundle")
        continue
    mime = mimetypes.guess_type(fp)[0] or "application/octet-stream"
    entry = {"mime": mime, "compressed": False, "data": base64.b64encode(open(fp, "rb").read()).decode()}
    if rid in by_id:
        man[by_id[rid]["uuid"]] = entry
    else:
        u = str(uuid.uuid4()); man[u] = entry
        e = {"id": rid, "uuid": u}; ext.append(e); by_id[rid] = e
    print(f"embedded {rid:16s} <- {path}")

# drop embedded files nothing refers to any more (e.g. fonts from an older design)
used = set(re.findall(UUID, tpl)) | {e["uuid"] for e in ext}
dropped = [u for u in man if u not in used]
for u in dropped: del man[u]
if dropped: print(f"dropped {len(dropped)} unused embedded file(s)")

parts = [(ti, tj, "\n" + json.dumps(tpl).replace("</", "<\\u002F") + "\n  "),
         (mi, mj, "\n" + json.dumps(man, separators=(",", ":")) + "\n  "),
         (ei, ej, "\n" + json.dumps(ext, separators=(",", ":")) + "\n  ")]
for i, j, new in sorted(parts, reverse=True):
    s = s[:i] + new + s[j:]

# ── loader page (what the browser sees before the bundle unpacks) ──
li, lj = head(s)
shell = s[li:lj]
title = re.search(r"<title>.*?</title>", src, re.S).group(0)
shell = re.sub(r"<title>.*?</title>", lambda m: title, shell, count=1, flags=re.S)
block = re.search(r"[ \t]*<!-- shell-head:start.*?<!-- shell-head:end -->\n?", src, re.S)
shell = re.sub(r"[ \t]*<!-- shell-head:start.*?<!-- shell-head:end -->\n?", "", shell, flags=re.S)
if block:
    k = shell.index("</title>") + len("</title>\n")
    shell = shell[:k] + block.group(0) + shell[k:]
bg = re.search(r'<template id="__bundler_thumbnail" data-bg-color="([^"]+)"', src)
if bg:
    shell = re.sub(r"background: #[0-9A-Fa-f]{6};", f"background: {bg.group(1)};", shell)
s = s[:li] + shell + s[lj:]

thumb = re.search(r'<template id="__bundler_thumbnail"[^>]*>\s*(.*?)\s*</template>', src, re.S)
if thumb:
    d0 = s.index('<div id="__bundler_thumbnail">') + len('<div id="__bundler_thumbnail">')
    d1 = s.index("</div>", s.index("</svg>", d0))
    s = s[:d0] + "\n    " + thumb.group(1) + "\n  " + s[d1:]

open(OUT, "w", encoding="utf-8").write(s)
print("wrote index.html", os.path.getsize(OUT), "bytes")
