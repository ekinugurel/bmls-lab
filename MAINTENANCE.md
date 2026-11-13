# BMLS Lab Website — Maintenance Guide

This document explains how to update and extend the BMLS Lab website (`BMLS Lab.html`).

---

## File Structure

```
BMLS Lab.html        ← main source file (edit this)
index.html           ← self-contained export for GitHub Pages (regenerate after edits)
build_index.py       ← regenerates index.html from BMLS Lab.html
fonts/               ← Source Serif 4 + Source Sans 3 (self-hosted, SIL Open Font License)
uploads/
  IMG_3620.jpeg      ← your profile photo (embedded in index.html; not in the repo)
  saba-sohrabi.jpg   ← student photo
  research-*.png/svg ← research figures
  bmls-fork-v2.png         ← lab icon with "BMLS" wordmark (original; used for link previews)
  bmls-fork-v2-small.png   ← lab icon, heavy strokes (original; source of the favicons)
  bmls-mark.png            ← the mark alone, transparent, heavy strokes (header, footer)
  bmls-mark-fine.png       ← the mark alone, transparent, fine strokes (homepage hero)
  favicon-32.png, icon-192.png, apple-touch-icon.png  ← browser-tab and home-screen icons
files/
  CV_EU.pdf          ← your CV (linked from the People section)
MAINTENANCE.md       ← this file
```

---

## How the Site Works

The site is a single HTML file using **React** (via CDN) with **Babel** for JSX. All content lives inside `<script type="text/babel">` at the bottom of `BMLS Lab.html`. All styling for the live design lives in the `<style>` block in `<head>`, under the comment `/* ── V1 styles ── */`.

Three design variants (V1, V2, V3) are defined as React components. **V1** is the one the site shows. V2 and V3 are older experiments that are no longer styled for the current fonts; you can ignore them.

---

## Updating Content

Open `BMLS Lab.html` in any text editor and find the data arrays near the top of the `<script type="text/babel">` block.

### 1. Adding a News Item

Find the `NEWS` array:

```js
const NEWS = [
  { date:"Nov 2026", text:'Your news item text here.', link:null },
  // ... existing items
];
```

Add a new object at the **top** of the array (newest first). Use `link:"https://…"` to make the whole item a link, or write the text as JSX (`text:<>… <a href="…" target="_blank" rel="noreferrer">…</a> …</>`) to link only part of it. The News section shows the 10 most recent items (`NEWS.slice(0,10)` inside V1).

---

### 2. Adding / Editing a Research Thrust

Find the `RESEARCH` array. Each thrust has a `title`, `body` (list of paragraphs), a figure (`image`, `imageId`, `alt`), and `related` work. Figures listed in a `<meta name="ext-resource-dependency" …>` tag at the top of the file get embedded into `index.html`; add one for any new figure.

---

### 3. Publications

Find the `PUBLICATIONS` array. Entries are grouped by `year` automatically, in the order they appear. `Ekin Uğurel` is bolded automatically in author lists.

---

### 4. Updating Your Bio

In the `V1` component, find the comment `{/* PEOPLE — PI BIO */}`. The title/affiliation line and the three bio paragraphs are plain text:

```jsx
<p className="v1-affil">Assistant Professor, Industrial and Systems Engineering<br/>University of Houston</p>
<p>
  Ekin Uğurel is an Assistant Professor in …
</p>
```

Students are in the `STUDENTS` array near the top of the file.

---

### 5. Updating Your Photo

Replace `uploads/IMG_3620.jpeg` with a new file (keep the same filename, or update the path in two places):

1. The `<meta>` tag in `<head>`:
   ```html
   <meta name="ext-resource-dependency" content="uploads/YOUR_NEW_PHOTO.jpeg" data-resource-id="profilePhoto"/>
   ```
2. The `<img className="v1-photo" …>` tag in the PI section of `V1`.

---

### 6. Updating Links (CV, Scholar, GitHub, Email)

In the PI section of `V1`, find the link list under the bio paragraphs:

```jsx
{[
  ["CV","files/CV_EU.pdf",false],
  ["Google Scholar","https://scholar.google.com/citations?user=Xp6PAL0AAAAJ&hl=en&oi=ao",false],
  ["GitHub","https://github.com/ekinugurel",false],
  ["Email","mailto:eugurel@Central.UH.EDU",false],
].map(([l,href,isReq])=>(
```

Each entry is `[label, href, isReq]`; set `isReq` to `true` to show a small "(on request)" note next to a link.

**Updating your CV:** replace `files/CV_EU.pdf` with the new PDF (same filename), then commit and push. No rebuild of `index.html` is needed for this — the PDF is served as a separate file, not embedded in the bundle. Your personal site (`ekinugurel.github.io`) keeps its own copy at `files/CV_EU.pdf`, so update both.

---

### 7. Updating the Join the Lab Section

Find `{/* JOIN US */}` in `V1`. Each opening is a `{ role:"…", detail:"…" }` object; the contact sentence and email link are just below.

---

## Adding a New Section

Inside `V1`'s `<main>`, add a `<Section>` between the existing ones:

```jsx
<Section id="teaching" title="Teaching" intro="Optional one-paragraph introduction.">
  {/* your content here */}
</Section>
```

Then add it to the header navigation: find `const NAV = [...]` at the top of `V1` and add `["Teaching","#teaching"]`.

---

## Logo and Icons

- The header and footer use `uploads/bmls-mark.png`; the homepage hero uses `uploads/bmls-mark-fine.png`. Both are transparent crops of your original icons, embedded into `index.html` via the `markBold` / `markFine` `<meta name="ext-resource-dependency">` tags.
- Browser-tab icons, the iPhone home-screen icon, and the link-preview image are set in the `<!-- shell-head:start -->` block in `<head>`.
- To change the logo, replace those PNG files (keep the names) and rebuild.

---

## Deploying to GitHub Pages

After each update:

1. Edit `BMLS Lab.html` as described above.
2. Run `python3 build_index.py` in this folder. It copies the app code, the whole `<head>` (fonts, styles, icons, link-preview tags) and the embedded images into `index.html`.
3. Commit and push `index.html`, `BMLS Lab.html`, and anything new in `uploads/`, `fonts/`, or `files/`.

Files that `index.html` links to by URL (everything in `fonts/`, the favicons, `files/CV_EU.pdf`) must be in the repo — they are not embedded.

### Custom domain

Add a file named `CNAME` to the repo root containing just your domain:
```
bmls-lab.uh.edu
```
Then configure your DNS per GitHub's documentation.

---

## Color & Typography Reference

Colors are CSS variables on `.v1` in the `/* ── V1 styles ── */` block; they come from the lab mark.

| Variable | Value | Used for |
|----------|-------|----------|
| `--ink` | `#1C1B1A` | Headings, the mark's black, primary button |
| `--text` | `#33302C` | Body text |
| `--muted` | `#6B655D` | Dates, labels, author lists |
| `--rule` | `#E5E1D9` | Dividers |
| `--coral` | `#E0605A` | The mark's red; link underlines |
| `--coral-ink` | `#B3443D` | Small red text (PDF/Code links, "Principal investigator") — darker so it stays readable |
| `--paper` | `#FFFFFF` | Page background |

| Role | Font | Notes |
|------|------|-------|
| Headings and body text | Source Serif 4 | Variable font; picks a display cut automatically at large sizes |
| Navigation, dates, labels, author lists | Source Sans 3 | |

Both fonts are self-hosted in `fonts/` (no Google Fonts request) and include Turkish characters such as ğ.

---

## Quick Reference: Where Things Live

| Content | Location in file |
|---------|-----------------|
| News items | `const NEWS = [...]` |
| Research thrusts | `const RESEARCH = [...]` |
| Publications | `const PUBLICATIONS = [...]` |
| Students | `const STUDENTS = [...]` |
| Header navigation | `const NAV = [...]` at the top of `V1` |
| Homepage title, tagline, focus areas | `{/* HERO */}` and `const FOCUS = [...]` in `V1` |
| Bio text, profile photo, links | `{/* PEOPLE — PI BIO */}` in `V1` |
| Recruiting text | `{/* JOIN US */}` in `V1` |
| Footer text | `{/* FOOTER */}` in `V1` |
| Colors, spacing, fonts | `/* ── V1 styles ── */` in the `<style>` block in `<head>` |
| Favicons, link-preview tags | `<!-- shell-head:start -->` block in `<head>` |
