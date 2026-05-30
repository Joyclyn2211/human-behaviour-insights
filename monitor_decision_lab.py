"""
Weekly monitor for The Decision Lab (https://thedecisionlab.com)
Runs every Sunday at 8am via Windows Task Scheduler.

What it does:
1. Fetches the /biases page to find concepts not yet in the wiki
2. For each high-priority missing concept, fetches the full article
3. Creates a new wiki concept page
4. Updates the tracker and index
5. Logs the run

Usage: python monitor_decision_lab.py
"""

import json
import os
import re
import urllib.request
import urllib.error
from datetime import date, datetime

ROOT     = os.path.dirname(os.path.abspath(__file__))
WIKI     = os.path.join(ROOT, '..', 'wiki')
CONCEPTS = os.path.join(WIKI, 'concepts')
TRACKER  = os.path.join(WIKI, 'sources', 'decision-lab-tracker.md')
INDEX    = os.path.join(WIKI, 'index.md')
LOG      = os.path.join(WIKI, 'log.md')

# ── Priority list — fetch these first if not yet in wiki ──────────────────
PRIORITY_CONCEPTS = [
    ("fundamental-attribution-error", "Fundamental Attribution Error",
     "https://thedecisionlab.com/biases/fundamental-attribution-error",
     "Relationships, conflict — why we blame character and ignore context"),
    ("empathy-gap",     "Empathy Gap",
     "https://thedecisionlab.com/biases/empathy-gap",
     "Intimate relationships — failing to predict how emotions change our behaviour"),
    ("planning-fallacy","Planning Fallacy",
     "https://thedecisionlab.com/biases/planning-fallacy",
     "Personal development — systematically underestimating time and effort"),
    ("dunning-kruger",  "Dunning-Kruger Effect",
     "https://thedecisionlab.com/biases/dunning-kruger-effect",
     "Self-knowledge — incompetence is invisible to the incompetent"),
    ("choice-overload", "Choice Overload",
     "https://thedecisionlab.com/biases/choice-overload",
     "Decision-making, modern life — too many options paralyse rather than liberate"),
    ("peak-end-rule",   "Peak-End Rule",
     "https://thedecisionlab.com/biases/peak-end-rule",
     "Memory, relationships — we remember peaks and endings, not averages"),
    ("ikea-effect",     "IKEA Effect",
     "https://thedecisionlab.com/biases/ikea-effect",
     "Identity, ownership — we overvalue things we helped create"),
    ("sunk-cost-fallacy","Sunk Cost Fallacy",
     "https://thedecisionlab.com/biases/sunk-cost-fallacy",
     "Decisions, relationships — continuing because of past investment"),
    ("optimism-bias",   "Optimism Bias",
     "https://thedecisionlab.com/biases/optimism-bias",
     "Planning, risk — overestimating positive outcomes"),
    ("loss-aversion",   "Loss Aversion",
     "https://thedecisionlab.com/biases/loss-aversion",
     "Decision-making, finance — losses hurt twice as much as gains feel good"),
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; HumanBehaviourWikiBot/1.0)'
}

# ── Helpers ───────────────────────────────────────────────────────────────

def today():
    return date.today().isoformat()

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode('utf-8', errors='replace')
    except Exception as e:
        return None

def concept_file(slug):
    return os.path.join(CONCEPTS, slug + '.md')

def already_ingested(slug):
    return os.path.exists(concept_file(slug))

def extract_text_from_html(html):
    """Very basic HTML → text stripping."""
    html = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<style[^>]*>[\s\S]*?</style>',   '', html, flags=re.IGNORECASE)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = re.sub(r'&nbsp;', ' ', html)
    html = re.sub(r'&amp;',  '&', html)
    html = re.sub(r'&lt;',   '<', html)
    html = re.sub(r'&gt;',   '>', html)
    html = re.sub(r'&quot;', '"', html)
    html = re.sub(r'\s{2,}', '\n', html)
    return html.strip()

def extract_definition(text):
    """Try to pull a definition sentence from article text."""
    for line in text.split('\n'):
        line = line.strip()
        if len(line) > 60 and len(line) < 300:
            if any(w in line.lower() for w in ['is ', 'refers to', 'describes', 'occurs when', 'tendency']):
                return line
    return "See The Decision Lab for the full definition."

def build_concept_page(slug, title, url, relevance, text):
    defn = extract_definition(text)
    today_str = today()
    return f"""---
title: {title}
tags: [concept, psychology, decision-making, behavioural-economics]
source_count: 1
last_updated: {today_str}
---

# {title}

**Key Insight:** {defn}

*Source: The Decision Lab · {url}*

---

## What It Is

{defn}

**Relevance to this wiki:** {relevance}

---

## Key Research

*(Fetch the full article at {url} for complete research summary and examples.)*

---

## Applied to Daily Life

### With Yourself
Notice when {title.lower()} is operating in your thinking. Ask: "Is this bias shaping my decision right now?"

### In Business
{title} affects professional decisions in specific, predictable ways. Awareness is the first step to designing around it.

### In Social Relationships
Social interactions are a rich environment for {title.lower()}. Knowing the pattern helps you respond rather than react.

### In Intimate Relationships
Close relationships amplify most cognitive biases. Understanding {title.lower()} gives you language and tools for more honest engagement.

---

## See Also
- [[Cognitive Biases]]
- [[Confirmation Bias]]
- [[Self-Knowledge]]

*Note: This is a stub page auto-generated from The Decision Lab monitor. Ask Claude to expand it with full content from {url}.*
"""

def update_tracker(slug, title, notes="auto-generated stub"):
    if not os.path.exists(TRACKER):
        return
    with open(TRACKER, 'r', encoding='utf-8') as f:
        content = f.read()
    today_str = today()
    new_row = f"| {title} | [[{title}]] | {today_str} — {notes} |"
    content = content.replace(
        "| Concept | Wiki Page | Date Added |",
        f"| Concept | Wiki Page | Date Added |\n{new_row}"
    )
    # Update monitoring log table
    log_row = f"| {today_str} | monitor | Added stub: {title} |"
    content = content.replace(
        "| 2026-05-30 | Initial ingest |",
        f"{log_row}\n| 2026-05-30 | Initial ingest |"
    )
    with open(TRACKER, 'w', encoding='utf-8') as f:
        f.write(content)

def update_index(title, slug, description):
    if not os.path.exists(INDEX):
        return
    with open(INDEX, 'r', encoding='utf-8') as f:
        content = f.read()
    new_line = f"| [{title}](concepts/{slug}.md) | {description} |"
    # Insert after the last concept line
    content = content.replace(
        "| [Status Quo Bias](concepts/status-quo-bias.md)",
        f"{new_line}\n| [Status Quo Bias](concepts/status-quo-bias.md)"
    )
    with open(INDEX, 'w', encoding='utf-8') as f:
        f.write(content)

def append_log(message):
    if not os.path.exists(LOG):
        return
    with open(LOG, 'r', encoding='utf-8') as f:
        content = f.read()
    today_str = today()
    entry = f"\n## [{today_str}] monitor | Decision Lab weekly check\n\n{message}\n\n---\n"
    # Insert after first ---
    content = content.replace("---\n\n## [2026-05-30]", f"---{entry}\n## [2026-05-30]", 1)
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write(content)

# ── Main ──────────────────────────────────────────────────────────────────

def main():
    print(f"[{today()}] Decision Lab monitor starting...")
    added = []
    skipped = []

    for slug, title, url, relevance in PRIORITY_CONCEPTS:
        if already_ingested(slug):
            skipped.append(title)
            print(f"  ✓ Already ingested: {title}")
            continue

        print(f"  → Fetching: {title}")
        html = fetch_url(url)
        if not html:
            print(f"  ✗ Could not fetch: {url}")
            continue

        text = extract_text_from_html(html)
        page = build_concept_page(slug, title, url, relevance, text)

        # Write the page
        with open(concept_file(slug), 'w', encoding='utf-8') as f:
            f.write(page)

        update_tracker(slug, title)
        update_index(title, slug, relevance)
        added.append(title)
        print(f"  ✓ Created stub: {title}")

        # Only add 2 per run to keep it manageable
        if len(added) >= 2:
            break

    # Write to log
    if added:
        msg = f"Added {len(added)} new concept stub(s): {', '.join(added)}\nSkipped (already ingested): {', '.join(skipped[:5])}"
    else:
        msg = f"No new concepts added. All priority concepts already ingested. Skipped: {', '.join(skipped[:5])}"

    append_log(msg)
    print(f"\nDone. Added: {added or 'none'}")
    print(f"Note: Stub pages were created. Ask Claude to expand them with full content.")

if __name__ == '__main__':
    main()
