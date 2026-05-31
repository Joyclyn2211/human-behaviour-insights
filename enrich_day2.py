"""One-off: replace Day 2 (2026-05-31) concepts with in-depth content."""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data', 'entries.json')

with open(DATA, 'r', encoding='utf-8') as f:
    entries = json.load(f)

cognitive_biases = {
    "id": "cognitive-biases",
    "title": "Cognitive Biases",
    "source": "Psychology · Kahneman & Tversky",
    "tagline": "Your brain runs on shortcuts that were brilliant for survival and are quietly sabotaging your modern decisions.",
    "keyPoints": [
        "The mind has two systems (Kahneman). System 1 is fast, automatic, emotional — it generates instant impressions and is the source of almost every bias. System 2 is slow, effortful, logical — but it's lazy and usually just rubber-stamps whatever System 1 already decided. Biases happen when System 2 fails to check System 1's work.",
        "Biases are not stupidity or carelessness. They are efficient heuristics — mental shortcuts that were adaptive in ancestral environments (snap threat-detection, fast social judgement) but misfire in a world of statistics, markets, and strangers. Intelligent people are NOT more protected; they're often better at constructing clever justifications for biased conclusions.",
        "The most consequential biases cluster in predictable places: how we judge other people (fundamental attribution error, halo effect), how we handle gains and losses (loss aversion, sunk cost), how we estimate likelihood (availability, representativeness), and how we defend what we already believe (confirmation bias, anchoring).",
        "You cannot eliminate biases by knowing about them — System 1 operates below conscious control. Awareness alone barely helps. What works is STRUCTURE: checklists, outside views, deliberate friction, and decision rules that don't depend on in-the-moment judgement.",
        "The bias blind spot: we readily see bias in others and feel ourselves to be the rational exception. This meta-bias is why 'just be objective' never works — your sense of being objective is itself produced by System 1."
    ],
    "strategicSteps": [
        "Build decision friction for anything important. Before a consequential choice, force a 24-hour gap and write down your reasoning. This recruits System 2 into a decision System 1 wants to make instantly.",
        "Use the 'outside view'. Instead of asking 'how will MY project go?' (optimism bias guaranteed), ask 'how do projects like this usually go?' Base rates beat gut feeling. Kahneman calls this the single most useful debiasing move.",
        "Run a pre-mortem. Before committing, imagine it's a year later and the decision failed catastrophically. Write the story of how. This surfaces the risks confirmation bias and optimism bias hid from you.",
        "Separate the person from the situation. When judging someone's behaviour, deliberately ask 'what situation could make a reasonable person act this way?' before concluding it's their character. This directly counters the fundamental attribution error.",
        "Make the bias work FOR you. Loss aversion (losses hurt ~2x more than gains feel good) is a tool: stake money you'll lose if you skip the gym; the pain of loss out-motivates the pull of comfort."
    ],
    "scenarios": {
        "business": {
            "title": "The Sunk-Cost Project That Won't Die",
            "situation": "Your team has spent 18 months and a large budget on a product feature. The data now clearly shows customers don't want it. Yet every meeting ends with 'we've come too far to stop now — let's push through.' More money goes in.",
            "whatHappens": "This is the sunk cost fallacy compounded by loss aversion and confirmation bias. The money already spent is gone regardless — it should be irrelevant to the forward decision. But abandoning the project feels like 'losing' the investment, so the team keeps throwing good resources after bad, and selectively highlights any data scrap that suggests it might still work.",
            "applicationSteps": [
                "Reframe the question to erase the past: 'Knowing only what we know today, with this budget, would we START this project right now?' If no, the sunk cost is talking.",
                "Make the loss explicit and bounded: 'We will lose the 18 months either way. The only real choice is whether we also lose the next 6.'",
                "Assign someone to build the strongest case for KILLING it. Without a designated challenger, confirmation bias guarantees only pro-continuation evidence gets aired.",
                "Set a kill-criterion in advance for the NEXT project: 'If by month 3 metric X isn't above Y, we stop — decided now, while we're unbiased.'"
            ]
        },
        "social": {
            "title": "The Halo Effect in a New Acquaintance",
            "situation": "You meet someone polished, articulate, and confident at a networking event. You immediately assume they're also competent, trustworthy, and successful — and you start agreeing with their opinions more readily than you would with anyone else.",
            "whatHappens": "The halo effect: one salient positive trait (charisma) bleeds into unrelated judgements (competence, honesty). It's how confident frauds succeed and quiet experts get overlooked. Your System 1 built an entire character profile from a 30-second impression, and confirmation bias will now defend it.",
            "applicationSteps": [
                "Separate the traits you've actually observed from the ones you're inferring. 'I've seen they're articulate. I have zero evidence yet about whether they're competent or honest.'",
                "Look specifically for disconfirming evidence — the thing the halo is hiding. Charismatic people get fewer hard questions; ask one.",
                "Delay consequential trust. Charisma is real-time; reliability only shows over repeated interactions. Let time, not first impression, calibrate your judgement.",
                "Invert it for the overlooked: when someone is awkward or unpolished, deliberately ask 'what might this person be excellent at that their delivery is hiding?'"
            ]
        },
        "intimate": {
            "title": "The Fundamental Attribution Error in Conflict",
            "situation": "Your partner forgets something important to you. Your instant interpretation: 'They don't care. They're inconsiderate.' But last week when YOU forgot something, you explained it as 'I was overwhelmed and exhausted' — a situation, not a flaw.",
            "whatHappens": "The fundamental attribution error: we explain others' behaviour by their character ('they're selfish') and our own identical behaviour by circumstances ('I was busy'). This asymmetry is the engine of most relationship conflict — each person experiences themselves as reasonable and the other as flawed.",
            "applicationSteps": [
                "Catch the character verdict as it forms ('they ARE inconsiderate') and convert it into a situational question ('what was going on for them today?').",
                "Apply the symmetry test: 'When I did this exact thing, what was my explanation? Would that same explanation be available to them?' Usually it is.",
                "Lead with the situation, not the accusation: 'Hey, you forgot X — was something going on?' opens a door; 'You never think about me' slams it.",
                "Build a shared rule for the relationship: 'We assume good intent and ask about circumstances before assigning blame.' Name it in a calm moment so you can both invoke it in a heated one."
            ]
        }
    }
}

logotherapy = {
    "id": "logotherapy",
    "title": "Logotherapy",
    "source": "Psychology · Viktor Frankl",
    "tagline": "The primary human drive isn't pleasure or power — it's meaning. And meaning can be found even in suffering you cannot escape.",
    "keyPoints": [
        "Frankl developed logotherapy partly in Nazi concentration camps, where he observed who survived and who gave up. His conclusion: those who had a 'why' — a person to return to, a book to finish, a task only they could do — endured 'almost any how.' Meaning, not comfort, was the difference between collapse and survival.",
        "Meaning is found in three ways, not invented from thin air: (1) through WORK or creating something — a contribution, a deed; (2) through LOVE or encountering someone — connection, beauty, experience; (3) through the ATTITUDE we take toward unavoidable suffering. The third is the radical one: when you can't change a situation, you can still choose your stance toward it, and that choice itself creates meaning.",
        "The 'existential vacuum' is Frankl's diagnosis of modern malaise — a feeling of emptiness, boredom, and 'what's the point?' that appears when survival is handled but meaning is absent. He argued much depression, addiction, and aggression grows in this vacuum. Affluence doesn't fill it; only meaning does.",
        "Self-transcendence is the mechanism: the more you aim directly AT happiness or meaning, the more they elude you. They arrive as by-products of devoting yourself to something — or someone — beyond yourself. 'Don't aim at success. The more you aim at it and make it a target, the more you are going to miss it.'",
        "'Tragic optimism' is saying yes to life despite the 'tragic triad' — pain, guilt, and death. Not toxic positivity that denies suffering, but a hard-won capacity to find meaning within it. This is the opposite of both despair and forced cheerfulness."
    ],
    "strategicSteps": [
        "Ask the reframed question. Frankl said the question is never 'what do I want from life?' but 'what is life asking of ME, right now, in this specific situation?' Apply it to whatever you're facing today — it shifts you from passive consumer to responsible agent.",
        "Locate your three sources weekly. Write one answer each for: what did I CREATE or contribute? Who did I genuinely CONNECT with? What unavoidable difficulty did I face, and what STANCE did I take? Gaps reveal where meaning is thin.",
        "Practise 'dereflection' for anxiety. When you're trapped overthinking yourself (your performance, your happiness, your symptoms), deliberately redirect attention OUTWARD toward a task or person. Meaning lives outside the self, not in self-monitoring.",
        "Find the 'why' before the 'how'. Before a hard goal or grim period, get specific about what it's FOR — who benefits, what it enables, who you become. A concrete why makes a brutal how survivable.",
        "Reframe unavoidable suffering as a question of stance. When something genuinely cannot be changed, ask: 'Given that this is happening, what would it mean to meet it well? What is the most meaningful way to carry this?'"
    ],
    "scenarios": {
        "business": {
            "title": "The Hollow Success",
            "situation": "You're good at your job and well paid. But Friday evenings you feel empty. The work doesn't feel like it matters. You can't tell whether you should quit, or whether the emptiness would follow you anywhere.",
            "whatHappens": "This is the existential vacuum in a professional skin. Competence and salary handle survival but don't supply meaning. Frankl's three sources let you diagnose precisely what's missing: most 'meaningless' jobs actually contain meaning that's gone unnoticed — or reveal a genuine misalignment worth acting on.",
            "applicationSteps": [
                "Trace the contribution: 'Who specifically is better off because I did my work well this week?' Make it a real person, not an abstraction. Meaning hides in specifics — the colleague you unblocked, the customer you served.",
                "Test the three sources against the job: Is there room to CREATE? To CONNECT with people you value? If both are genuinely absent and unfixable, that's real data — not a character flaw in you.",
                "Before quitting, try changing your stance for two weeks: approach the same tasks asking 'what would doing this meaningfully look like?' Sometimes the job isn't the problem; the autopilot is.",
                "If the vacuum persists after honest effort, ask the Frankl question: 'What is life asking of me now?' The answer might be a new role — or a meaningful pursuit OUTSIDE work that the job exists to fund."
            ]
        },
        "social": {
            "title": "Supporting a Friend Through the Unfixable",
            "situation": "A friend is facing something genuinely terrible and irreversible — a terminal diagnosis, a devastating loss. You desperately want to help but every comforting phrase ('it'll be okay', 'everything happens for a reason') feels hollow, and you can see it landing badly.",
            "whatHappens": "Most of us instinctively try to REMOVE suffering — minimise it, explain it, or fix it. But this suffering can't be removed, so those moves fail and can even wound. Frankl's insight: when you can't change the situation, the gift you can offer is helping someone find meaning WITHIN it, and simply not abandoning them in it.",
            "applicationSteps": [
                "Stop trying to fix or reframe their pain. Sit in it with them. 'This is genuinely terrible, and I'm here' is worth more than any silver lining.",
                "Don't supply meaning — that's theirs to find. Instead ask gently: 'What matters most to you in how you face this?' or 'Who or what is helping you hold on?'",
                "Honour the dignity of their stance. Frankl saw that HOW a person bears unavoidable suffering can be a profound achievement. Name it when you see it: 'The way you're carrying this is remarkable.'",
                "Be the concrete 'why'. Often a person's reason to keep going is the people who need them. Your steady presence can itself be part of their meaning — show up reliably, not just dramatically."
            ]
        },
        "intimate": {
            "title": "The Relationship That's Become Hard",
            "situation": "You're in a persistently difficult stretch with your partner — not explosive, just heavy and depleting. You keep asking 'is this still making me happy?' and the honest answer some days is no. You're wondering whether to hold on or let go.",
            "whatHappens": "Frankl would gently challenge the question itself. 'What do I want FROM this relationship?' frames you as a consumer of happiness. 'What is this relationship asking of me — and what meaning could I create in it?' frames you as a participant. The shift from extracting to contributing often reveals whether there's life left to build, or whether it's genuinely run its course.",
            "applicationSteps": [
                "Switch the question for one week: instead of 'am I happy?', ask 'what does showing up well in this relationship ask of me right now?' Notice what that surfaces.",
                "Find what you're avoiding. Meaning in relationships usually hides behind the conversation you're not having, the apology you're withholding, the change you're resisting. Name it.",
                "Apply self-transcendence: stop aiming at 'being happy together' directly. Aim instead at a shared project, caring well for each other, or a difficulty you face as a team — happiness tends to return as a by-product.",
                "Use the regret test for clarity: 'If this ended, what would I regret not having genuinely tried?' Try exactly that — fully, for a defined period. Then you'll have an answer earned through commitment, not guesswork."
            ]
        }
    }
}

for e in entries:
    if e["date"] == "2026-05-31":
        e["concepts"] = [cognitive_biases, logotherapy]

with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

print("Day 2 enriched. Concepts:", [c["title"] for e in entries if e["date"]=="2026-05-31" for c in e["concepts"]])
