# Homeowner's Handbook

A field guide to home repair, maintenance, and upgrades. Static, SEO-optimized,
no external dependencies to build.

## Structure

```
data/
  tasks/<slug>.json     One JSON file per task (99 files). Source of truth.
  categories.json       Category metadata: name -> {code, blurb}.

generator/
  build.py              Reads data/, writes the full static site into dist/.
  validate_tasks.py     Schema-validates every data/tasks/*.json file.
  check_links.py        Walks dist/ and verifies every internal link resolves.
  assets_src/
    style.css           Site styles.
    site.js              Progressive-enhancement JS (search/filter, modal).

dist/                   Generated output (gitignored). Deploy this folder.

.github/workflows/validate.yml   Runs schema validation + build + link check on every push.
```

## Why one file per task

Each task is its own small JSON file rather than one big array, because:

- **Future backend**: each file maps cleanly to a future database row —
  migrating to a real DB later is a straightforward import script.
- **Future app**: the same JSON records can be served as-is (or via an API)
  to an iOS/Android client, no reshaping required.
- **Editable at the file level**: a future "suggest an edit" contribution
  maps to a diff on one small file, not a change buried in a giant array —
  which matters once community/wiki-style editing is live.

## Local workflow

```bash
python3 generator/validate_tasks.py   # check data/tasks/*.json against schema
python3 generator/build.py            # generate dist/
python3 generator/check_links.py      # verify no broken internal links
```

Open `dist/index.html` in a browser, or serve it locally:

```bash
cd dist && python3 -m http.server 8000
```

## Adding or editing a task

1. Add/edit a JSON file in `data/tasks/<slug>.json`. Required fields:
   `id`, `slug` (must match filename), `category` (must exist in
   `data/categories.json`), `task`, `trigger`, `priority`
   (`Safety-Critical` / `Preventive` / `Cosmetic` / `Upgrade`), `difficulty`
   (1-5), `mode` (`DIY` / `Pro` / `DIY or Pro`), `time`, `cost`, `steps`
   (non-empty list of strings), `videoTitle`, `videoUrl`, `verified` (bool).
2. Run `python3 generator/validate_tasks.py` to check it.
3. Run `python3 generator/build.py` to regenerate the site.
4. Commit — CI re-validates and rebuilds on push.

## Deployment

Deploy the contents of `dist/` to Cloudflare Pages (or any static host).
`dist/` is regenerated on every build, so it isn't committed to the repo —
only `data/` and `generator/` are the tracked source of truth.
