#!/usr/bin/env python3
"""
Homeowner's Handbook static site generator.

Source of truth:
  data/tasks/<slug>.json   -- one JSON file per task (99 files)
  data/categories.json     -- category metadata (name -> {code, blurb})

Output (into dist/):
  index.html
  browse/index.html
  about/index.html
  category/<cat-slug>/index.html      (one per category)
  task/<task-slug>/index.html         (one per task)
  assets/style.css, assets/site.js
  sitemap.xml, robots.txt
  data/tasks-index.json               (lightweight JSON used by nothing server-side,
                                        kept for future app/API reuse)

No external dependencies. Run: python3 generator/build.py
"""
import json
import os
import re
import shutil
import html as htmlmod
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
TASKS_DIR = os.path.join(DATA_DIR, "tasks")
DIST_DIR = os.path.join(ROOT, "dist")
ASSETS_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets_src")

SITE_URL = "https://homeowners-handbook.com"
PRIORITY_ORDER = ["Safety-Critical", "Preventive", "Cosmetic", "Upgrade"]
PRIORITY_CLASS = {"Safety-Critical": "safety", "Preventive": "preventive", "Cosmetic": "cosmetic", "Upgrade": "upgrade"}


def esc(s):
    return htmlmod.escape(str(s), quote=True)


def slugify(name):
    s = name.lower()
    s = re.sub(r"[&']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_data():
    tasks = []
    for fname in sorted(os.listdir(TASKS_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(TASKS_DIR, fname), encoding="utf-8") as f:
            tasks.append(json.load(f))
    tasks.sort(key=lambda t: t["id"])

    with open(os.path.join(DATA_DIR, "categories.json"), encoding="utf-8") as f:
        categories = json.load(f)

    # validate every task references a known category
    unknown = sorted({t["category"] for t in tasks} - set(categories.keys()))
    if unknown:
        raise SystemExit(f"ERROR: tasks reference undefined categories: {unknown}")

    return tasks, categories


def mode_class(mode):
    if mode == "DIY":
        return "mode-diy"
    if mode == "Pro":
        return "mode-pro"
    return "mode-either"  # covers "DIY or Pro"


def badge_html(priority):
    return f'<span class="badge {PRIORITY_CLASS.get(priority, "")}">{esc(priority)}</span>'


def difficulty_dots(n):
    n = max(0, min(5, int(n)))
    return "●" * n + "○" * (5 - n)


def head(title, description, canonical_path, extra=""):
    canonical = f"{SITE_URL}{canonical_path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='8' fill='%2328495A'/%3E%3Ctext x='32' y='42' font-family='Space Grotesk,Arial,sans-serif' font-weight='700' font-size='24' fill='%23F5F3EC' text-anchor='middle'%3EHH%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root_rel(canonical_path)}assets/style.css">
{extra}</head>
<body>
"""


def root_rel(path):
    """Relative prefix to site root from a given path like /task/foo/ -> ../../"""
    depth = path.strip("/").count("/") + (0 if path.endswith("/") and path.strip("/") == "" else 1)
    if path == "/":
        return ""
    parts = [p for p in path.strip("/").split("/") if p]
    return "../" * len(parts)


def header_nav(current_path):
    r = root_rel(current_path)
    home_href = r + "index.html" if r else "index.html"
    # use directory-style links (Cloudflare Pages serves index.html for a dir)
    home_href = r if r else "./"
    browse_href = r + "browse/"
    about_href = r + "about/"

    def cur(path_key):
        return ' aria-current="page"' if current_path.startswith(path_key) else ""

    return f"""<header class="site">
  <div class="wrap bar">
    <a href="{home_href}" class="brand">
      <span class="mark">HH</span>
      <span class="name">Homeowner's <em>Handbook</em></span>
    </a>
    <div class="search-shell">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input id="headerSearch" type="text" placeholder="Search 99 repairs & upgrades…" autocomplete="off">
    </div>
    <nav class="top-links">
      <a href="{home_href}"{cur('/')if current_path=='/' else ''}>Home</a>
      <a href="{browse_href}"{cur('/browse')}>Browse all</a>
      <a href="{about_href}"{cur('/about')}>About</a>
    </nav>
  </div>
</header>
"""


def footer_html():
    return f"""<footer>
  <div class="wrap">
    <span>&copy; {date.today().year} Homeowner's Handbook</span>
    <span>homeowners-handbook.com</span>
  </div>
</footer>
"""


def modal_and_toast():
    return """<div class="modal-overlay" id="modalOverlay">
  <div class="modal">
    <h3>Suggest an edit</h3>
    <p>For <strong id="modalTaskName"></strong>. Open contribution isn't live yet &mdash; but tell us what should change, and it'll be first in line for review when it is.</p>
    <textarea id="suggestText" placeholder="e.g. Step 3 should mention shutting off the breaker first&hellip;"></textarea>
    <div class="modal-actions">
      <button class="btn-ghost" onclick="closeModal()">Cancel</button>
      <button class="btn-suggest" onclick="submitSuggestion()">Submit suggestion</button>
    </div>
  </div>
</div>
<div class="toast" id="toast"></div>
"""


def script_tag(current_path):
    r = root_rel(current_path)
    return f'<script src="{r}assets/site.js"></script>\n'


def ticket_card(t, root):
    href = f"{root}task/{t['slug']}/"
    search_blob = esc(f"{t['task']} {t['category']} {t['trigger']}".lower())
    return f"""<a class="ticket" href="{href}" data-priority="{esc(t['priority'])}" data-search="{search_blob}">
    <div class="perf"></div>
    <div class="ticket-top">
      <span class="tid mono">NO. {t['id']:03d}</span>
      {badge_html(t['priority'])}
    </div>
    <div class="cat-label">{esc(t['category'])}</div>
    <h3>{esc(t['task'])}</h3>
    <div class="meta-row">
      <span>&#9201; {esc(t['time'])}</span>
      <span>{esc(t['mode'])}</span>
      <span>{difficulty_dots(t['difficulty'])}</span>
    </div>
  </a>"""


def cat_card(cat_name, meta, count, root):
    href = f"{root}category/{slugify(cat_name)}/"
    return f"""<a class="cat-card" href="{href}">
    <span class="tab"></span>
    <span class="code">{esc(meta['code'])}</span>
    <h3>{esc(cat_name)}</h3>
    <p>{esc(meta['blurb'])}</p>
    <span class="n mono">{count} tasks &rarr;</span>
  </a>"""


def filter_bar_html():
    chips = ['<button class="chip active" data-priority="">All</button>']
    for p in PRIORITY_ORDER:
        chips.append(f'<button class="chip" data-priority="{esc(p)}">{esc(p)}</button>')
    return f"""<div class="filter-bar">
    <span class="fb-label">Priority</span>
    {''.join(chips)}
  </div>"""


def build_home(tasks, categories, out_dir):
    root = ""
    cats = list(categories.keys())
    safety_count = sum(1 for t in tasks if t["priority"] == "Safety-Critical")
    cat_cards = "\n      ".join(
        cat_card(c, categories[c], sum(1 for t in tasks if t["category"] == c), root) for c in cats
    )
    safety_tickets = "\n      ".join(
        ticket_card(t, root) for t in tasks if t["priority"] == "Safety-Critical"
    )[:0] or "\n      ".join(
        ticket_card(t, root) for t in [t for t in tasks if t["priority"] == "Safety-Critical"][:4]
    )

    body = f"""{header_nav('/')}
<main>
  <div class="wrap">
    <section class="hero">
      <p class="eyebrow">{len(tasks)} tasks &middot; {len(cats)} systems &middot; one house</p>
      <h1>Every repair your house will ever ask of you.</h1>
      <p class="sub">Look up any home repair, maintenance job, or upgrade. Follow clear steps, know your DIY-vs-pro line, and watch a trusted video before you start.</p>
      <div class="stat-row">
        <div class="stat"><span class="n">{len(tasks)}</span><span class="l">Cataloged tasks</span></div>
        <div class="stat"><span class="n">{safety_count}</span><span class="l">Safety-critical</span></div>
        <div class="stat"><span class="n">{len(cats)}</span><span class="l">Home systems</span></div>
      </div>
    </section>

    <div class="section-head">
      <h2>Browse by system</h2>
      <span class="count mono">{len(cats)} categories</span>
    </div>
    <div class="cat-grid">
      {cat_cards}
    </div>

    <div class="section-head">
      <h2>Start here &mdash; safety first</h2>
      <span class="count mono">{safety_count} tasks</span>
    </div>
    <div class="ticket-grid">
      {safety_tickets}
    </div>

    <section class="roadmap">
      <div class="wrap">
        <div>
          <p class="eyebrow">What's next</p>
          <h2>Built to grow like a wiki</h2>
          <p>This first version ships with a vetted starter catalog. The structure underneath &mdash; one record per task, versioned steps, sourced videos &mdash; is built so homeowners, contractors, and editors can propose improvements once community editing goes live.</p>
        </div>
        <ol>
          <li><strong>Suggest an edit</strong><span>Every task page has a "Suggest an edit" action today &mdash; it queues real feedback for the team while accounts and moderation are built.</span></li>
          <li><strong>Open contribution</strong><span>Verified pros and experienced homeowners will be able to submit step revisions, better videos, and regional notes directly.</span></li>
          <li><strong>Revision history</strong><span>Like a wiki, every task will show its edit history and who last verified each step.</span></li>
        </ol>
      </div>
    </section>
  </div>
</main>
{footer_html()}
{script_tag('/')}"""

    html = head(
        "Homeowner's Handbook — Look Up Any Home Repair",
        f"A field guide to home repair, maintenance, and upgrades. Look up any of {len(tasks)} common homeowner tasks, follow clear steps, and know when to call a pro.",
        "/",
    ) + body + "\n</body>\n</html>\n"

    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_browse(tasks, out_dir):
    path = "/browse/"
    root = "../"
    out = os.path.join(out_dir, "browse")
    os.makedirs(out, exist_ok=True)

    tickets = "\n      ".join(ticket_card(t, root) for t in tasks)

    body = f"""{header_nav(path)}
<main>
  <div class="wrap">
    <div class="crumb"><a href="../">Home</a> / Browse all</div>
    <div class="section-head" style="margin-top:0;">
      <h2>All tasks</h2>
      <span class="count mono" data-total-label="of {len(tasks)}">{len(tasks)} of {len(tasks)}</span>
    </div>
    <div class="search-shell" style="max-width:100%; margin-bottom:18px;">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input id="searchInput" type="text" placeholder="Filter these {len(tasks)} tasks&hellip;" autocomplete="off">
    </div>
    {filter_bar_html()}
    <div id="listArea">
      <div class="ticket-grid">
      {tickets}
      </div>
    </div>
  </div>
</main>
{footer_html()}
{script_tag(path)}"""

    html = head(
        "Browse all tasks — Homeowner's Handbook",
        f"Browse all {len(tasks)} homeowner repair, maintenance, and upgrade tasks. Filter by priority or search by keyword.",
        path,
    ) + body + "\n</body>\n</html>\n"

    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_category_pages(tasks, categories, out_dir):
    for cat_name, meta in categories.items():
        cslug = slugify(cat_name)
        path = f"/category/{cslug}/"
        root = "../../"
        out = os.path.join(out_dir, "category", cslug)
        os.makedirs(out, exist_ok=True)

        cat_tasks = [t for t in tasks if t["category"] == cat_name]
        tickets = "\n      ".join(ticket_card(t, root) for t in cat_tasks)

        body = f"""{header_nav(path)}
<main>
  <div class="wrap">
    <div class="crumb"><a href="../../">Home</a> / <a href="../../browse/">Browse</a> / {esc(cat_name)}</div>
    <div class="section-head" style="margin-top:0;">
      <h2>{esc(cat_name)}</h2>
      <span class="count mono" data-total-label="tasks">{len(cat_tasks)} tasks</span>
    </div>
    <p style="color:var(--ink-soft); font-family:'Space Grotesk',sans-serif; font-size:14px; margin-top:-8px;">{esc(meta['blurb'])}</p>
    <div class="search-shell" style="max-width:100%; margin-bottom:18px;">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input id="searchInput" type="text" placeholder="Filter {esc(cat_name)} tasks&hellip;" autocomplete="off">
    </div>
    {filter_bar_html()}
    <div id="listArea">
      <div class="ticket-grid">
      {tickets}
      </div>
    </div>
  </div>
</main>
{footer_html()}
{script_tag(path)}"""

        html = head(
            f"{cat_name} — Homeowner's Handbook",
            f"{meta['blurb']}. {len(cat_tasks)} tasks covering {cat_name.lower()} for homeowners.",
            path,
        ) + body + "\n</body>\n</html>\n"

        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)


def build_task_pages(tasks, out_dir):
    by_slug = {t["slug"]: t for t in tasks}
    for t in tasks:
        path = f"/task/{t['slug']}/"
        root = "../../"
        out = os.path.join(out_dir, "task", t["slug"])
        os.makedirs(out, exist_ok=True)

        if t.get("videoUrl"):
            video_html = f"""<a class="watch" href="{esc(t['videoUrl'])}" target="_blank" rel="noopener">
        Watch this guide
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17L17 7M17 7H8M17 7V16"/></svg>
      </a>"""
        else:
            video_html = '<span style="font-size:13px;color:var(--ink-faint);">No video linked yet</span>'

        verified_note = (
            '<div class="unverified-note" style="color:var(--green);">&#10003; Source checked against this task.</div>'
            if t.get("verified")
            else '<div class="unverified-note">This link is a suggested starting point and hasn\'t been individually re-checked recently &mdash; search the title to confirm it still matches before relying on it.</div>'
        )

        steps_html = "\n            ".join(f"<li><p>{esc(s)}</p></li>" for s in t["steps"])
        cat_slug = slugify(t["category"])

        body = f"""{header_nav(path)}
<main>
  <div class="wrap">
    <div class="crumb">
      <a href="../../">Home</a> /
      <a href="../../category/{cat_slug}/">{esc(t['category'])}</a> /
      {esc(t['task'])}
    </div>

    <div class="detail-card">
      <div class="perf-top"></div>
      <div class="detail-head">
        <div class="tid-row">
          <span class="tid">TASK NO. {t['id']:03d}</span>
          {badge_html(t['priority'])}
        </div>
        <h1>{esc(t['task'])}</h1>
        <a class="cat-label" href="../../category/{cat_slug}/">{esc(t['category'])}</a>
      </div>
      <div class="spec-strip">
        <div class="spec"><div class="l">Trigger</div><div class="v" style="font-size:13px;">{esc(t['trigger'])}</div></div>
        <div class="spec"><div class="l">Who does it</div><div class="v {mode_class(t['mode'])}">{esc(t['mode'])}</div></div>
        <div class="spec"><div class="l">Est. time</div><div class="v">{esc(t['time'])}</div></div>
        <div class="spec"><div class="l">Est. cost</div><div class="v">{esc(t['cost'])}</div></div>
        <div class="spec"><div class="l">Difficulty</div><div class="v">{difficulty_dots(t['difficulty'])}</div></div>
      </div>
      <div class="detail-body">
        <div>
          <div class="l mono" style="font-size:10px;letter-spacing:.08em;color:var(--ink-faint);text-transform:uppercase;margin-bottom:10px;">Step by step</div>
          <ol class="steps-list">
            {steps_html}
          </ol>
        </div>
        <div class="side-panel">
          <div class="video-box">
            <div class="l">Video guide</div>
            <div class="vt">{esc(t.get('videoTitle') or '&mdash;')}</div>
            {video_html}
            {verified_note}
          </div>
          <div class="contribute-box">
            <div class="l">Community editing (coming soon)</div>
            <p>See a better technique, a broken link, or a regional building-code note? Contributions will work like a wiki once accounts and review are live.</p>
            <button class="btn-suggest" onclick="openSuggestModal('{esc(t['task'])}')">Suggest an edit</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>
{footer_html()}
{modal_and_toast()}
{script_tag(path)}"""

        html = head(
            f"{t['task']} — Homeowner's Handbook",
            f"How to {t['task'].lower()}. {t['trigger']}. {t['mode']}, est. {t['time']}, {t['cost']}. Step-by-step guide with video.",
            path,
        ) + body + "\n</body>\n</html>\n"

        with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)


def build_about(out_dir):
    path = "/about/"
    out = os.path.join(out_dir, "about")
    os.makedirs(out, exist_ok=True)

    body = f"""{header_nav(path)}
<main>
  <div class="wrap">
    <div class="crumb"><a href="../">Home</a> / About</div>
    <section style="max-width:640px; padding:20px 0 60px;">
      <p class="eyebrow" style="font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--amber);margin-bottom:12px;">About this project</p>
      <h1 style="font-size:32px; letter-spacing:-0.01em; margin:0 0 16px;">A reference, not a lecture.</h1>
      <p style="color:var(--ink-soft); font-size:16px;">Homeowner's Handbook starts as a curated catalog of the repairs, maintenance jobs, and upgrades homeowners run into most. Every task lists what triggers it, how hard it is, whether it's safe to DIY, and a trusted video to watch before you start.</p>
      <p style="color:var(--ink-soft); font-size:16px;">The long-term goal is an open, wiki-style reference: homeowners and licensed pros contributing corrections, regional notes, and better sources over time, with a visible edit history so you always know what's been verified.</p>
    </section>
  </div>
</main>
{footer_html()}
{script_tag(path)}"""

    html = head(
        "About — Homeowner's Handbook",
        "About Homeowner's Handbook, a field guide to home repair, maintenance, and upgrades built to grow into an open wiki-style reference.",
        path,
    ) + body + "\n</body>\n</html>\n"

    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def build_sitemap(tasks, categories, out_dir):
    urls = ["/", "/browse/", "/about/"]
    urls += [f"/category/{slugify(c)}/" for c in categories]
    urls += [f"/task/{t['slug']}/" for t in tasks]
    today = date.today().isoformat()
    entries = "\n".join(
        f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""
    with open(os.path.join(out_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def build_robots(out_dir):
    txt = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    with open(os.path.join(out_dir, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


def build_search_index(tasks, out_dir):
    """Lightweight index kept for future app/API reuse -- not used by the generated
    pages themselves (they use inline data-search attributes for zero-JS-fetch filtering)."""
    out = os.path.join(out_dir, "data")
    os.makedirs(out, exist_ok=True)
    index = [
        {
            "id": t["id"],
            "slug": t["slug"],
            "task": t["task"],
            "category": t["category"],
            "priority": t["priority"],
            "mode": t["mode"],
            "time": t["time"],
            "difficulty": t["difficulty"],
        }
        for t in tasks
    ]
    with open(os.path.join(out, "tasks-index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def copy_assets(out_dir):
    dest = os.path.join(out_dir, "assets")
    os.makedirs(dest, exist_ok=True)
    shutil.copy(os.path.join(ASSETS_SRC, "style.css"), os.path.join(dest, "style.css"))
    shutil.copy(os.path.join(ASSETS_SRC, "site.js"), os.path.join(dest, "site.js"))


def main():
    tasks, categories = load_data()

    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR)

    copy_assets(DIST_DIR)
    build_home(tasks, categories, DIST_DIR)
    build_browse(tasks, DIST_DIR)
    build_about(DIST_DIR)
    build_category_pages(tasks, categories, DIST_DIR)
    build_task_pages(tasks, DIST_DIR)
    build_sitemap(tasks, categories, DIST_DIR)
    build_robots(DIST_DIR)
    build_search_index(tasks, DIST_DIR)

    page_count = 1 + 1 + 1 + len(categories) + len(tasks)
    print(f"Built {page_count} pages ({len(tasks)} tasks, {len(categories)} categories) into {DIST_DIR}")


if __name__ == "__main__":
    main()
