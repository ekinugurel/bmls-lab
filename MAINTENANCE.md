# BMLS Lab Website — Maintenance Guide

This document explains how to update and extend the BMLS Lab website (`BMLS Lab.html`).

---

## File Structure

```
BMLS Lab.html       ← main source file (edit this)
index.html          ← self-contained export for GitHub Pages (regenerate after edits)
uploads/
  IMG_3620.jpeg     ← your profile photo
MAINTENANCE.md      ← this file
```

---

## How the Site Works

The site is a single HTML file using **React** (via CDN) with **Babel** for JSX. All content lives inside `<script type="text/babel">` at the bottom of `BMLS Lab.html`. There are no build tools, no npm, no config files.

Three design variants (V1, V2, V3) are defined as React components. You selected **V1 (Academic Minimal)** — this is the one that renders by default.

---

## Updating Content

Open `BMLS Lab.html` in any text editor and find the data arrays near the top of the `<script type="text/babel">` block.

### 1. Adding a News Item

Find the `NEWS` array (~line 60):

```js
const NEWS = [
  { date:"Mar 2026", text:'Your news item text here.' },
  // ... existing items
];
```

Add a new object at the **top** of the array (newest first):

```js
{ date:"Sep 2026", text:'New paper: "Your Title" — Journal Name.' },
```

---

### 2. Adding / Editing a Research Thrust

Find the `RESEARCH` array (~line 40):

```js
const RESEARCH = [
  {
    id:"01",
    title:"Human–AI Coevolution in Travel",
    sub:"Recommender Systems & Behavioral Impact",
    desc:"Full description paragraph here.",
    tags:["Tag One","Tag Two","Tag Three"],
  },
  // ...
];
```

- **Edit** an existing entry by changing its fields.
- **Add** a new thrust by appending a new object (`id:"04"`, etc.). The grid will expand automatically — note that 3 columns works best; for 4+, consider changing the layout to `gridTemplateColumns:"repeat(2,1fr)"`.

---

### 3. Updating Your Bio

Find the PI Bio section inside the `V1` component. Look for the text starting with `Dr. Uğurel earned her PhD`:

```jsx
<p style={{ ... }}>
  Dr. Uğurel earned her PhD in Transportation Engineering...
</p>
<p style={{ ... }}>
  Her work bridges theoretical ML and practical challenges...
</p>
```

Edit the text directly. The title/affiliation line is just above:

```jsx
<div style={{ fontSize:14.5, color:MUT, marginBottom:24 }}>
  Assistant Professor, Industrial and Systems Engineering<br/>
  University of Houston
</div>
```

---

### 4. Updating Your Photo

Replace `uploads/IMG_3620.jpeg` with a new file (keep the same filename, or update the path in two places):

1. The `<meta>` tag in `<head>`:
   ```html
   <meta name="ext-resource-dependency" content="uploads/YOUR_NEW_PHOTO.jpeg" data-resource-id="profilePhoto"/>
   ```

2. The `<img>` tag inside V1's PI Bio section:
   ```jsx
   <img src={window.__resources?.profilePhoto || "uploads/YOUR_NEW_PHOTO.jpeg"} .../>
   ```

---

### 5. Updating Links (CV, Scholar, GitHub, Email)

In the V1 PI Bio section, find:

```jsx
{["CV","Google Scholar","GitHub","Email"].map(l => {
```

These are currently `href="#"` placeholders. Replace each `href` individually by switching from `.map` to explicit anchors:

```jsx
<a href="https://your-cv-link.pdf" ...>CV</a>
<a href="https://scholar.google.com/citations?user=YOURCODE" ...>Google Scholar</a>
<a href="https://github.com/ekinugurel" ...>GitHub</a>
<a href="mailto:ekin.ugurel@houston.edu" ...>Email</a>
```

---

### 6. Updating the Recruiting / Join Us Section

Find the `Join Us` section comment inside V1. Edit the heading and body text:

```jsx
<div style={{ ...serif, fontSize:22, ... }}>Prospective PhD Students</div>
<div style={{ fontSize:14, ... }}>
  Fully-funded positions for Fall 2026. ...
</div>
```

Update the mailto link:
```jsx
<Btn primary style={{ ... }}>Get in Touch →</Btn>
```
Change the `href` on the `<Btn>` component's `<a>` tag to `mailto:ekin.ugurel@houston.edu`.

---

## Adding a New Section

To add a new full-width section (e.g., Publications), insert it inside the `V1` component's return statement between existing `<section>` blocks. Here's a template:

```jsx
{/* PUBLICATIONS */}
<section style={{ padding:"80px 48px" }}>
  <div style={{ maxWidth:1100, margin:"0 auto" }}>
    <div style={{ display:"flex", alignItems:"baseline", gap:16, marginBottom:44 }}>
      <h2 style={{ ...serif, fontSize:36, color:INK }}>Publications</h2>
      <div style={{ flex:1, height:1, background:LINE }}/>
    </div>
    {/* your content here */}
  </div>
</section>
```

Use alternating backgrounds for visual rhythm:
- White sections: `background` omitted (inherits `#FAFAF8`)
- Tan/off-white sections: `background:TAN` (i.e. `#F3F0EB`)

---

## Adding a Navigation Link

Find the nav links array inside V1:

```jsx
{["Research","People","News","Join Us"].map(l=><NavLink key={l} label={l}/>)}
```

Add a new label:

```jsx
{["Research","People","Publications","News","Join Us"].map(...)}
```

To make it scroll to a section, give your section an `id`:

```jsx
<section id="publications" style={{ ... }}>
```

Then add `href="#publications"` to the NavLink component (currently the component always sets `href="#"` — update the `NavLink` function to accept an `href` prop if needed).

---

## Deploying to GitHub Pages

### First deploy

1. Create a GitHub repository (e.g. `bmls-lab`)
2. Go to **Settings → Pages** → Source: **Deploy from branch** → Branch: `main` → Folder: `/ (root)`
3. In your project, add `index.html` to the repo root
4. Push — GitHub will serve it at `https://yourusername.github.io/bmls-lab/`

### After each update

1. Edit `BMLS Lab.html` as described above
2. Regenerate `index.html` (the self-contained export) — ask the assistant to re-export, or re-run the bundler
3. Commit and push `index.html`

### Custom domain

Add a file named `CNAME` to the repo root containing just your domain:
```
bmls-lab.uh.edu
```
Then configure your DNS per GitHub's documentation.

---

## Color & Typography Reference

| Token | Value | Used for |
|-------|-------|----------|
| `R` (UH Red) | `#C8102E` | Accents, links on hover, borders |
| `INK` | `#1A1712` | Primary text, headings |
| `MUT` | `#7A6F63` | Secondary text, nav links |
| `BG` | `#FAFAF8` | Page background |
| `TAN` | `#F3F0EB` | Alternating section background |
| `LINE` | `#E2DDD4` | Dividers, card borders |

| Role | Font | Weight |
|------|------|--------|
| Display headings | DM Serif Display | 400 (regular) |
| Body, nav, UI | DM Sans | 300–600 |

---

## Quick Reference: Where Things Live

| Content | Location in file |
|---------|-----------------|
| News items | `const NEWS = [...]` |
| Research thrusts | `const RESEARCH = [...]` |
| Profile photo | `<img src=...>` inside V1 PI Bio section |
| Bio text | Two `<p>` tags inside V1 PI Bio section |
| Nav links | `["Research","People","News","Join Us"].map(...)` inside V1 Nav |
| Recruiting CTA text | V1 `{/* JOIN US */}` section |
| Lab tagline (hero) | `<p className="fu2" ...>` inside V1 Hero section |
| Footer text | V1 `{/* FOOTER */}` section |
