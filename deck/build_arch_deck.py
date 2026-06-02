# Task Management System | Software Architecture deck (SEN3006).
# Professional academic presentation. Black-and-white Swiss editorial system
# (V2 presentations skill): numbered sections + TOC, substantive slides written
# to be presented conversationally, real GUI screenshots as evidence, speaker
# notes on every slide. Built with python-pptx. Build: python build_arch_deck.py
import os, re
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
DIA = os.path.join(HERE, "_dia")          # high-res UML + real GUI screenshots
OUT = os.path.join(HERE, "Task-Management-System.pptx")

INK = RGBColor(0x0B, 0x0B, 0x0B); NEAR = RGBColor(0x16, 0x16, 0x16)
GRAY = RGBColor(0x6E, 0x6E, 0x6E); GRAYW = RGBColor(0x9A, 0x9A, 0x9A)
FAINT = RGBColor(0xB4, 0xB4, 0xB4); RULEW = RGBColor(0xDE, 0xDE, 0xDE)
RULEB = RGBColor(0x2E, 0x2E, 0x2E); WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CODEBG = RGBColor(0xF6, 0xF6, 0xF4); CODEBD = RGBColor(0xE3, 0xE3, 0xE3)
KW = RGBColor(0x82, 0x50, 0xDF); TYP = RGBColor(0x05, 0x50, 0xAE)
STR = RGBColor(0x0A, 0x7B, 0x33); NUM = RGBColor(0x05, 0x50, 0xAE); COM = RGBColor(0x6E, 0x77, 0x81)
FONT = "Inter"; MONO = "Consolas"
DPI = 200; SW, SH = 13.333, 7.5; M = 0.78; TOTAL = 28

prs = Presentation(); prs.slide_width = Emu(int(SW*914400)); prs.slide_height = Emu(int(SH*914400))
BLANK = prs.slide_layouts[6]

def slide(bg=WHITE):
    s = prs.slides.add_slide(BLANK); s.background.fill.solid(); s.background.fill.fore_color.rgb = bg; return s
def notes(s, txt):
    s.notes_slide.notes_text_frame.text = txt
def hline(s, x, y, w, color=RULEW, weight=1.0):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y), Inches(x+w), Inches(y))
    ln.line.color.rgb = color; ln.line.width = Pt(weight); ln.shadow.inherit = False; return ln
def _spc(r, pts): r.font._rPr.set("spc", str(int(pts*100)))
def text(s, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"): setattr(tf, m, 0)
    first = True
    for para in paras:
        runs = para if isinstance(para, list) else [para]
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False; p.alignment = align; meta = runs[0]
        if meta.get("space_before") is not None: p.space_before = Pt(meta["space_before"])
        if meta.get("space_after") is not None: p.space_after = Pt(meta["space_after"])
        if meta.get("line") is not None: p.line_spacing = meta["line"]
        for rd in runs:
            r = p.add_run(); r.text = rd["t"]
            f = r.font; f.name = rd.get("font", FONT); f.size = Pt(rd.get("size", 14)); f.bold = rd.get("bold", False); f.color.rgb = rd.get("color", INK)
            if rd.get("track"): _spc(r, rd["track"])
    return tf
def eyebrow(s, label, color=GRAY, speaker=None):
    text(s, M, 0.6, 9, 0.3, [{"t": label.upper(), "size": 11, "color": color, "bold": True, "track": 2.2}])
    if speaker:
        text(s, SW-M-6.5, 0.6, 6.5, 0.3, [{"t": speaker.upper(), "size": 9.5, "color": FAINT, "bold": True, "track": 1.6}], align=PP_ALIGN.RIGHT)
def title(s, t, color=INK, size=27, y=1.4): text(s, M, y, SW-2*M, 0.9, [{"t": t, "size": size, "color": color, "bold": True, "line": 1.05}])
def sub(s, t, color=GRAY, y=2.28, w=None): text(s, M, y, w or (SW-2*M), 0.7, [{"t": t, "size": 13, "color": color, "line": 1.35}])
def footer(s, n, on_dark=False):
    c = GRAYW if on_dark else FAINT
    text(s, M, SH-0.5, 8, 0.3, [{"t": "Task Management System  ·  SEN3006", "size": 8.5, "color": c, "track": 1.2}])
    text(s, SW-M-3, SH-0.5, 3, 0.3, [{"t": f"{n:02d} / {TOTAL}", "size": 8.5, "color": c, "track": 1.2}], align=PP_ALIGN.RIGHT)
def divider(s, kicker, statement, sub_text=None, speaker=None):
    text(s, M, 0.6, 9, 0.3, [{"t": kicker.upper(), "size": 11, "color": GRAYW, "bold": True, "track": 2.8}])
    if speaker:
        text(s, SW-M-6.5, 0.6, 6.5, 0.3, [{"t": speaker.upper(), "size": 9.5, "color": FAINT, "bold": True, "track": 1.6}], align=PP_ALIGN.RIGHT)
    hline(s, M, 3.0, SW-2*M, RULEB, 1.0)
    text(s, M, 3.3, SW-2*M, 1.8, [{"t": statement, "size": 36, "color": WHITE, "bold": True, "line": 1.06}])
    if sub_text:
        text(s, M, 5.5, SW-2.4*M, 0.9, [{"t": sub_text, "size": 14, "color": GRAYW, "line": 1.4}])
def defcard(s, rows, y=2.45, rstep=1.02, labw=2.45):
    """Academic definition rows: tracked caps label on the left, body on the right, hairline above each."""
    for i, (lab, body) in enumerate(rows):
        yy = y + i*rstep
        hline(s, M, yy, SW-2*M, RULEW, 1.0)
        text(s, M, yy+0.16, labw, 0.6, [{"t": lab, "size": 11, "color": INK, "bold": True, "track": 1.6}])
        text(s, M+labw+0.2, yy+0.13, SW-2*M-labw-0.2, rstep-0.06, [{"t": body, "size": 12.5, "color": GRAY, "line": 1.35}])
def cols3(s, triples, y=4.9, rule=True, lab_size=12.5, body_size=11):
    gap = 0.5; colw = (SW-2*M-2*gap)/3
    for i, (h, b) in enumerate(triples):
        x = M + i*(colw+gap)
        if rule: hline(s, x, y, colw, INK, 1.4)
        text(s, x, y+0.15, colw, 1.7, [[{"t": h, "size": lab_size, "color": INK, "bold": True, "space_after": 4}],
                                       [{"t": b, "size": body_size, "color": GRAY, "line": 1.3}]])
def listcol(s, x, y, w, label, items, gap=0.66, item_size=12.5):
    text(s, x, y, w, 0.3, [{"t": label, "size": 11, "color": GRAY, "bold": True, "track": 1.6}])
    hline(s, x, y+0.36, w, INK, 1.4)
    for i, it in enumerate(items):
        yy = y+0.54+i*gap
        text(s, x, yy+0.01, 0.3, 0.4, [{"t": "·", "size": 12, "color": INK, "bold": True}])
        text(s, x+0.3, yy, w-0.3, gap+0.1, [{"t": it, "size": item_size, "color": NEAR, "line": 1.18}])
def add_arrow(conn):
    ln = conn.line._get_or_add_ln(); t = ln.find(qn("a:tailEnd"))
    if t is None: t = ln.makeelement(qn("a:tailEnd"), {}); ln.append(t)
    t.set("type", "triangle"); t.set("w", "med"); t.set("len", "med")

# ---- syntax highlighter (Java) ----
JAVA_KW = {"class", "interface", "enum", "abstract", "extends", "implements", "new", "void", "return",
           "switch", "case", "int", "boolean", "public", "private", "protected", "static", "final",
           "this", "throws", "import", "package", "if", "else"}
_tok = re.compile(r'(//[^\n]*|"[^"]*"|[A-Za-z_][A-Za-z0-9_]*|\d+|\s+|.)')
def java_runs(line):
    if not line.strip(): return [{"t": " ", "color": INK}]
    out = []
    for m in _tok.finditer(line):
        t = m.group(0)
        if t.startswith("//"): col = COM
        elif t.startswith('"'): col = STR
        elif t.isspace(): col = INK
        elif t.isdigit(): col = NUM
        elif t in JAVA_KW: col = KW
        elif re.match(r'^[A-Z][A-Za-z0-9_]*$', t): col = TYP
        else: col = INK
        out.append({"t": t, "color": col})
    return out
def code(s, x, y, w, lines, size=12.5):
    lh = size/72*1.55; h = 0.36 + len(lines)*lh
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = CODEBG; sp.line.color.rgb = CODEBD; sp.line.width = Pt(1.0); sp.shadow.inherit = False
    try: sp.adjustments[0] = 0.04
    except Exception: pass
    tf = sp.text_frame; tf.word_wrap = False
    try: tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    except Exception: pass
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.28); tf.margin_right = Inches(0.2); tf.margin_top = Inches(0.16); tf.margin_bottom = Inches(0.12)
    first = True
    for ln in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False; p.line_spacing = 1.42; p.alignment = PP_ALIGN.LEFT
        for rd in java_runs(ln):
            r = p.add_run(); r.text = rd["t"]; r.font.name = MONO; r.font.size = Pt(size); r.font.color.rgb = rd["color"]
    return h
def img_contain(s, name, bx, by, bw, bh, border=RULEW):
    path = os.path.join(DIA, name)
    if not os.path.exists(path):
        text(s, bx, by+bh/2-0.2, bw, 0.4, [{"t": "[ "+name+" ]", "size": 12, "color": FAINT}], align=PP_ALIGN.CENTER); return
    iw, ih = Image.open(path).size; ratio = iw/ih
    if bw/bh > ratio: h = bh; w = bh*ratio
    else: w = bw; h = bw/ratio
    x = bx+(bw-w)/2; y = by+(bh-h)/2
    pic = s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    if border: pic.line.color.rgb = border; pic.line.width = Pt(0.75)
    pic.shadow.inherit = False

AR = "Abdul Rahman"; MH = "Mouhammad"
# ============================== SLIDES ==============================

# 01 TITLE -----------------------------------------------------------
s = slide(INK)
text(s, M, 0.6, 9, 0.3, [{"t": "SEN3006 · SOFTWARE ARCHITECTURE", "size": 11, "color": GRAYW, "track": 2.2}])
text(s, SW-M-6, 0.6, 6, 0.3, [{"t": "Project Presentation", "size": 11, "color": GRAYW, "track": 1.6}], align=PP_ALIGN.RIGHT)
text(s, M, 2.4, 11.8, 2.4, [[{"t": "Task Management System.", "size": 46, "color": WHITE, "bold": True, "line": 1.05}],
                            [{"t": "Factory Method + Strategy, in pure Java.", "size": 22, "color": FAINT, "bold": True, "line": 1.2, "space_before": 10}]])
hline(s, M, 5.95, SW-2*M, RULEB, 1.0)
text(s, M, 6.15, 7.7, 0.7, [{"t": "A task management system for software teams, designed around two classic design patterns.", "size": 12.5, "color": GRAYW, "line": 1.3}])
text(s, SW-M-5, 6.12, 5, 0.7, [[{"t": "Abdul Rahman Malak", "size": 12.5, "color": WHITE, "bold": True}],
                               [{"t": "Mouhammad Houjeirat", "size": 12.5, "color": WHITE, "bold": True, "space_before": 2}]], align=PP_ALIGN.RIGHT)
notes(s, "BOTH (open together).\n"
    "Good morning, and thank you. We are Abdul Rahman Malak and Mouhammad Houjeirat, presenting our SEN3006 project: a Task Management System written in pure Java.\n"
    "The system is built around two of the design patterns from the course: Factory Method, a creational pattern, and Strategy, a behavioural pattern. It has no external libraries, so the architecture is the only thing under evaluation.\n"
    "Our goal today is to define the problem clearly, justify why we chose these two patterns, walk through the architecture and the code, run the system live, and then evaluate it honestly. Abdul Rahman will take the table of contents.")

# 02 TABLE OF CONTENTS -----------------------------------------------
s = slide(WHITE); eyebrow(s, "Contents", speaker=AR); title(s, "What this presentation covers.")
toc = [("01", "Introduction & problem definition", "Abdul Rahman", "~3 min"),
       ("02", "The design patterns: Factory Method + Strategy", "Abdul Rahman + Mouhammad", "~5 min"),
       ("03", "Architecture & implementation", "Mouhammad", "~3 min"),
       ("04", "Live demonstration", "Both", "~3 min"),
       ("05", "Results, evaluation & conclusion", "Abdul Rahman", "~2 min")]
y0 = 2.55
for i, (n, t, who, tm) in enumerate(toc):
    y = y0 + i*0.78
    hline(s, M, y, SW-2*M, RULEW, 1.0)
    text(s, M, y+0.18, 0.7, 0.4, [{"t": n, "size": 15, "color": FAINT, "bold": True}])
    text(s, M+0.85, y+0.2, 8.2, 0.5, [{"t": t, "size": 14, "color": INK, "bold": True}])
    text(s, SW-M-3.6, y+0.16, 3.6, 0.5, [[{"t": who, "size": 10.5, "color": GRAY}],
                                         [{"t": tm, "size": 9.5, "color": FAINT, "space_before": 1}]], align=PP_ALIGN.RIGHT)
text(s, M, SH-0.76, SW-2*M, 0.4, [{"t": "Roughly 16 minutes of talk and demo, then questions. Both presenters take questions on the parts they led.", "size": 10.5, "color": FAINT, "track": 0.4}])
footer(s, 2)
notes(s, AR + ".\n"
    "Here is how the talk is organised, in five sections. Section one defines the problem and the requirements. Section two is the core of the talk: the two design patterns, why we chose them, and how we implemented them. Section three covers the architecture and how it maps to Java and to SOLID. Section four is a live demonstration of the running system. Section five is an honest evaluation and the conclusion.\n"
    "We split the sections between us, shown on the right. Please hold questions for the end unless something is unclear on screen. Section one is mine.")

# 03 SECTION 01 DIVIDER ----------------------------------------------
s = slide(INK)
divider(s, "Section 01", "Introduction & problem definition.",
        "The domain we chose, the objectives we set, and the two problems that shaped the whole design.", speaker=AR)
notes(s, AR + ".\n"
    "Section one. Before any pattern or class, we want to define the problem precisely, because the assignment is graded partly on a clear problem definition. I will cover the domain and our objectives, state the functional and non-functional requirements, and then show the two specific problems that the two patterns were chosen to solve.")

# 04 INTRODUCTION ----------------------------------------------------
s = slide(WHITE); eyebrow(s, "Introduction · background & objectives", speaker=AR); title(s, "Why a task management system?")
sub(s, "Software teams track many kinds of work. How that work is created and ordered is exactly where a design tends to decay over time.")
intro = [("The domain", "A tracker for a software team: bugs, features, and documentation tasks, each moving through a shared lifecycle from open to done."),
         ("The motivation", "Two recurring causes of code decay in such a system map cleanly onto two well known design patterns from the course."),
         ("Our objectives", "Support several task types and several orderings, and let new ones be added without editing existing, tested code."),
         ("The solution in one line", "One engine, three ways to run it, sixteen Java files, and zero external dependencies.")]
gap = 0.62; colw = (SW-2*M-gap)/2
for i, (h, b) in enumerate(intro):
    c, r = i % 2, i // 2; x = M+c*(colw+gap); y = 3.05+r*1.75
    hline(s, x, y, colw, RULEW, 1.0)
    text(s, x, y+0.14, colw, 1.5, [[{"t": h, "size": 14, "color": INK, "bold": True, "space_after": 4}],
                                   [{"t": b, "size": 12, "color": GRAY, "line": 1.35}]])
footer(s, 4)
notes(s, AR + ".\n"
    "Quick background and our objectives, top left to bottom right. The domain is a task tracker for a software team, handling three kinds of work: bugs, features, and documentation, all moving through one lifecycle.\n"
    "Our motivation was not to invent a pattern showcase. It was that two real, recurring sources of mess in this kind of system happen to match two patterns we studied. Our objective was concrete and testable: we should be able to add a new task type or a new ordering rule without editing any code that already works.\n"
    "And the solution, in one line: one engine, three entry points, sixteen files, no libraries. The next slide states the requirements formally.")

# 05 REQUIREMENTS ----------------------------------------------------
s = slide(WHITE); eyebrow(s, "Problem definition · requirements", speaker=AR); title(s, "What the system must do.")
gap = 0.7; colw = (SW-2*M-gap)/2
listcol(s, M, 2.45, colw, "FUNCTIONAL REQUIREMENTS", [
    "Create bug, feature, and documentation tasks.",
    "Order the list by priority, deadline, or severity.",
    "Move tasks through a validated lifecycle.",
    "Filter the list by status and summarise it."])
listcol(s, M+colw+gap, 2.45, colw, "NON-FUNCTIONAL REQUIREMENTS", [
    "Extensible: new types or orderings, no edits to existing code.",
    "Pure Java 8+, zero external dependencies.",
    "Runnable from the terminal: tests, console, and a GUI.",
    "Explainable: the design must hold up in a viva."])
hline(s, M, 6.15, SW-2*M, RULEW, 1.0)
text(s, M, 6.3, SW-2*M, 0.5, [{"t": "Two requirements drive the whole design: tasks are created in different ways, and the same list is ordered in different ways.", "size": 12, "color": INK, "bold": True, "line": 1.3}])
footer(s, 5)
notes(s, AR + ".\n"
    "On the left, the functional requirements: create the three task types, order the list three ways, move tasks through the lifecycle, and filter and summarise. These are the things a user can do.\n"
    "On the right, the non-functional requirements, which is where the architecture matters. The system must be extensible without editing existing code, must stay pure Java with no dependencies, must run from the terminal in three forms, and must be explainable, because we have to defend every design decision today.\n"
    "The line at the bottom is the key: two requirements drive everything. Different creation, and different ordering. The next two slides show why each is genuinely hard.")

# 06 PROBLEM 1 -------------------------------------------------------
s = slide(WHITE); eyebrow(s, "Problem definition · problem 1", speaker=AR); title(s, "Tasks have different creation logic.")
sub(s, "Each task type carries different fields and different defaults. Building them by hand couples every caller to the concrete classes.")
code(s, M, 3.05, SW-2*M, [
    'new BugTask(title, priority, "MEDIUM", "");          // severity + steps',
    'new FeatureTask(title, priority, 8, 5);              // effort + value',
    'new DocumentationTask(title, priority, "API", "Developers");'])
cols3(s, [("The smell", "Every entry point imports and names BugTask, FeatureTask, and DocumentationTask directly."),
          ("The consequence", "Adding a fourth type means finding and editing every place that creates a task."),
          ("What we need", "Create a task from a type identifier, without the caller naming a concrete class.")], y=5.05)
footer(s, 6)
notes(s, AR + ".\n"
    "Problem one is creation. Look at the three constructors. They are genuinely different: a bug needs a severity and reproduction steps, a feature needs an effort estimate and a business value, a documentation task needs a type and an audience. Each also has sensible defaults.\n"
    "The smell, bottom left: without a factory, every entry point, the console and the scripted demo, has to import and name each concrete class. The consequence, in the middle: when we add a fourth type, we have to hunt down and edit every one of those call sites. What we need, on the right: a way to create a task from a simple identifier, like the string BUG, without the caller knowing which class that is. That is exactly Factory Method, which we will get to in section two.")

# 07 PROBLEM 2 -------------------------------------------------------
s = slide(WHITE); eyebrow(s, "Problem definition · problem 2", speaker=AR); title(s, "Ordering depends on the context.")
sub(s, "The same task list is sorted differently at different moments. The list never changes; only the ordering rule does.")
code(s, M, 3.05, SW-2*M, [
    'switch (sortMode) {',
    '    case DEADLINE: /* sort by due date   */ break;',
    '    case SEVERITY: /* bugs first, by rank */ break;',
    '    case URGENT:   /* sort by priority    */ break;',
    '}'])
cols3(s, [("The smell", "One growing switch statement inside the manager carries every ordering rule."),
          ("The consequence", "Each new context edits tested code, which breaks the Open/Closed principle."),
          ("What we need", "Swap the ordering at runtime, and add new orderings without touching the manager.")], y=5.6)
footer(s, 7)
notes(s, AR + ".\n"
    "Problem two is ordering. Three real contexts: sprint planning sorts by deadline, incident response sorts by severity with bugs first, and the daily standup sorts by raw priority. The list of tasks is identical in all three; only the rule changes.\n"
    "The naive solution is the switch statement on screen, living inside the manager. The smell is that one method grows without bound. The consequence is that every new context forces us to open and edit code that already works and is already tested, which is a direct violation of the Open/Closed principle. What we need is to swap the ordering at runtime and add new orderings as separate units. That is the Strategy pattern. Hand back to me for section two, the patterns themselves.")

# 08 SECTION 02 DIVIDER ----------------------------------------------
s = slide(INK)
divider(s, "Section 02", "The design patterns.",
        "Two patterns chosen to match the two problems, plus a third that the task lifecycle gave us almost for free.", speaker=AR + " + " + MH)
notes(s, AR + ".\n"
    "Section two is the heart of the talk and the largest part of the grade. For each pattern we follow the same structure the report uses: the definition, why it suits this problem, its advantages, and how we actually implemented it. We start by mapping the two problems to the two patterns, then take Factory Method, then Strategy, then a short bonus on the lifecycle.")

# 09 PATTERN SELECTION -----------------------------------------------
s = slide(WHITE); eyebrow(s, "Pattern selection", speaker=AR); title(s, "Matching patterns to problems.")
sub(s, "We did not start from the patterns. We started from the two problems, and each one points to a single, well-fitted pattern.")
rows = [("Problem 1 · different creation logic", "Factory Method", "Creational", "Decouples the caller from the concrete task classes."),
        ("Problem 2 · context-dependent ordering", "Strategy", "Behavioral", "Makes the ordering a swappable object, chosen at runtime."),
        ("Bonus · the task lifecycle", "State (in an enum)", "Behavioral", "Each status declares its own legal transitions.")]
y0 = 3.05
for i, (prob, pat, cat, why) in enumerate(rows):
    y = y0 + i*1.12
    hline(s, M, y, SW-2*M, RULEW, 1.0)
    text(s, M, y+0.16, 4.3, 0.7, [{"t": prob, "size": 12.5, "color": GRAY, "line": 1.25}])
    text(s, M+4.6, y+0.13, 0.5, 0.4, [{"t": "→", "size": 15, "color": INK, "bold": True}])
    text(s, M+5.2, y+0.13, 3.0, 0.7, [[{"t": pat, "size": 15, "color": INK, "bold": True}],
                                      [{"t": cat + " pattern", "size": 10, "color": FAINT, "space_before": 1}]])
    text(s, M+8.5, y+0.18, SW-2*M-8.5, 0.7, [{"t": why, "size": 11.5, "color": GRAY, "line": 1.25}])
footer(s, 9)
notes(s, AR + ".\n"
    "This slide is the bridge. Reading each row left to right: problem one, different creation logic, points to Factory Method, a creational pattern, which decouples the caller from the concrete task classes. Problem two, context-dependent ordering, points to Strategy, a behavioural pattern, which makes each ordering a swappable object chosen at runtime.\n"
    "The third row is a bonus we did not have to do. The task lifecycle is naturally a state machine, so we encoded the State pattern inside a single enum. We picked the domain precisely because these mappings are natural, not forced. Now the detail, starting with Factory Method.")

# 10 FACTORY METHOD · definition & rationale -------------------------
s = slide(WHITE); eyebrow(s, "Pattern 1 · Factory Method", speaker=AR); title(s, "Factory Method, and why it fits.")
defcard(s, [
    ("DEFINITION", "Define a method for creating an object, and let each subclass decide which concrete class it produces."),
    ("WHY HERE", "Every task type has its own construction rules and defaults. The caller should not have to know them."),
    ("ADVANTAGE", "A new task type is a new class. Code that creates tasks never changes when a type is added."),
    ("REAL-WORLD", "The same idea behind a document app that opens .pdf, .docx, or .txt through one Open action.")])
footer(s, 10)
notes(s, AR + ".\n"
    "Factory Method, following the report structure. The definition: define a method for creating an object, and let each subclass decide which concrete class it returns. We have an abstract TaskFactory with a createTask method, and three subclasses that each build their own type.\n"
    "Why it fits here: each task type has different construction rules and defaults, and we do not want the caller to carry that knowledge. The advantage is the one tied to our objective: a new task type is just a new class, and no existing creation code changes. A familiar real-world example is a document editor that opens several file formats through a single Open action; you do not call a different method per format. Next, how it looks in our code.")

# 11 FACTORY METHOD · in our code ------------------------------------
s = slide(WHITE); eyebrow(s, "Pattern 1 · Factory Method", speaker=AR); title(s, "How we implemented it.")
sub(s, "The manager keeps a registry of factories keyed by a string. The caller asks for a type by name and never sees a concrete class.")
code(s, M, 2.95, SW-2*M, [
    'manager.createTask("BUG", "Login broken", "OAuth callback fails", 8);',
    'manager.createTask("FEATURE", "Dark mode", "Top user request", 5);'])
gap = 0.7; colw = (SW-2*M-gap)/2
hline(s, M, 4.75, colw, INK, 1.4)
text(s, M, 4.9, colw, 1.4, [[{"t": "Abstract class, not an interface", "size": 13.5, "color": INK, "bold": True, "space_after": 4}],
    [{"t": "Each subclass owns its defaults: a bug is MEDIUM severity, a feature is 8h effort and value 5, a doc targets developers.", "size": 11.5, "color": GRAY, "line": 1.3}]])
hline(s, M+colw+gap, 4.75, colw, INK, 1.4)
text(s, M+colw+gap, 4.9, colw, 1.4, [[{"t": "createTaskWithDeadline() on the base", "size": 13.5, "color": INK, "bold": True, "space_after": 4}],
    [{"t": "The base wraps createTask() and attaches a deadline once. That is Template Method, reused by all three factories.", "size": 11.5, "color": GRAY, "line": 1.3}]])
footer(s, 11)
notes(s, AR + ".\n"
    "Here is the implementation. The manager holds a Map from a string key to a factory. The caller writes createTask with the string BUG, and the manager looks up the right factory and calls it. The caller never imports BugTask. When we added Documentation late in the project, we registered it once and the console menu offered it automatically, because the menu iterates the registry.\n"
    "Two design decisions we expect questions on. Left: we used an abstract class, not an interface, so each subclass can own its defaults. Right: createTaskWithDeadline lives on the base class and wraps the abstract createTask, which is the Template Method pattern sitting on top of Factory Method, so the deadline logic is written once, not three times. Hand to Mouhammad for Strategy.")

# 12 STRATEGY · definition & rationale -------------------------------
s = slide(WHITE); eyebrow(s, "Pattern 2 · Strategy", speaker=MH); title(s, "Strategy, and why it fits.")
defcard(s, [
    ("DEFINITION", "Define a family of interchangeable algorithms, encapsulate each one, and select between them at runtime."),
    ("WHY HERE", "The same task list must be ordered differently in different contexts, while the app is running."),
    ("ADVANTAGE", "Add or switch an ordering without touching the code that holds and manages the list."),
    ("REAL-WORLD", "Like choosing a route in a maps app: fastest, shortest, or no tolls, computed over the same map.")])
footer(s, 12)
notes(s, MH + ".\n"
    "Strategy, same structure. The definition: define a family of interchangeable algorithms, put each behind a common interface, and choose between them at runtime. Our interface is PriorityStrategy with a single sort method, and we have three implementations.\n"
    "Why it fits: the same list needs different orderings in different moments, and the user changes that while the app runs. The advantage, again tied to our objective: a new ordering is a new class, and the manager that holds the list never changes. The everyday example is a maps app: fastest, shortest, or avoid tolls, are three strategies over the same map. Next, the code.")

# 13 STRATEGY · in our code ------------------------------------------
s = slide(WHITE); eyebrow(s, "Pattern 2 · Strategy", speaker=MH); title(s, "How we implemented it.")
sub(s, "Each ordering is a swappable object behind one interface. Changing the sort is a single setter call; the manager stays unaware of which is active.")
code(s, M, 2.95, SW-2*M, [
    'manager.setPriorityStrategy(new SeverityFirstStrategy());',
    '// the next call to getPrioritizedTasks() returns the new order'])
gap = 0.7; colw = (SW-2*M-gap)/2
hline(s, M, 4.75, colw, INK, 1.4)
text(s, M, 4.9, colw, 1.4, [[{"t": "An interface, not a raw Comparator", "size": 13.5, "color": INK, "bold": True, "space_after": 4}],
    [{"t": "PriorityStrategy names the role. SeverityFirst also partitions bugs to the top, which a pairwise Comparator handles awkwardly.", "size": 11.5, "color": GRAY, "line": 1.3}]])
hline(s, M+colw+gap, 4.75, colw, INK, 1.4)
text(s, M+colw+gap, 4.9, colw, 1.4, [[{"t": "A setter, not a constructor argument", "size": 13.5, "color": INK, "bold": True, "space_after": 4}],
    [{"t": "Users change the sort mid-session. A setter avoids rebuilding the manager and copying every task into a new instance.", "size": 11.5, "color": GRAY, "line": 1.3}]])
footer(s, 13)
notes(s, MH + ".\n"
    "The implementation is small. The manager holds one PriorityStrategy field. Changing the order is one setter call, and the next listing comes back sorted differently, with no recompile.\n"
    "Two decisions. Left: we used a named interface rather than a raw Java Comparator, because the name PriorityStrategy advertises the role in the system, and because SeverityFirst partitions bugs to the top before sorting the rest, which is stateful work a pairwise Comparator does awkwardly. Right: we used a setter rather than constructor injection, because the user swaps sorts while the app runs, and a setter avoids rebuilding the manager. The next slide shows this happening for real in the GUI.")

# 14 STRATEGY · live evidence (screenshots) --------------------------
s = slide(WHITE); eyebrow(s, "Pattern 2 · Strategy · evidence", speaker=MH); title(s, "The same list, reordered live.")
gap = 0.5; colw = (SW-2*M-gap)/2
img_contain(s, "gui-strategy.png", M, 2.35, colw, 3.95, border=RULEW)
img_contain(s, "gui-severity.png", M+colw+gap, 2.35, colw, 3.95, border=RULEW)
text(s, M, 6.32, colw, 0.4, [{"t": "Urgent First sort: priority 5 down to 1.", "size": 10.5, "color": GRAY, "track": 0.4}])
text(s, M+colw+gap, 6.32, colw, 0.4, [{"t": "Severity First sort: both bugs rise to the top.", "size": 10.5, "color": GRAY, "track": 0.4}])
footer(s, 14)
notes(s, MH + ".\n"
    "These are two real screenshots of our running GUI, the same five tasks in both. On the left, sorted Urgent First, the rows run by priority, five down to one. On the right, after switching the Sort by dropdown to Severity First, the two bug rows jump to the top, and the status bar confirms the active strategy changed.\n"
    "Nothing was recompiled between these two pictures. The list of tasks is identical; only the strategy object changed, through one setter call wired to the dropdown. This is the clearest single piece of evidence that the pattern works as intended. In the live demo we will do this switch in front of you.")

# 15 BONUS · STATE / lifecycle ---------------------------------------
s = slide(WHITE); eyebrow(s, "Bonus pattern · State", speaker=MH); title(s, "The lifecycle is a state machine.")
img_contain(s, "state-diagram.png", M, 2.4, 6.0, 4.1, border=RULEW)
text(s, 7.25, 2.55, SW-M-7.25, 4.0, [
    [{"t": "TaskStatus encodes its own transitions.", "size": 13.5, "color": INK, "bold": True, "space_after": 8}],
    [{"t": "Each enum constant declares its legal next states through canTransitionTo().", "size": 12, "color": GRAY, "line": 1.35, "space_after": 7}],
    [{"t": "AbstractTask.setStatus() checks that table and throws on an illegal move.", "size": 12, "color": GRAY, "line": 1.35, "space_after": 7}],
    [{"t": "The engine refuses to skip OPEN straight to DONE: the cycle must be walked.", "size": 12, "color": GRAY, "line": 1.35, "space_after": 7}],
    [{"t": "The State pattern, in a single enum file, with no extra classes.", "size": 12, "color": INK, "bold": True, "line": 1.35}]])
footer(s, 15)
notes(s, MH + ".\n"
    "The bonus. The rubric only requires one creational and one behavioural pattern, but the task lifecycle is naturally a state machine, so we encoded it cheaply. A normal path: OPEN, then IN_PROGRESS when a developer picks it up, then REVIEW, then DONE, which is terminal. A reviewer can reject back to IN_PROGRESS, any active task can be BLOCKED, and BLOCKED returns to OPEN.\n"
    "The rules live on the enum itself, through canTransitionTo, and setStatus throws if you try an illegal jump such as OPEN straight to DONE. So this is the State pattern expressed in one enum, with no extra classes. It caught two real bugs during development. Hand back to me for the architecture section.")

# 16 SECTION 03 DIVIDER ----------------------------------------------
s = slide(INK)
divider(s, "Section 03", "Architecture & implementation.",
        "How the design looks as classes, how a single request flows through it, and how it maps to Java and to SOLID.", speaker=MH)
notes(s, MH + ".\n"
    "Section three. We move from the two patterns to the system as a whole. I will show the class diagram and the layers, the sequence of one create-task call, the file structure of the implementation, and finally how the design lines up with all five SOLID principles.")

# 17 CLASS DIAGRAM ---------------------------------------------------
s = slide(WHITE); eyebrow(s, "Architecture · structure", speaker=MH)
text(s, M, 1.2, 8.5, 0.5, [{"t": "The class diagram.", "size": 22, "color": INK, "bold": True}])
text(s, M, 1.74, SW-2*M, 0.4, [{"t": "Three layers: product (tasks) · pattern (factories + strategies) · coordination (the manager and entry points).   Every arrow points toward an abstraction.", "size": 11, "color": FAINT, "line": 1.3}])
img_contain(s, "class-diagram.png", M, 2.25, SW-2*M, 4.55, border=RULEW)
footer(s, 17)
notes(s, MH + ".\n"
    "The class diagram in three horizontal layers. The top layer is the product: the Task interface, AbstractTask, and the three concrete tasks. The middle layer is the patterns: the factory hierarchy on one side, the strategy hierarchy on the other. The bottom is coordination: TaskManager plus the three entry points.\n"
    "The single most important thing to see is that every arrow points toward an abstraction. The manager depends on the Task interface and the TaskFactory abstract class, never on a concrete BugTask. That is Dependency Inversion in visual form, and it is the structural reason a new task type does not touch the manager.")

# 18 SEQUENCE DIAGRAM ------------------------------------------------
s = slide(WHITE); eyebrow(s, "Architecture · behaviour", speaker=MH)
text(s, M, 1.2, 8.5, 0.5, [{"t": "Creating a task, step by step.", "size": 22, "color": INK, "bold": True}])
text(s, M, 1.74, SW-2*M, 0.4, [{"t": "The caller passes a type string. The manager finds the registered factory and returns a Task. No concrete class is ever named by the caller.", "size": 11, "color": FAINT, "line": 1.3}])
img_contain(s, "sequence-diagram.png", M, 2.25, SW-2*M, 4.55, border=RULEW)
footer(s, 18)
notes(s, MH + ".\n"
    "This sequence diagram traces one createTask call. The entry point asks the manager for a BUG. The manager looks up the factory registered under that key, asks it to build the task, and returns a Task reference. Notice what does not happen: the caller never constructs or imports BugTask.\n"
    "This is the runtime counterpart of the class diagram. The static view shows arrows pointing at abstractions; this dynamic view shows that at call time the concrete type stays hidden behind the manager and the factory.")

# 19 IMPLEMENTATION OVERVIEW -----------------------------------------
s = slide(WHITE); eyebrow(s, "Implementation · structure", speaker=MH); title(s, "Sixteen files, three layers.")
sub(s, "No package declarations, only java.util and java.time imported. The folders below mirror the three layers of the class diagram.")
gap = 0.5; colw = (SW-2*M-2*gap)/3
listcol(s, M, 2.95, colw, "PRODUCT LAYER", [
    "Task (interface)", "AbstractTask (base)", "BugTask · FeatureTask", "DocumentationTask", "TaskStatus (enum)"], gap=0.6, item_size=12)
listcol(s, M+colw+gap, 2.95, colw, "PATTERN LAYER", [
    "TaskFactory (abstract)", "Bug / Feature / Doc factories", "PriorityStrategy (interface)", "UrgentFirst · DeadlineFirst", "SeverityFirst"], gap=0.6, item_size=12)
listcol(s, M+2*(colw+gap), 2.95, colw, "COORDINATION & ENTRY", [
    "TaskManager (coordinator)", "Main (automated tests)", "TaskManagementApp (console)", "gui.TaskManagerGUI (Swing)"], gap=0.6, item_size=12)
hline(s, M, 6.35, SW-2*M, RULEW, 1.0)
text(s, M, 6.5, SW-2*M, 0.4, [{"t": "All three entry points drive the same engine through its public API. 2 interfaces · 1 enum · 1 abstract · 12 concrete classes.", "size": 11, "color": GRAY, "line": 1.3}])
footer(s, 19)
notes(s, MH + ".\n"
    "The implementation, grouped by the same three layers. The product layer holds the Task interface, the abstract base, the three concrete tasks, and the status enum. The pattern layer holds the abstract factory and its three subclasses, plus the strategy interface and its three implementations. The coordination layer is the single TaskManager, plus the three entry points: Main for automated tests, TaskManagementApp for the console, and the Swing GUI.\n"
    "Sixteen files, two interfaces, one enum, one abstract class, twelve concrete classes, and the only imports are java.util and java.time. Crucially, all three entry points use the same engine through its public API, which is what lets the GUI and the console behave identically.")

# 20 SOLID -----------------------------------------------------------
s = slide(WHITE); eyebrow(s, "Implementation · principles", speaker=MH); title(s, "How the design meets SOLID.")
sol = [("S · Single responsibility", "Factories build, strategies sort, the manager coordinates. One reason to change each."),
       ("O · Open / Closed", "A new task type or sort is a new file plus one line. Zero edits to existing classes."),
       ("L · Liskov substitution", "Every factory works through the abstract reference; every strategy through the interface."),
       ("I · Interface segregation", "PriorityStrategy declares one method; the Task interface stays minimal."),
       ("D · Dependency inversion", "The manager's fields are all interfaces and abstract types, never concretes."),
       ("The throughline", "Abstractions sit in the middle of the system; concrete classes live at the edges.")]
gap = 0.7; colw = (SW-2*M-gap)/2
for i, (h, b) in enumerate(sol):
    c, r = i % 2, i // 2; x = M+c*(colw+gap); y = 2.55+r*1.35
    text(s, x, y+0.02, 0.3, 0.4, [{"t": "·", "size": 13, "color": INK, "bold": True}])
    text(s, x+0.34, y, colw-0.34, 1.2, [[{"t": h, "size": 13, "color": INK, "bold": True, "space_after": 2}],
                                        [{"t": b, "size": 11, "color": GRAY, "line": 1.25}]])
footer(s, 20)
notes(s, MH + ".\n"
    "SOLID, briefly, because it falls out of the two patterns rather than being added on. Single responsibility: factories build, strategies sort, the manager coordinates. Open/Closed: a new type or sort is a new file and one line, with zero edits to existing code, which is our central objective. Liskov: every factory and strategy stands in for its abstraction without surprises. Interface segregation: the strategy interface has one method, and the Task interface is minimal. Dependency inversion: the manager references only abstractions.\n"
    "The throughline at the bottom sums it up: abstractions in the middle, concrete classes at the edges. If you want one example of inversion, it is that there is no new BugTask anywhere inside the manager. Hand to both of us for the demonstration.")

# 21 SECTION 04 DIVIDER ----------------------------------------------
s = slide(INK)
divider(s, "Section 04", "Live demonstration.",
        "The compiled system, run three ways: the automated test suite, the interactive console, and the Swing GUI.", speaker="Both")
notes(s, "Both. " + MH + " drives, " + AR + " narrates.\n"
    "Section four is the live demonstration, which the assignment requires. We will run the automated tests first, then open the GUI and switch the strategy live, create a task through the factory, and trigger an illegal lifecycle move so you can see the engine reject it. It is rehearsed to about three minutes, and we have screenshots as a backup if the projector fails.")

# 22 DEMO RUNBOOK ----------------------------------------------------
s = slide(WHITE); eyebrow(s, "Live demonstration · runbook", speaker=AR + " narrates · " + MH + " drives"); title(s, "Running the system.")
text(s, M, 2.06, 1.55, 0.3, [{"t": "BUILD ONCE", "size": 9.5, "color": GRAY, "bold": True, "track": 1.8}])
text(s, M+1.55, 2.0, SW-2*M-1.55, 0.34, [{"t": "javac -d bin src/main/java/*.java src/main/java/gui/*.java", "size": 11.5, "color": NEAR, "font": MONO}])
hline(s, M, 2.5, SW-2*M, RULEW, 1.0)
img_contain(s, "gui-strategy.png", M, 2.75, 4.85, 3.6, border=RULEW)
steps = [("1 · Automated tests", [{"t": "java -cp bin Main", "font": MONO}, {"t": "  six sections, ends ALL TESTS PASSED."}]),
         ("2 · Open the GUI", [{"t": "java -jar TaskManagerGUI.jar", "font": MONO}, {"t": "  then Demo, Load Strategy Demo."}]),
         ("3 · Strategy, live", [{"t": "switch Sort by: Urgent, Deadline, Severity. The table reorders, no recompile."}]),
         ("4 · Factory, live", [{"t": "add a task from the form. Type is BUG, FEATURE, or DOCUMENTATION."}]),
         ("5 · State machine", [{"t": "click a row: OPEN to DONE is refused, OPEN to IN_PROGRESS is allowed."}])]
sx = M+5.25; sw = SW-M-sx
for i, (h, runs) in enumerate(steps):
    y = 2.78 + i*0.74
    text(s, sx, y, sw, 0.3, [{"t": h, "size": 12.5, "color": INK, "bold": True}])
    text(s, sx, y+0.28, sw, 0.42, [[{**r, "size": r.get("size", 10.5), "color": r.get("color", GRAY), "line": 1.2} for r in runs]])
text(s, M, 6.55, SW-2*M, 0.4, [{"t": "Validation lives in the engine, not the GUI. Every entry point shares the same Factory Method + Strategy core.", "size": 10.5, "color": FAINT}])
footer(s, 22)
notes(s, "Both. " + MH + " runs the commands, " + AR + " narrates.\n"
    "Build once with the javac line at the top. Then five steps. Step one, run Main: six test sections scroll past and it ends with ALL TESTS PASSED; pause on Test 1, Factory, and Test 2, Strategy. Step two, open the GUI with the jar and load the Strategy demo from the Demo menu.\n"
    "Step three is the key moment: switch the Sort by dropdown through Urgent, Deadline, and Severity, and the table reorders each time with no recompile, exactly like the screenshots two slides ago. Step four, add a task using the form; the Type dropdown chooses which factory builds it. Step five, click a row and try to mark an OPEN task DONE: the engine refuses with the exact reason, then OPEN to IN_PROGRESS works.\n"
    "The closing point: validation lives in the engine, and all three entry points share the same core. If time is short, skip step one and start at the GUI. Hand back to me for the evaluation.")

# 23 SECTION 05 DIVIDER ----------------------------------------------
s = slide(INK)
divider(s, "Section 05", "Results, evaluation & conclusion.",
        "What the patterns delivered in practice, the honest limits of this implementation, and what we take away.", speaker=AR)
notes(s, AR + ".\n"
    "The final section. We evaluate the result against our objective, we are honest about the limitations and the alternatives we considered, and we close with the conclusion and what we learned.")

# 24 RESULTS & ADVANTAGES --------------------------------------------
s = slide(WHITE); eyebrow(s, "Results · what the patterns delivered", speaker=AR); title(s, "New features, without editing old code.")
gap = 0.7; colw = (SW-2*M-gap)/2
listcol(s, M, 2.5, colw, "EXTENSION, IN NUMBERS", [
    "New task type: 2 new files, 1 line of registration, 0 edits.",
    "New ordering: 1 new file, 1 setter call, 0 edits.",
    "Test 5 in Main asserts this Open/Closed property at runtime."])
listcol(s, M+colw+gap, 2.5, colw, "WHAT WORKED IN PRACTICE", [
    "Documentation type was added late in under 30 minutes.",
    "The GUI dropdown proves the Strategy swap, live.",
    "The lifecycle enum caught two real bugs in development.",
    "Main doubles as a test harness, with no JUnit needed."])
footer(s, 24)
notes(s, AR + ".\n"
    "Did the design meet its objective? On the left, in numbers: a new task type costs two new files and one registration line, with zero edits to existing code; a new ordering costs one new file and one setter call, again zero edits. We did not just claim this, Test 5 in Main checks the property at runtime.\n"
    "On the right, what actually happened during the project. We added the Documentation type late, and it took under thirty minutes end to end. The GUI dropdown demonstrates the strategy swap live. The lifecycle enum caught two real bugs before they shipped. And Main served as our test harness without pulling in JUnit, which kept the zero-dependency rule.")

# 25 LIMITATIONS & ALTERNATIVES --------------------------------------
s = slide(WHITE); eyebrow(s, "Evaluation · limitations & alternatives", speaker=AR); title(s, "An honest look at the design.")
cols3(s, [("Limitations", "All data is in memory; nothing persists. Single user, no concurrency. Validation throws rather than collecting all errors."),
          ("Alternatives we weighed", "Abstract Factory: rejected, there is only one product family. A raw Comparator: loses the named role and the stateful sort."),
          ("Future work", "Persistence via Repository, tags via Specification, async dispatch, and a small REST layer over the same engine.")],
      y=2.9, lab_size=14, body_size=11.5)
hline(s, M, 5.6, SW-2*M, RULEW, 1.0)
text(s, M, 5.75, SW-2*M, 0.6, [{"t": "Being explicit about what is not built, and why, is part of the design. The engine is decoupled enough that each item above is an addition, not a rewrite.", "size": 11.5, "color": GRAY, "line": 1.35}])
footer(s, 25)
notes(s, AR + ".\n"
    "An honest evaluation, which the rubric asks for. Limitations: everything is in memory so nothing persists, it is single-user with no concurrency control, and validation throws on the first error rather than collecting them. These are real, and they are deliberate scoping choices for an academic project.\n"
    "Alternatives we weighed: we considered Abstract Factory but rejected it, because we have only one product family, a single Task, so the extra abstraction would not earn its keep. We considered a raw Comparator instead of Strategy, but that loses the named role and handles the bugs-first sort awkwardly. Future work would be persistence with a Repository, tags with a Specification, async dispatch, and a REST layer. The point at the bottom: because the engine is decoupled, each of these is an addition, not a rewrite.")

# 26 CONCLUSION ------------------------------------------------------
s = slide(WHITE); eyebrow(s, "Conclusion", speaker=AR); title(s, "What we set out to do, and what we learned.")
concl = [("What we achieved", "A working task system where new types and new orderings cost no edits to existing, tested code."),
         ("The patterns earned their place", "Each was chosen to solve a concrete problem from section one, not to satisfy a checklist."),
         ("The lesson", "Naming a role, a factory or a strategy, makes the codebase explain itself to the next reader."),
         ("The bigger point", "Design patterns are a shared vocabulary for keeping software open to change without fear.")]
gap = 0.62; colw = (SW-2*M-gap)/2
for i, (h, b) in enumerate(concl):
    c, r = i % 2, i // 2; x = M+c*(colw+gap); y = 2.7+r*1.75
    hline(s, x, y, colw, RULEW, 1.0)
    text(s, x, y+0.14, colw, 1.5, [[{"t": h, "size": 14, "color": INK, "bold": True, "space_after": 4}],
                                   [{"t": b, "size": 12, "color": GRAY, "line": 1.35}]])
footer(s, 26)
notes(s, AR + ".\n"
    "To conclude. What we achieved: a working system that meets the objective we set, new types and orderings without editing existing code. The patterns earned their place, because each one answered a specific problem from section one, rather than being added to tick a box.\n"
    "Our main lesson was about naming: calling something a factory or a strategy makes the code explain itself, which matters more than cleverness on a team. And the bigger point, the reason the course exists: design patterns are a shared vocabulary that lets a team keep software open to change without being afraid to touch it. Thank you, and we are happy to take questions.")

# 27 THANK YOU / Q&A -------------------------------------------------
s = slide(INK)
text(s, M, 2.6, 11.8, 1.7, [[{"t": "Thank you.", "size": 44, "color": WHITE, "bold": True, "line": 1.06}],
                            [{"t": "Questions welcome.", "size": 44, "color": FAINT, "bold": True, "line": 1.06}]])
hline(s, M, 4.85, SW-2*M, RULEB, 1.0)
text(s, M, 5.05, 9.5, 1.0, [[{"t": "We can speak to any part: the problem, the patterns, the architecture, the code, or the demo.", "size": 13, "color": GRAYW, "line": 1.35, "space_after": 6}],
                            [{"t": "SEN3006 Software Architecture · Abdul Rahman Malak · Mouhammad Houjeirat", "size": 11, "color": GRAYW}]])
notes(s, "Both.\n"
    "Thank you. We will split questions by area: Abdul Rahman takes the problem framing, Factory Method, SOLID, and the evaluation; Mouhammad takes Strategy, the architecture, and the lifecycle. Anticipated questions: Why an abstract factory class instead of an interface? Per-subclass defaults plus Template Method. Why a strategy interface instead of a Comparator? It advertises the role and supports the partition-then-sort. Why a string-keyed registry? Runtime lookup from any entry point. Why no JUnit? The zero-dependency rule, with Main as the harness. The study guide in docs/design has a fuller cheat sheet.")

# 28 APPENDIX | component + deployment -------------------------------
s = slide(WHITE); eyebrow(s, "Appendix · supporting views"); title(s, "Component & deployment views.", size=24)
gap = 0.5; colw = (SW-2*M-gap)/2
img_contain(s, "component-diagram.png", M, 2.5, colw, 3.5, border=RULEW)
img_contain(s, "deployment-diagram.png", M+colw+gap, 2.5, colw, 3.5, border=RULEW)
text(s, M, 6.2, colw, 0.3, [{"t": "Component view: the three layers as modules.", "size": 10.5, "color": GRAY, "track": 0.6}])
text(s, M+colw+gap, 6.2, colw, 0.3, [{"t": "Deployment view: one JVM, three entry points.", "size": 10.5, "color": GRAY, "track": 0.6}])
footer(s, 28)
notes(s, "Appendix, for questions.\n"
    "Two supporting views kept in reserve. The component diagram groups the system into the product, pattern, and coordination modules. The deployment diagram shows the whole thing runs in a single JVM, with three entry points over one shared engine, no network and no external services. Both are explained in full in the report.")

prs.save(OUT); print("SAVED", OUT, "|", len(prs.slides._sldIdLst), "slides")
