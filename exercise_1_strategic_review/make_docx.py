from docx import Document
from docx.shared import Pt, RGBColor, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Page margins ────────────────────────────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Inches(0.9)
section.bottom_margin = Inches(0.9)
section.left_margin   = Inches(1.1)
section.right_margin  = Inches(1.1)

# ── Helpers ──────────────────────────────────────────────────────────────────
def heading(text, level=1, space_before=14, space_after=4):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    return p

def body(text, bold_prefix=None, space_before=2, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if bold_prefix:
        run = p.add_run(bold_prefix)
        run.bold = True
        run.font.size = Pt(11)
        p.add_run(text)
    else:
        run = p.add_run(text)
        run.font.size = Pt(11)
    return p

def rule():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'CCCCCC')
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p

def speaker_note(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.left_indent  = Inches(0.25)
    run = p.add_run(f"[{text}]")
    run.italic = True
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    return p

# ── HEADER BLOCK ─────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
r = p.add_run("MERIDIAN TECHNOLOGIES")
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
r.font.bold = True

p2 = doc.add_paragraph()
p2.paragraph_format.space_after = Pt(2)
r2 = p2.add_run("Annual Board Strategic Review  ·  May 2026")
r2.font.size = Pt(9)
r2.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

p3 = doc.add_paragraph()
p3.paragraph_format.space_after = Pt(2)
r3 = p3.add_run("Presenter: Catherine Park, President & CEO")
r3.font.size = Pt(9)
r3.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

rule()

# ── HEADLINE ─────────────────────────────────────────────────────────────────
h = doc.add_paragraph()
h.paragraph_format.space_before = Pt(10)
h.paragraph_format.space_after  = Pt(12)
h.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = h.add_run(
    "Meridian's enterprise franchise is stronger than ever — "
    "and we must decide, this year, whether AI transforms it or disrupts it."
)
run.bold = True
run.font.size = Pt(13)

rule()

# ── FRAMING ──────────────────────────────────────────────────────────────────
heading("Opening  (30 seconds)", level=2, space_before=10)
body(
    "I want to use my five minutes to give you an honest picture of where we stand, "
    "name the three issues that should dominate our conversation today, and then make "
    "one ask of this board. Everything else in the deck supports these points."
)
speaker_note("Speak slowly. Make eye contact. Do not rush past this.")

# ── CHART ────────────────────────────────────────────────────────────────────
heading("The Shape of Our Business  (60 seconds)", level=2, space_before=12)
body(
    "Before I get to the issues, I want you to see one chart — because it makes the "
    "strategic situation more legible than any paragraph I could write."
)

try:
    doc.add_picture(
        "/home/user/UCB-Class/exercise_1_strategic_review/meridian_chart.png",
        width=Inches(5.8)
    )
    last_para = doc.paragraphs[-1]
    last_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    cr = cap.add_run("Figure 1: ARR mix shift (left) and NRR by segment, Q1 2024 – Q4 2025 (right)")
    cr.italic = True
    cr.font.size = Pt(9)
    cr.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
except Exception as e:
    body(f"[Chart: meridian_chart.png — {e}]")

body(
    "The left panel shows that three years ago SMB was our largest segment at 38% of ARR. "
    "Today it is 13% and shrinking. Enterprise has grown from 27% to 40%. "
    "That mix shift is real progress — and it is the result of deliberate strategy."
)
body(
    "The right panel shows why the shift isn't finished. Enterprise NRR holds at 125%. "
    "Mid-market NRR has drifted from 108% to 102% and is approaching the flatline. "
    "SMB is at 84% — structurally contracting. "
    "These three lines tell you everything about the urgency of what follows."
)
speaker_note("Pause here. Let the board look at the chart for 10 seconds before continuing.")

rule()

# ── ISSUE 1 ──────────────────────────────────────────────────────────────────
heading("Issue 1 — The AI gap is real and the window is narrowing  (75 seconds)", level=2, space_before=12)
body(
    "When I joined fourteen months ago, I said we were behind on AI and the gap was widening. "
    "That was true. Here is what has changed and what hasn't."
)
body(
    "What has changed: ",
    bold_prefix="What has changed:  ",
)
p = doc.add_paragraph(style='List Bullet')
p.paragraph_format.space_after = Pt(3)
p.add_run("AI Copilot reached GA in September. We have 710 paying seats and a 44% attach rate on Q4 enterprise renewals — above our 40% target.")
p = doc.add_paragraph(style='List Bullet')
p.paragraph_format.space_after = Pt(3)
p.add_run("The Helio acquisition closed in November. 26 of 28 engineers are still with us. The agent orchestration architecture that would have taken us six months to design, we got on day one.")
p = doc.add_paragraph(style='List Bullet')
p.paragraph_format.space_after = Pt(8)
p.add_run("Copilot generated $3.5M in 2025 ARR. Small. But the attach rate suggests the monetization model works.")

body(
    "What hasn't changed: ",
    bold_prefix="What hasn't changed:  ",
)
p = doc.add_paragraph(style='List Bullet')
p.paragraph_format.space_after = Pt(3)
p.add_run("Asana shipped its full agent suite in November and has bundled AI into its standard tier — it is no longer an upsell, it is table stakes.")
p = doc.add_paragraph(style='List Bullet')
p.paragraph_format.space_after = Pt(3)
p.add_run("Monday is now larger than us by ARR. ClearAI Work raised $120M at a $1B+ valuation.")
p = doc.add_paragraph(style='List Bullet')
p.paragraph_format.space_after = Pt(8)
p.add_run("Atlassian announced agentic Jira last month. They will be in our enterprise deals directly — a new competitive front we did not have twelve months ago.")

body(
    "Our GTM efficiency is also declining: magic number dropped from 1.20 to 0.92 over eight quarters "
    "and CAC payback has extended from 18 to 22 months. We are spending more to grow less. "
    "That compression will get worse before it gets better if competitors continue to bundle AI at no incremental cost."
)
speaker_note("Deliver 'Atlassian' line with weight — it is the newest and most underappreciated risk.")

rule()

# ── ISSUE 2 ──────────────────────────────────────────────────────────────────
heading("Issue 2 — Mid-market is approaching a tipping point  (60 seconds)", level=2, space_before=12)
body(
    "Mid-market is 47% of our ARR — $194 million — and its NRR just crossed below 103%. "
    "At 102%, mid-market is barely self-sustaining from the existing base. "
    "New logo acquisition efficiency in that segment is declining alongside the overall magic number."
)
body(
    "The structural pressure is specific: mid-market customers want two things we have been slow to deliver. "
    "First, AI features — and competitors are giving them away bundled. "
    "Second, resource management, which has been the top-three ask in our customer advisory board "
    "for two years running and which we have deferred twice in favor of AI work. "
    "We are deferring the features that keep mid-market customers to invest in features that win new enterprise logos. "
    "That is not necessarily wrong — but it is a tradeoff we should be explicit about."
)
body(
    "The 2026 roadmap resurrects resource management for Q2. If mid-market NRR dips below 100% before that ships, "
    "we will have a more serious retention problem on our hands. I am watching this line every month."
)
speaker_note("This is the issue board members from a SaaS background will fixate on. Be ready for NRR questions.")

rule()

# ── ISSUE 3 ──────────────────────────────────────────────────────────────────
heading("Issue 3 — Our ability to execute depends on people decisions we must make now  (45 seconds)", level=2, space_before=12)
body(
    "Our October employee survey — 81% response rate across 2,402 employees — surfaced two risks "
    "I want this board to understand."
)
body(
    "First, 31% of engineering responses cited roadmap thrash as their top concern. "
    "Three AI pivots in eighteen months. The third pivot was right — Copilot is at GA and the Helio "
    "architecture is working. But the organization will not trust this direction until we demonstrate "
    "that it sticks. The board's approval of a clear 2026–2028 plan today is part of how we do that."
)
body(
    "Second, 27% of senior engineers flagged compensation falling behind market. "
    "Our People team estimates 15 to 25 senior engineers are at flight risk in Q1 2026. "
    "Separately, the Helio team — the 28 people our entire agentic roadmap depends on — "
    "hits their first compensation cliff this year. "
    "If we lose them, the CPO's roadmap is exposed by 15 months."
)
body(
    "I plan to address the comp refresh in Q1. I want the board to know it is coming and why."
)
speaker_note("Keep this section tight. Board does not need the full survey — just the two numbers.")

rule()

# ── ASK ──────────────────────────────────────────────────────────────────────
heading("My One Ask  (30 seconds)", level=2, space_before=12)
body(
    "I will present a full 2026–2028 strategic plan at Investor Day on March 11th. "
    "Today I am asking this board for one thing: "
)

ask = doc.add_paragraph()
ask.paragraph_format.space_before = Pt(6)
ask.paragraph_format.space_after  = Pt(6)
ask.paragraph_format.left_indent  = Inches(0.3)
ask.alignment = WD_ALIGN_PARAGRAPH.LEFT
r = ask.add_run(
    "Alignment on Meridian's strategic identity — "
    "are we an enterprise-grade agentic work platform, or a multi-segment collaboration tool? "
    "The answer to that question determines our R&D priorities, our pricing model, our sales motion, "
    "and what we say to investors in six weeks."
)
r.bold = True
r.font.size = Pt(11.5)

body(
    "I have a point of view. I want to hear yours. Everything else today is context for that conversation."
)
speaker_note("Stop here. Do not fill the silence. Let the board respond.")

rule()

# ── FOOTER NOTE ──────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(10)
r = p.add_run(
    "Speaker notes appear in [brackets] in italics. Prepared remarks are approximately 5 minutes at a measured pace. "
    "Source data: meridian_financials_2022_2025.csv, meridian_kpis_2024.csv, meridian_segments_overview.md, "
    "meridian_earnings_call_q4_2025.txt, meridian_employee_survey_2025.md, meridian_product_roadmap_2025.md."
)
r.font.size = Pt(8.5)
r.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
r.italic = True

doc.save("/home/user/UCB-Class/exercise_1_strategic_review/board_opening_remarks.docx")
print("Saved.")
