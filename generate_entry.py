"""
Daily entry generator for Human Behaviour website.
Run this script each morning to add a new entry to entries.json.

Usage:  python generate_entry.py
"""

import json
import os
import glob
import re
import random
import sys
from datetime import date, datetime

# Ensure UTF-8 console output on Windows (avoids cp1252 crashes on ✓ etc.)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.join(ROOT, '..', 'wiki')
DATA_FILE = os.path.join(ROOT, 'data', 'entries.json')

# ── Daily concept rotation ──────────────────────────────────────────────────
# Each tuple: (wiki_file_relative_path, display_source, id_slug)
CONCEPT_POOL = [
    ("concepts/confirmation-bias.md",       "Psychology · Daniel Kahneman",       "confirmation-bias"),
    ("frameworks/stoicism.md",              "Philosophy · Epictetus · Aurelius",   "stoicism-control"),
    ("concepts/growth-mindset.md",          "Psychology · Carol Dweck",            "growth-mindset"),
    ("frameworks/atomic-habits.md",         "Personal Development · James Clear",  "atomic-habits"),
    ("frameworks/logotherapy.md",           "Psychology · Viktor Frankl",          "logotherapy"),
    ("concepts/cognitive-biases.md",        "Psychology · Kahneman / Tversky",     "cognitive-biases"),
    ("concepts/self-knowledge.md",          "Philosophy · Psychology",             "self-knowledge"),
    ("frameworks/first-principles-thinking.md", "Philosophy · 李善友 (Li Shanyu)", "first-principles"),
    ("concepts/mental-models.md",           "Philosophy · Charlie Munger",         "mental-models"),
    ("frameworks/strategic-thinking.md",    "Strategy · Sun Tzu",                  "strategic-thinking"),
    ("concepts/independent-thinking.md",    "Essay · Paul Graham (2020)",           "independent-thinking"),
]

# Daily themes
THEMES = [
    "Seeing Clearly", "Inner Strength", "Deliberate Change", "Knowing Yourself",
    "Thinking Better", "Acting Wisely", "Building Resilience", "Finding Meaning",
    "Breaking Patterns", "Living Intentionally",
]

# ── Scenario templates (expand as you ingest more sources) ──────────────────
SCENARIO_BANK = {
    "growth-mindset": {
        "business": {
            "title": "The Performance Review",
            "situation": "Your annual review highlights a weakness. Your first reaction is defensiveness — or dismissal. You tell yourself 'that's just not my strength.'",
            "whatHappens": "A fixed mindset treats the feedback as a verdict on who you are. A growth mindset treats it as a map of where to go next. The difference determines whether feedback helps you or just hurts.",
            "applicationSteps": [
                "After receiving any critical feedback, write it down without responding for 24 hours. Let it land before you defend.",
                "Ask: 'What would I do with this feedback if I genuinely believed I could improve?' Then do that.",
                "Reframe: replace 'I'm not good at X' with 'I haven't yet invested in developing X.' Notice how that changes your next move.",
                "Find one person who was once weak at the thing you're weak at, and now isn't. Study what they did."
            ]
        },
        "social": {
            "title": "Being Wrong in Public",
            "situation": "You made a confident claim at a dinner party. Someone politely corrected you. You felt your face flush. Your instinct was to qualify, deflect, or double down.",
            "whatHappens": "Fixed mindset treats public correction as a threat to status. Growth mindset treats it as free information. How you respond in that moment signals which world you're living in.",
            "applicationSteps": [
                "Practice saying: 'You're right, I got that wrong — thank you.' Say it cleanly, without qualification. Notice that the world doesn't end.",
                "After being corrected, ask a genuine follow-up question about the correct information. Curiosity dissolves embarrassment.",
                "Privately track how often you're corrected and on what topics. Patterns reveal real gaps.",
                "Model the behaviour you want in others: when you correct someone, do it gently and make it easy for them to update gracefully."
            ]
        },
        "intimate": {
            "title": "Compatibility vs Growth",
            "situation": "Your partner points out a pattern in your behaviour that they find hurtful. Your first impulse: 'That's just who I am. They knew this when they met me.'",
            "whatHappens": "Fixed mindset uses identity as a shield against the discomfort of change. But 'that's just who I am' is almost always a choice, not a fact.",
            "applicationSteps": [
                "When you hear yourself say 'that's just who I am' about a behaviour someone finds hurtful — write it down. Ask: 'Is this truly fixed, or have I just never really tried to change it?'",
                "Ask your partner: 'What would it look like if I changed this, even 20%? What would you notice?' Get specific. Specific is actionable.",
                "Choose one small version of the change to practise for two weeks. Report back. Growth in relationships is demonstrated, not declared.",
                "Separate identity from behaviour: 'I am a person who sometimes does X' is very different from 'I am X.' One can change; the other feels like it can't."
            ]
        }
    },
    "atomic-habits": {
        "business": {
            "title": "The Meeting Habit",
            "situation": "Every Monday you arrive to work intending to do deep work. By 10am you've been pulled into three 'quick' meetings and your morning is gone. This happens every week.",
            "whatHappens": "You're relying on willpower and intention to protect your best work time. But the environment hasn't changed, so neither has the outcome. Habits need architecture, not resolve.",
            "applicationSteps": [
                "Block 7:30–9:30am as 'No meetings' in your calendar every day. Make it a recurring event with a title others can see. Environment design beats willpower.",
                "Identify the cue for the bad habit (checking Slack immediately on arrival). Replace it with a deliberate trigger for the good one (making tea = deep work begins).",
                "Create a 'two-minute rule' for deep work: if you can start your most important task in under two minutes, do it before opening email.",
                "Track the streak. Even a simple ✓ on a notepad creates identity reinforcement: 'I am someone who protects my deep work.'"
            ]
        },
        "social": {
            "title": "The Friend You Keep Meaning to Call",
            "situation": "There's someone important to you who you haven't spoken to in months. You think of them often. You keep meaning to reach out. You haven't.",
            "whatHappens": "Maintenance of close relationships doesn't happen by intention alone — it requires habit architecture. Waiting until you 'feel like it' or have 'enough to say' means it doesn't happen.",
            "applicationSteps": [
                "Create a recurring reminder: the first Sunday of each month, send one genuine message to one person you've been meaning to contact. One message. Non-negotiable.",
                "Habit stack: every time you make your morning coffee, you send one short check-in to someone. The coffee is the cue.",
                "Lower the bar radically: 'Thinking of you' is a complete message. It doesn't need to be a conversation-starter. Connection is the goal, not performance.",
                "Make a list of 10 people you value. Rotate through them. The system removes the decision fatigue of 'who should I contact?'"
            ]
        },
        "intimate": {
            "title": "The Drift",
            "situation": "You and your partner used to talk differently. Somewhere in the busyness of life, the quality of your daily interactions became transactional — logistics, schedules, surface. You miss the connection.",
            "whatHappens": "Intimacy doesn't disappear dramatically — it drifts, one skipped conversation at a time. It also doesn't return dramatically. It returns the same way: one small, deliberate act at a time.",
            "applicationSteps": [
                "Introduce one daily ritual: 10 minutes at the end of each day where phones are away and you ask one question that isn't logistical. Start simple: 'What was the best part of your day?'",
                "Habit stack it onto something that already happens every day — dinner, making tea, getting into bed.",
                "Never cancel the ritual for less than a genuine emergency. Consistency is the message, not the content.",
                "Once a month, do something you used to do together early in the relationship. Nostalgia activates the identity of who you are to each other."
            ]
        }
    },
    "logotherapy": {
        "business": {
            "title": "The Meaningless Job",
            "situation": "You're good at your job. You're paid well. But you go home on Friday feeling hollow. The work doesn't feel like it matters. You can't tell if you should leave or if the problem is in you.",
            "whatHappens": "Frankl's insight: meaning can be found in three ways — through creating or contributing, through love or connection, or through the attitude we take toward unavoidable suffering. Most 'meaningless' jobs contain at least one of these, unnoticed.",
            "applicationSteps": [
                "Write: 'Who benefits from my work, specifically, and how?' If you can't answer this, the problem may be that you've never looked — not that it doesn't exist.",
                "Identify one person whose work you make easier or better. Make that person real and visible to yourself. Meaning often lives in specifics, not abstractions.",
                "If genuine meaning isn't findable, ask: 'Is this suffering worth enduring for what it enables elsewhere in my life?' That too is meaning — Frankl called it 'tragic optimism.'",
                "Ask the Viktor Frankl question directly: 'What is life asking of me right now?' Sometimes the answer isn't a new job — it's a new way of showing up to this one."
            ]
        },
        "social": {
            "title": "Supporting Someone in Crisis",
            "situation": "A friend is going through something genuinely terrible — illness, loss, failure. You want to help but don't know what to say. You default to platitudes. You can tell they're not landing.",
            "whatHappens": "Most people try to remove suffering — by minimising it ('it'll get better'), explaining it ('everything happens for a reason'), or fixing it. Frankl's insight: the more valuable thing is to help someone find meaning within it.",
            "applicationSteps": [
                "Ask: 'What do you think this is asking of you?' — gently, and only if the relationship allows it. This shifts from 'when will this end?' to 'what does this mean?'",
                "Don't rush to comfort. Sit with the difficulty first. 'This is genuinely hard' is often more valuable than reassurance.",
                "Ask what they need — not what you think they need. 'Do you want me to listen, or to help you think through options?' The question itself communicates care.",
                "If they're searching for meaning, don't provide it for them. Ask questions that help them find it: 'What matters most to you about getting through this?'"
            ]
        },
        "intimate": {
            "title": "When the Relationship is Hard",
            "situation": "You're in a difficult period with your partner — not dramatic, just persistently hard. You're wondering whether this is fixable, or whether you're holding on to something that's run its course.",
            "whatHappens": "Frankl: the question is never 'what do I want from this relationship?' but 'what does this relationship ask of me?' The frame shift from consumer to contributor often reveals the answer.",
            "applicationSteps": [
                "Ask: 'What do I uniquely offer this person that they wouldn't easily find elsewhere?' And: 'What do they offer me?' If you can't answer either, that's important information.",
                "Identify what you are avoiding: the difficult conversation, the acknowledgment, the change. Avoidance is almost always where meaning is hiding.",
                "Ask the Frankl question: 'What would I regret not having tried, if this ended?' Then try that thing. At least you'll know.",
                "If the relationship is genuinely hard but meaningful, ask: 'Can I choose to commit to this fully for 90 days and see who we become?' Meaning requires commitment. Commitment requires a choice."
            ]
        }
    }
}

# ── Main ────────────────────────────────────────────────────────────────────

def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_entries(entries):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def today_str():
    return date.today().isoformat()

def already_has_today(entries):
    today = today_str()
    return any(e['date'] == today for e in entries)

def read_wiki_file(rel_path):
    full = os.path.join(WIKI, rel_path)
    if not os.path.exists(full):
        return None
    with open(full, 'r', encoding='utf-8') as f:
        return f.read()

def extract_tagline(content):
    m = re.search(r'\*\*Key Insight:\*\*\s*(.+?)(?:\n|$)', content)
    if m:
        t = m.group(1).strip().rstrip('.')
        return t[:120] + ('…' if len(t) > 120 else '')
    # fallback: first non-empty paragraph after the title
    lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('---') and not l.startswith('|')]
    for line in lines[:5]:
        if len(line) > 40:
            return line[:120]
    return "A key insight from your Human Behaviour wiki."

def extract_key_points(content):
    """Pull bullet points and list items from the content."""
    points = []
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('- ') and len(line) > 30:
            clean = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', line[2:])
            clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)
            if len(clean) > 40:
                points.append(clean[:200])
        if len(points) >= 4:
            break
    if len(points) < 2:
        # Extract from paragraphs
        paragraphs = [p.strip() for p in re.split(r'\n\n+', content) if len(p.strip()) > 60]
        for para in paragraphs:
            if not para.startswith('#') and not para.startswith('|') and not para.startswith('---'):
                clean = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', para)
                clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean)
                clean = clean.replace('\n', ' ').strip()
                if 50 < len(clean) < 250:
                    points.append(clean)
            if len(points) >= 4:
                break
    return points[:4] if points else ["See your wiki for the full concept breakdown."]

def get_strategic_steps(concept_id):
    # Return generic strategic steps; extend this per concept
    defaults = {
        "first-principles": [
            "Each morning, pick one assumption you've been treating as fact. Ask: 'Is this actually true, or is it a continuity assumption?' Write the answer.",
            "Before any major decision, ask: 'What am I treating as a first principle here that I've never examined?'",
            "Use the decomposition method: break any 'impossible' challenge into components and ask which parts are genuinely fixed vs. conventional.",
            "Ask weekly: 'What is everyone around me accepting without question? Is there a hidden axiom I should be challenging?'"
        ],
        "self-knowledge": [
            "Journal for 10 minutes each evening on one question: 'What did I feel today that I didn't fully acknowledge at the time?'",
            "Seek one piece of genuinely honest feedback this week — from someone who will tell you what you need to hear, not what you want to hear.",
            "Notice your emotional reactions: they are data about your values, not just noise. Ask 'what does this reaction tell me about what I care about?'",
            "Map the gap: 'What do I say I value vs. what does my behaviour over the last week actually show I value?'"
        ],
        "mental-models": [
            "Pick one field outside your expertise this month. Find its single most important foundational idea. How does it apply to your current challenges?",
            "When stuck on a problem, deliberately ask: 'What would a biologist say? An economist? A philosopher?' Run it through multiple lenses.",
            "Build your personal 'latticework': keep a list of the 10 mental models you use most. Are they diverse, or are they all from the same domain?",
            "Practice inversion: instead of 'How do I achieve X?', ask 'What would guarantee I fail at X?' Then eliminate those conditions."
        ],
        "strategic-thinking": [
            "Each morning: identify one thing you're trying to control that you can't. Redirect that energy to what you actually can influence.",
            "Before entering any high-stakes situation, apply Sun Tzu's Five Factors: Is my timing right? Do I know the terrain? Am I the right person for this?",
            "Ask weekly: 'Where am I fighting battles that don't need to be fought? What would winning without fighting look like here?'",
            "Before a difficult conversation: 'What outcome do I actually want? What is the minimum I can do to achieve it?'"
        ],
    }
    return defaults.get(concept_id, [
        "Start with observation before action: spend one day simply noticing where this concept appears in your life.",
        "Choose one specific context this week where you will consciously apply this concept.",
        "At the end of the week, write: 'What changed when I applied this? What did I notice?'",
        "Share one insight from this concept with someone you trust. Teaching it solidifies it."
    ])

def build_concept(pool_entry, entries):
    rel_path, source, concept_id = pool_entry
    content = read_wiki_file(rel_path)

    tagline = extract_tagline(content) if content else "A key insight from your Human Behaviour wiki."
    key_points = extract_key_points(content) if content else ["See your wiki for the full breakdown."]
    title = rel_path.split('/')[-1].replace('.md','').replace('-',' ').title()

    # Try to get title from content
    if content:
        m = re.search(r'^#\s+(.+?)(?:\s*\(.*?\))?\s*$', content, re.MULTILINE)
        if m:
            t = m.group(1).strip()
            if len(t) < 60:
                title = t

    strategic_steps = get_strategic_steps(concept_id)

    # Get scenarios
    scenarios_data = SCENARIO_BANK.get(concept_id, None)
    if not scenarios_data:
        # Build generic scenarios
        scenarios_data = {
            "business": {
                "title": "Professional Application",
                "situation": "You encounter a situation at work that this concept directly applies to.",
                "whatHappens": "Without awareness of this concept, the default response often makes things worse. With it, you have a strategic choice.",
                "applicationSteps": [
                    "Before reacting, pause and ask: how does this concept apply to what's happening right now?",
                    "Identify which aspect of the concept is most relevant to this specific situation.",
                    "Apply the concept deliberately and notice what changes.",
                    "Reflect afterward: what would have happened without this lens?"
                ]
            },
            "social": {
                "title": "Social Application",
                "situation": "A recurring social situation where this concept could shift the dynamic.",
                "whatHappens": "Social interactions often run on autopilot. This concept gives you a deliberate tool to engage differently.",
                "applicationSteps": [
                    "Notice when this concept applies in your next social interaction.",
                    "Choose one specific application of it and try it consciously.",
                    "Observe the other person's response. What changed?",
                    "Ask yourself afterward: what did I learn about them and myself?"
                ]
            },
            "intimate": {
                "title": "Intimate Relationship Application",
                "situation": "The concept applied to your closest relationships.",
                "whatHappens": "Intimate relationships are where our deepest patterns play out. This concept offers a tool for conscious engagement.",
                "applicationSteps": [
                    "Identify one pattern in your relationship where this concept might apply.",
                    "Share the concept with your partner and explore it together.",
                    "Choose one concrete thing to try differently this week.",
                    "Check in at the end of the week: what shifted?"
                ]
            }
        }

    return {
        "id": concept_id,
        "title": title,
        "source": source,
        "tagline": tagline,
        "keyPoints": key_points,
        "strategicSteps": strategic_steps,
        "scenarios": scenarios_data
    }

def pick_two_concepts(entries):
    """Pick 2 concepts not used in the last 7 days."""
    recent_ids = set()
    for e in sorted(entries, key=lambda x: x['date'], reverse=True)[:7]:
        for c in e.get('concepts', []):
            recent_ids.add(c.get('id',''))

    available = [p for p in CONCEPT_POOL if p[2] not in recent_ids]
    if len(available) < 2:
        available = CONCEPT_POOL

    return random.sample(available, min(2, len(available)))

def main():
    entries = load_entries()

    if already_has_today(entries):
        print(f"✓ Entry for {today_str()} already exists. Nothing to do.")
        return

    day_num = len(entries) + 1
    theme = THEMES[(day_num - 1) % len(THEMES)]
    chosen = pick_two_concepts(entries)

    concepts = [build_concept(c, entries) for c in chosen]

    new_entry = {
        "date": today_str(),
        "day": day_num,
        "theme": theme,
        "concepts": concepts
    }

    entries.append(new_entry)
    save_entries(entries)
    print(f"✓ Day {day_num} entry generated for {today_str()}: {theme}")
    print(f"  Concepts: {' · '.join(c['title'] for c in concepts)}")

if __name__ == '__main__':
    main()
