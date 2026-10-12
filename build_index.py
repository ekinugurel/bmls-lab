#!/usr/bin/env python3
"""Regenerate index.html (the self-contained GitHub Pages bundle) from BMLS Lab.html.

Usage:  python3 build_index.py

- Copies the <script type="text/babel"> app code from BMLS Lab.html into the bundle.
- Embeds every file listed in a <meta name="ext-resource-dependency" ...> tag
  (e.g. uploads/saba-sohrabi.jpg) so it is available as window.__resources[id].
  Resources whose local file is missing (e.g. the original profile photo) keep
  whatever is already in the bundle.
"""
import base64, json, mimetypes, os, re, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "BMLS Lab.html"), os.path.join(HERE, "index.html")
mimetypes.add_type("image/svg+xml", ".svg")

src = open(SRC, encoding="utf-8").read()
s = open(OUT, encoding="utf-8").read()

def span(text, tag):
    i = text.find(tag); assert i >= 0, tag
    i = text.find(">", i) + 1
    return i, text.find("</script>", i)

def babel(text):
    return span(text, '<script type="text/babel">')

ti, tj = span(s, '<script type="__bundler/template">')
mi, mj = span(s, '<script type="__bundler/manifest">')
ei, ej = span(s, '<script type="__bundler/ext_resources">')
tpl = json.loads(s[ti:tj]); man = json.loads(s[mi:mj]); ext = json.loads(s[ei:ej])

# app code
a, b = babel(tpl), babel(src)
tpl = tpl[:a[0]] + src[b[0]:b[1]] + tpl[a[1]:]

# resources
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

parts = [(ti, tj, "\n" + json.dumps(tpl).replace("</", "<\\u002F") + "\n  "),
         (mi, mj, "\n" + json.dumps(man, separators=(",", ":")) + "\n  "),
         (ei, ej, "\n" + json.dumps(ext, separators=(",", ":")) + "\n  ")]
for i, j, new in sorted(parts, reverse=True):
    s = s[:i] + new + s[j:]
open(OUT, "w", encoding="utf-8").write(s)
print("wrote index.html", os.path.getsize(OUT), "bytes")
