---
name: explain
description: Build a local animated, step-by-step explainer website for a pipeline, model or algorithm in the current project, on its real data, served on localhost, so the user can understand it and then critique it. Use when the user says "explain", "/explain", "make an explainer", "show me visually what the model/pipeline does", "animate how we process the data", or "walk me through this visually".
---

# explain — animated walk-through of real code on real data

Output: `explorer/` (or the folder the user names) holding `export.py`, `data.json` and `index.html`,
served on a free localhost port. It is an internal tool for understanding, not a deliverable.
Below, `$SKILL` is this skill's folder (`~/.claude/skills/explain` for a manual install, or the plugin's
`skills/explain`). A finished example lives in the repo's `examples/kmeans/`.

## 1 · Understand first (do not skip)
- Read the pipeline/model source end to end, and run it once. List its real stages in execution order:
  inputs → each transformation or decision → outputs.
- For each stage, note (a) one picture that shows what changes, (b) the key formula or line of code,
  (c) the assumption most worth arguing about.
- Aim for 5–9 stages. The question each stage answers is its title.

## 2 · Export real data — `export.py`
- Run the source with `runpy.run_path(...)` (or import it) and take objects from its globals, so the page
  shows exactly what the code computes. Never retype numbers into the HTML.
- Dump only what the stages draw to `data.json`. Use `json.dumps(..., allow_nan=False)` and turn NaN into None:
  browsers reject `NaN`, and the page silently renders blank.
- **Alignment trap:** if the source re-sorts a table after building a positional array (a matrix, a
  `.values` column), rows stop matching. Recompute per-row values from the row itself, or store them as columns
  before the sort.
- End with an `assert` that one headline number in the JSON equals the source's own printout.

## 3 · Build the page — copy `$SKILL/template.html`
- Fill in `{{TITLE}}` (2–4 words), `{{HEADING}}` and `{{SUBTITLE}}`. Replace the example `s1` and the `STAGES` array.
- Each stage is `{name, title, draw, text, tech, code, words, critique}`:
  - `text` is plain words, no jargon. `tech` is precise: method, library, edge cases.
  - `code` is the real line or formula from the source. `words` is a 2–4 term glossary.
  - `critique` is 1–3 questions that point at the stage's weakest assumption. This box is the point of the page,
    because the user reads the page in order to critique the model.
- `draw(g)` draws into an SVG with viewBox 0 0 1000 560. Helpers:
  - `S`/`T` create elements and text.
  - `fade(node, delay)` fades a node in. `draw(path, delay, dur)` animates a path's stroke.
  - `tween(ms, e => ..., delay)` runs eased JS animation; use it for anything that moves or grows.
  - `later(ms, fn)`: sequenced timeouts that cancel when the stage changes.
  - `tipOn(el, () => html)` adds a hover tooltip.
  - `legend`, `axisTitle`, `fmt`.
- Pictures that explain well: something moving from the "before" state to the "after" state (bars re-sorting,
  items dropping into buckets, connectors re-routing), one worked example before the full set, and a
  constraint drawn as a line that bars overflow (in red) or fit under.
- Keep one consistent colour per category across all stages. Give maps left (x 10–570) and charts right
  (x 600–990), or use the full width.

## 4 · Serve and verify
- Find a free port (`ss -ltn`) and run `python3 -m http.server <port> -d explorer` in the background.
- Screenshot every stage after its animation finishes (open `http://localhost:<port>/#N` in a headless browser,
  e.g. Playwright or a browser skill, wait about 8 s, screenshot) and look at every one. Check for:
  - text clipped at the right edge, and overlapping labels
  - console errors
  - numbers on screen that match the source's printout
- Fix what you find before showing the user. Then give the URL, a one-line description of each stage, and the
  stage you think deserves the hardest critique.

## 5 · Share (only when the user asks)
The page is static: `index.html` + `data.json`. Copy just those two into a temporary folder named after the
project (e.g. `pricing-model-explorer`) and deploy that folder to any static host (`vercel deploy --prod --yes`,
Netlify, GitHub Pages), so no source files or host config reach the repo or the site. Then `curl` the URL to
confirm it returns 200, and screenshot it once. A public URL is public; tell the user that. A browser can get a 404 for a minute after a deploy even when
`curl` returns 200; reload with a query string (`?r=2`) before calling it broken. Extra pages go in subfolders
(`scenarios/index.html` + `scenarios/data.json`) of the same deploy folder, and each page links to the others.

## Rules
- Commit only to the user's working branch, and never push or open a PR without asking.
- Every critique point must come from something the code actually does, never a generic worry.
- After the source changes, re-run `export.py` and refresh the page; the HTML should not need edits.
