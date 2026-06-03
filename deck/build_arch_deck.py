# Task Management System | Software Architecture deck (SEN3006).
# V3 redesign: warm editorial system. Spectral serif headers + Inter body, a
# warm cream base, an indigo spine with three pattern hues (Factory=clay,
# Strategy=teal, State=violet) plus status colours, structural Untitled UI icons
# on every card, colour-coded section dividers, and a section progress tracker.
# Presenter names appear on the cover only. Built with python-pptx.
# Build: python build_arch_deck.py   (icons live in _ico/, diagrams in _dia/)
import os, re
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
DIA = os.path.join(HERE, "_dia")
ICO = os.path.join(HERE, "_ico")
OUT = os.path.join(HERE, "Task-Management-System.pptx")

# ---- palette ----------------------------------------------------------------
def C(h): return RGBColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))
PAPER  = C("FBF9F5")   # content background, warm cream
CARD   = C("FFFFFF")   # card fill
CARDBD = C("E8E2D5")   # card border
RULE   = C("E4DECF")   # hairlines on cream
INK    = C("1C1A16")   # serif headers + dark backgrounds
BODY   = C("57534B")   # Inter body on cream
MUTE   = C("8C877D")   # labels, captions
FAINT  = C("B7B1A4")   # footers, de-emphasis
DARK   = C("1C1A16")   # divider / cover background
RULE_DK= C("3A352E")   # hairlines on dark
WHITE  = C("FFFFFF")
GRAYW  = C("A8A299")   # body text on dark
PANEL  = C("F4F0E8")   # subtle panel on cream

# accents on light (deeper)
INDIGO = C("4A45C7"); CLAY = C("BC5A2B"); TEAL = C("0E7C72"); VIOLET = C("7C3AED")
GREEN  = C("1E7A45"); AMBER = C("B5760C"); RED  = C("BB2D23")
# tints (chip backgrounds)
INDIGO_T=C("ECEBFA"); CLAY_T=C("F6ECE3"); TEAL_T=C("E2F0ED"); VIOLET_T=C("F0EAFB")
GREEN_T =C("E6F0EA"); AMBER_T=C("F5EEDD"); RED_T =C("F7E9E6"); MUTE_T=C("EEEBE6")
# accents on dark (brighter) for dividers
INDIGO_D=C("8E8BF5"); VIOLET_D=C("B6A6F7"); TEAL_D=C("4FC2B2"); GREEN_D=C("5BD08F"); AMBER_D=C("E7B765")

# code syntax (muted editor grade)
CODEBG=C("F7F4ED"); CODEBD=C("E7E1D4")
KW=C("8250DF"); TYP=C("0550AE"); STRc=C("0A7B33"); NUMc=C("0550AE"); COM=C("8C877D")

SERIF_SB="Spectral SemiBold"; SERIF="Spectral"; SERIF_MD="Spectral Medium"
SANS="Inter"; SANS_SB="Inter SemiBold"; SANS_MD="Inter Medium"; MONO="Consolas"

SW, SH = 13.333, 7.5; M = 0.82; TOTAL = 32

prs = Presentation(); prs.slide_width = Emu(int(SW*914400)); prs.slide_height = Emu(int(SH*914400))
BLANK = prs.slide_layouts[6]

# ---- primitives -------------------------------------------------------------
def slide(bg=PAPER):
    s = prs.slides.add_slide(BLANK); s.background.fill.solid(); s.background.fill.fore_color.rgb = bg; return s
def notes(s, txt): s.notes_slide.notes_text_frame.text = txt
def _spc(r, pts): r.font._rPr.set("spc", str(int(pts*100)))
def hline(s, x, y, w, color=RULE, weight=1.0):
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y), Inches(x+w), Inches(y))
    ln.line.color.rgb = color; ln.line.width = Pt(weight); ln.shadow.inherit = False; return ln
def rrect(s, x, y, w, h, fill, line=None, lw=1.0, radius=0.06):
    sp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(lw)
    sp.shadow.inherit = False
    try: sp.adjustments[0] = radius
    except Exception: pass
    return sp
def text(s, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(tf, m, 0)
    first = True
    for para in paras:
        runs = para if isinstance(para, list) else [para]
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False; p.alignment = align; meta = runs[0]
        if meta.get("space_before") is not None: p.space_before = Pt(meta["space_before"])
        if meta.get("space_after") is not None: p.space_after = Pt(meta["space_after"])
        if meta.get("line") is not None: p.line_spacing = meta["line"]
        for rd in runs:
            r = p.add_run(); r.text = rd["t"]; f = r.font
            f.name = rd.get("font", SANS); f.size = Pt(rd.get("size", 13.5))
            f.bold = rd.get("bold", False); f.color.rgb = rd.get("color", INK)
            if rd.get("italic"): f.italic = True
            if rd.get("track"): _spc(r, rd["track"])
    return tf
def place_icon(s, name, key, cx, cy, size):
    p = os.path.join(ICO, f"{name}__{key}.png")
    if not os.path.exists(p):
        return
    s.shapes.add_picture(p, Inches(cx-size/2), Inches(cy-size/2), Inches(size), Inches(size))
def chip(s, x, y, size, tint, name, key, frac=0.56):
    rrect(s, x, y, size, size, tint, radius=0.30)
    place_icon(s, name, key, x+size/2, y+size/2, size*frac)

# ---- chrome -----------------------------------------------------------------
def eyebrow(s, label, accent=INDIGO):
    rrect(s, M, 0.64, 0.07, 0.24, accent, radius=0.5)
    text(s, M+0.22, 0.64, 9, 0.3, [{"t": label.upper(), "size": 11, "color": accent, "bold": True, "track": 2.0, "font": SANS_SB}])
SECTION_HUE = {1: INDIGO, 2: VIOLET, 3: TEAL, 4: GREEN, 5: AMBER}
def tracker(s, active, on_dark=False):
    n=5; segw=0.32; gap=0.10; y=0.70
    x0 = SW-M-(n*segw+(n-1)*gap)
    hue = SECTION_HUE.get(active, INDIGO)
    for i in range(n):
        x = x0+i*(segw+gap)
        if i == active-1: col = hue
        else:             col = RULE_DK if on_dark else RULE
        rrect(s, x, y, segw, 0.07, col, radius=0.5)
    text(s, x0, y+0.13, n*segw+(n-1)*gap, 0.2,
         [{"t": f"SECTION {active} / 5", "size": 7.5, "color": hue, "track": 1.4, "font": SANS_SB}],
         align=PP_ALIGN.RIGHT)
def title(s, t, y=1.42, color=INK, size=29, w=None):
    text(s, M, y, w or (SW-2*M), 1.0, [{"t": t, "size": size, "color": color, "font": SERIF_SB, "line": 1.04}])
def sub(s, t, color=BODY, y=2.26, w=None, size=13):
    text(s, M, y, w or (SW-2*M-1.0), 0.7, [{"t": t, "size": size, "color": color, "line": 1.36}])
def footer(s, n, on_dark=False):
    c = GRAYW if on_dark else FAINT
    text(s, M, SH-0.52, 8, 0.3, [{"t": "Task Management System   ·   SEN3006 Software Architecture", "size": 8.5, "color": c, "track": 1.0}])
    text(s, SW-M-3, SH-0.52, 3, 0.3, [{"t": f"{n:02d} / {TOTAL}", "size": 8.5, "color": c, "track": 1.2}], align=PP_ALIGN.RIGHT)

# ---- composite blocks -------------------------------------------------------
def card(s, x, y, w, h, tint, name, key, title_t, body_t, tsize=13.5, bsize=11.5, cs=0.5):
    rrect(s, x, y, w, h, CARD, CARDBD, 1.0, radius=0.045)
    chip(s, x+0.28, y+0.28, cs, tint, name, key)
    text(s, x+0.28+cs+0.18, y+0.28, w-(0.28+cs+0.18)-0.24, cs,
         [{"t": title_t, "size": tsize, "color": INK, "font": SANS_SB, "line": 1.04}], anchor=MSO_ANCHOR.MIDDLE)
    text(s, x+0.30, y+0.28+cs+0.14, w-0.58, h-(0.28+cs+0.14)-0.16,
         [{"t": body_t, "size": bsize, "color": BODY, "line": 1.32}])
def listpanel(s, x, y, w, h, tint, name, key, label, items, acc, isize=12, gap=0.6):
    rrect(s, x, y, w, h, CARD, CARDBD, 1.0, radius=0.045)
    chip(s, x+0.30, y+0.28, 0.5, tint, name, key)
    text(s, x+0.30+0.5+0.18, y+0.28, w-1.2, 0.5,
         [{"t": label.upper(), "size": 11, "color": INK, "font": SANS_SB, "track": 1.4}], anchor=MSO_ANCHOR.MIDDLE)
    for i, it in enumerate(items):
        yy = y+1.04+i*gap
        text(s, x+0.34, yy-0.01, 0.22, 0.3, [{"t": "›", "size": 11.5, "color": acc, "font": SANS_SB}])
        text(s, x+0.58, yy, w-0.86, gap+0.1, [{"t": it, "size": isize, "color": BODY, "line": 1.2}])
def iconcol3(s, triples, y, specs, rule=True):
    gap=0.5; colw=(SW-2*M-2*gap)/3
    for i,(h,b) in enumerate(triples):
        x = M+i*(colw+gap); acc,tint,name,key = specs[i]
        chip(s, x, y, 0.5, tint, name, key)
        text(s, x, y+0.64, colw, 0.4, [{"t": h, "size": 13, "color": INK, "font": SANS_SB}])
        if rule: hline(s, x, y+0.97, colw*0.42, acc, 2.2)
        text(s, x, y+1.10, colw, 1.4, [{"t": b, "size": 11.5, "color": BODY, "line": 1.32}])
def console(s, x, y, w, h, rows, header="bash"):
    """Dark terminal card: window dots, header, then monospace rows of (text, color)."""
    rrect(s, x, y, w, h, C("15140F"), radius=0.05)
    for i,c in enumerate(["E66A5A","E7B765","5BD08F"]):
        rrect(s, x+0.22+i*0.20, y+0.135, 0.085, 0.085, C(c), radius=0.5)
    text(s, x, y+0.05, w, 0.26, [{"t": header, "size": 8.5, "color": C("6E6A60"), "font": MONO}], align=PP_ALIGN.CENTER)
    hline(s, x, y+0.36, w, C("2C291F"), 1.0)
    tf = s.shapes.add_textbox(Inches(x+0.24), Inches(y+0.46), Inches(w-0.42), Inches(h-0.56)).text_frame
    tf.word_wrap=False; tf.vertical_anchor=MSO_ANCHOR.TOP
    for m in ("margin_left","margin_right","margin_top","margin_bottom"): setattr(tf, m, 0)
    first=True
    for txt,col in rows:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first=False; p.line_spacing=1.24; p.alignment=PP_ALIGN.LEFT
        r=p.add_run(); r.text=txt if txt else " "; r.font.name=MONO; r.font.size=Pt(9); r.font.color.rgb=col

def cmdcard(s, x, y, w, label, command, accent, csize=13, h=0.92):
    """A 'paste this' command block: accent label on top, the exact command in mono below."""
    rrect(s, x, y, w, h, CODEBG, CODEBD, 1.0, radius=0.06)
    hline(s, x, y, w, accent, 2.4)
    text(s, x+0.26, y+0.16, w-0.5, 0.3, [{"t": label, "size": 10, "color": accent, "bold": True, "track": 1.5, "font": SANS_SB}])
    text(s, x+0.26, y+h-0.44, w-0.5, 0.36, [{"t": command, "size": csize, "color": INK, "font": MONO}])

def img_panel(s, name, bx, by, bw, bh, accent=None, caption=None):
    """White panel behind a diagram/screenshot, optional accent top-rule + caption."""
    rrect(s, bx, by, bw, bh, CARD, CARDBD, 1.0, radius=0.03)
    if accent: hline(s, bx+0.0, by, bw, accent, 2.4)
    pad = 0.18; ix, iy, iw, ih = bx+pad, by+pad+0.04, bw-2*pad, bh-2*pad-0.04
    path = os.path.join(DIA, name)
    if not os.path.exists(path):
        text(s, ix, iy+ih/2-0.2, iw, 0.4, [{"t": "[ "+name+" ]", "size": 12, "color": FAINT}], align=PP_ALIGN.CENTER); return
    iwpx, ihpx = Image.open(path).size; ratio = iwpx/ihpx
    if iw/ih > ratio: h = ih; w = ih*ratio
    else: w = iw; h = iw/ratio
    s.shapes.add_picture(path, Inches(ix+(iw-w)/2), Inches(iy+(ih-h)/2), Inches(w), Inches(h))
    if caption:
        text(s, bx, by+bh+0.1, bw, 0.3, [{"t": caption, "size": 10, "color": MUTE, "track": 0.4}], align=PP_ALIGN.CENTER)

def add_arrow(conn):
    ln = conn.line._get_or_add_ln(); t = ln.find(qn("a:tailEnd"))
    if t is None: t = ln.makeelement(qn("a:tailEnd"), {}); ln.append(t)
    t.set("type","triangle"); t.set("w","med"); t.set("len","med")

def blendhex(h1, h2, t):
    a=[int(h1[i:i+2],16) for i in (0,2,4)]; b=[int(h2[i:i+2],16) for i in (0,2,4)]
    return RGBColor(*[int(round(a[i]+(b[i]-a[i])*t)) for i in range(3)])
def divider(s, kicker, statement, sub_text, hexc, icon_name, active):
    # full-bleed section colour; white icon and statement, dimmed-white supporting marks
    s.background.fill.solid(); s.background.fill.fore_color.rgb = C(hexc)
    dim  = blendhex(hexc, "FFFFFF", 0.82)   # secondary text on the colour field
    rule = blendhex(hexc, "FFFFFF", 0.48)   # hairline on the colour field
    soff = blendhex(hexc, "FFFFFF", 0.30)   # inactive tracker segments
    text(s, M, 0.66, 9, 0.3, [{"t": kicker.upper(), "size": 11, "color": WHITE, "bold": True, "track": 2.8, "font": SANS_SB}])
    n=5; segw=0.32; gap=0.10; ty=0.70; x0=SW-M-(n*segw+(n-1)*gap)
    for i in range(n):
        rrect(s, x0+i*(segw+gap), ty, segw, 0.07, WHITE if i==active-1 else soff, radius=0.5)
    text(s, x0, ty+0.13, n*segw+(n-1)*gap, 0.2,
         [{"t": f"SECTION {active} / 5", "size": 7.5, "color": dim, "track": 1.4, "font": SANS_SB}], align=PP_ALIGN.RIGHT)
    place_icon(s, icon_name, "white", SW-M-1.25, 2.05, 1.55)
    hline(s, M, 3.30, SW-2*M, rule, 1.6)
    text(s, M, 3.60, SW-2*M-1.4, 1.4, [{"t": statement, "size": 37, "color": WHITE, "font": SERIF_SB, "line": 1.05}])
    text(s, M, 4.78, SW-2*M-2.2, 1.0, [{"t": sub_text, "size": 14, "color": dim, "line": 1.42}])

# ---- Java syntax highlighter + code panel -----------------------------------
JAVA_KW = {"class","interface","enum","abstract","extends","implements","new","void","return",
           "switch","case","int","boolean","public","private","protected","static","final",
           "this","throws","import","package","if","else"}
_tok = re.compile(r'(//[^\n]*|"[^"]*"|[A-Za-z_][A-Za-z0-9_]*|\d+|\s+|.)')
def java_runs(line):
    if not line.strip(): return [{"t": " ", "color": INK}]
    out=[]
    for m in _tok.finditer(line):
        t=m.group(0)
        if t.startswith("//"): col=COM
        elif t.startswith('"'): col=STRc
        elif t.isspace(): col=INK
        elif t.isdigit(): col=NUMc
        elif t in JAVA_KW: col=KW
        elif re.match(r'^[A-Z][A-Za-z0-9_]*$', t): col=TYP
        else: col=INK
        out.append({"t": t, "color": col})
    return out
def code(s, x, y, w, lines, size=12.5, accent=INDIGO):
    lh=size/72*1.55; h=0.40+len(lines)*lh
    rrect(s, x, y, w, h, CODEBG, CODEBD, 1.0, radius=0.04)
    hline(s, x, y, w, accent, 2.2)
    tf = s.shapes.add_textbox(Inches(x+0.04), Inches(y+0.14), Inches(w-0.08), Inches(h-0.2)).text_frame
    tf.word_wrap=False; tf.vertical_anchor=MSO_ANCHOR.TOP
    tf.margin_left=Inches(0.26); tf.margin_right=Inches(0.18); tf.margin_top=Inches(0.06); tf.margin_bottom=Inches(0.06)
    first=True
    for ln in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first=False; p.line_spacing=1.42; p.alignment=PP_ALIGN.LEFT
        for rd in java_runs(ln):
            r=p.add_run(); r.text=rd["t"]; r.font.name=MONO; r.font.size=Pt(size); r.font.color.rgb=rd["color"]
    return h

# ============================== SLIDES ==============================
NAME1="Abdul Rahman Malak"; NAME2="Mouhammad Houjeirat"

# 01 COVER (names live here only) --------------------------------------------
s = slide(DARK)
text(s, M, 0.66, 9, 0.3, [{"t": "SEN3006  ·  SOFTWARE ARCHITECTURE", "size": 11, "color": GRAYW, "track": 2.4, "font": SANS_SB}])
text(s, SW-M-6, 0.66, 6, 0.3, [{"t": "PROJECT PRESENTATION", "size": 11, "color": GRAYW, "track": 1.8, "font": SANS_SB}], align=PP_ALIGN.RIGHT)
text(s, M, 2.35, 11.9, 1.5, [{"t": "Task Management System.", "size": 50, "color": WHITE, "font": SERIF_SB, "line": 1.0}])
text(s, M, 3.62, 11.9, 0.7, [{"t": "Factory Method and Strategy, built in pure Java.", "size": 21, "color": INDIGO_D, "font": SERIF_MD, "italic": True, "line": 1.2}])
# pattern colour key rail
keyrow = [("Factory Method", CLAY), ("Strategy", TEAL), ("State", VIOLET)]
kx = M
for lab, col in keyrow:
    rrect(s, kx, 4.78, 0.30, 0.10, col, radius=0.5)
    text(s, kx+0.40, 4.66, 2.6, 0.34, [{"t": lab, "size": 11.5, "color": GRAYW, "font": SANS_SB, "track": 0.6}])
    kx += 0.40 + (1.95 if lab!="Strategy" else 1.45)
hline(s, M, 5.92, SW-2*M, RULE_DK, 1.0)
text(s, M, 6.14, 7.6, 0.8, [{"t": "A task tracker for software teams, designed around two classic patterns and a zero-dependency Java core.", "size": 12.5, "color": GRAYW, "line": 1.35}])
text(s, SW-M-4.6, 6.10, 4.6, 0.9, [[{"t": NAME1, "size": 13, "color": WHITE, "font": SANS_SB}],
                                   [{"t": NAME2, "size": 13, "color": WHITE, "font": SANS_SB, "space_before": 3}]], align=PP_ALIGN.RIGHT)
notes(s, "BOTH.\n"
    "We're " + NAME1 + " and " + NAME2 + " — our SEN3006 Task Management System, in pure Java. Two patterns, Factory Method + Strategy, plus State from the lifecycle. Zero dependencies, so the architecture is what's graded. " + NAME1 + " takes the contents.")

# 02 TABLE OF CONTENTS --------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Contents"); tracker(s, 1)
title(s, "What this presentation covers.")
toc = [("01","Introduction and problem definition","target-04","indigo",INDIGO,INDIGO_T,"~3 min"),
       ("02","The design patterns: Factory Method, Strategy, State","puzzle-piece-01","violet",VIOLET,VIOLET_T,"~5 min"),
       ("03","Architecture and implementation","grid-01","teal",TEAL,TEAL_T,"~4 min"),
       ("04","Live demonstration","terminal","green",GREEN,GREEN_T,"~3 min"),
       ("05","Results, evaluation and conclusion","trophy-01","amber",AMBER,AMBER_T,"~2 min")]
y0 = 2.62
for i,(n,t,icon,key,acc,tint,tm) in enumerate(toc):
    y = y0 + i*0.74
    rrect(s, M, y, SW-2*M, 0.62, CARD, CARDBD, 1.0, radius=0.06)
    chip(s, M+0.18, y+0.07, 0.48, tint, icon, key)
    text(s, M+0.84, y, 0.7, 0.62, [{"t": n, "size": 14, "color": acc, "font": SERIF_SB}], anchor=MSO_ANCHOR.MIDDLE)
    text(s, M+1.5, y, 8.2, 0.62, [{"t": t, "size": 14.5, "color": INK, "font": SANS_SB}], anchor=MSO_ANCHOR.MIDDLE)
    text(s, SW-M-1.7, y, 1.5, 0.62, [{"t": tm, "size": 11, "color": MUTE, "font": SANS_MD}], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
text(s, M, SH-0.74, SW-2*M, 0.4, [{"t": "Roughly sixteen minutes of talk and demo, then questions. We each take questions on the parts we led.", "size": 10.5, "color": FAINT, "track": 0.4}])
footer(s, 2)
notes(s, NAME1 + ".\n"
    "Five sections: problem, patterns (the big one), architecture, live demo, evaluation. About sixteen minutes, then questions. Hold questions to the end unless something on screen is unclear. Section one is mine.")

# 03 SECTION 01 DIVIDER -------------------------------------------------------
s = slide(DARK)
divider(s, "Section 01", "Introduction and problem definition.",
        "The domain we chose, the objectives we set, and the two problems that drove every pattern choice.",
        "4A45C7", "target-04", 1)
notes(s, NAME1 + ".\n"
    "Section one — define the problem first; it's graded. Domain and objectives, the requirements, then the two problems the patterns solve.")

# 04 INTRODUCTION -------------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Introduction  ·  background and objectives"); tracker(s, 1)
title(s, "Why a task management system?")
sub(s, "Software teams track many kinds of work. How that work gets created and ordered is where a tidy codebase usually starts to sprawl.")
intro=[("clipboard-check","indigo",INDIGO_T,"The domain","A tracker for a software team: bug, feature, and documentation tasks, each moving through one shared lifecycle from open to done."),
       ("zap","indigo",INDIGO_T,"The motivation","Two recurring causes of code sprawl in this kind of system line up cleanly with two patterns from the course."),
       ("target-04","indigo",INDIGO_T,"Our objective","Support new task types and new orderings, and let them be added without editing code that already works."),
       ("cube-01","indigo",INDIGO_T,"In one line","One engine, three ways to run it, sixteen Java files, zero external dependencies.")]
gap=0.5; colw=(SW-2*M-gap)/2; rh=1.74
for i,(icon,key,tint,h,b) in enumerate(intro):
    c,r=i%2,i//2; x=M+c*(colw+gap); y=2.98+r*(rh+0.22)
    card(s, x, y, colw, rh, tint, icon, key, h, b, tsize=14, bsize=11.5)
footer(s, 4)
notes(s, NAME1 + ".\n"
    "Domain: a task tracker for bugs, features, and docs on one lifecycle. Two recurring sources of code-sprawl match two course patterns. Objective, concrete and testable: add a new type or ordering without touching working code. One engine, three entry points, sixteen files, no libraries.")

# 05 REQUIREMENTS -------------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Problem definition  ·  requirements"); tracker(s, 1)
title(s, "What the system must do.")
gap=0.5; colw=(SW-2*M-gap)/2
listpanel(s, M, 2.5, colw, 3.28, INDIGO_T, "check-square", "indigo", "Functional requirements", [
    "Create bug, feature, and documentation tasks.",
    "Order the list by priority, deadline, or severity.",
    "Move tasks through a validated lifecycle.",
    "Filter by status and summarise the list."], INDIGO, gap=0.6)
listpanel(s, M+colw+gap, 2.5, colw, 3.28, INDIGO_T, "shield-tick", "indigo", "Non-functional requirements", [
    "Extensible: new types or orderings, no edits to old code.",
    "Pure Java 8+, zero external dependencies.",
    "Runs from the terminal: tests, console, and a GUI.",
    "Explainable: the design has to survive a viva."], INDIGO, gap=0.6)
rrect(s, M, 5.96, SW-2*M, 0.72, PANEL, radius=0.06)
text(s, M+0.3, 5.96, SW-2*M-0.6, 0.72, [{"t": "Two requirements drive the whole design: tasks are created in different ways, and the same list is ordered in different ways.", "size": 12.5, "color": INK, "font": SANS_SB, "line": 1.3}], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 5)
notes(s, NAME1 + ".\n"
    "Functional: create three task types, order three ways, validated lifecycle, filter and summarise. Non-functional, where the architecture lives: extensible with no edits to old code, pure Java, runs three ways, explainable. One line: different creation, different ordering. Next, why each is hard.")

# 06 PROBLEM 1 ----------------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Problem definition  ·  problem 1"); tracker(s, 1)
title(s, "Tasks have different creation logic.")
sub(s, "Each task type has different fields and different defaults. Building them by hand ties every caller to the concrete classes.")
code(s, M, 2.95, SW-2*M, [
    'new BugTask(title, priority, "MEDIUM", "");          // severity + steps',
    'new FeatureTask(title, priority, 8, 5);              // effort + value',
    'new DocumentationTask(title, priority, "API", "Developers");'], accent=CLAY)
iconcol3(s, [("The flaw","Every entry point imports and names BugTask, FeatureTask, and DocumentationTask directly."),
             ("The cost","Adding a fourth type means hunting down and editing every place that builds a task."),
             ("What we need","We need to make a task from a type identifier, so the caller never names a concrete class.")],
         y=4.95, specs=[(AMBER,AMBER_T,"alert-triangle","amber"),(RED,RED_T,"git-branch-01","red"),(GREEN,GREEN_T,"magic-wand-01","green")])
footer(s, 6)
notes(s, NAME1 + ".\n"
    "Creation. The three constructors are genuinely different — own fields and defaults. Flaw: every caller imports each concrete class. Cost: a fourth type means editing every call site. Need: build from an identifier like \"BUG\". That's Factory Method.")

# 07 PROBLEM 2 ----------------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Problem definition  ·  problem 2"); tracker(s, 1)
title(s, "Ordering depends on the moment.")
sub(s, "The same task list is sorted differently at different times. The list never changes; only the rule does.")
code(s, M, 2.95, SW-2*M, [
    'switch (sortMode) {',
    '    case DEADLINE: /* sort by due date   */ break;',
    '    case SEVERITY: /* bugs first, by rank */ break;',
    '    case URGENT:   /* sort by priority    */ break;',
    '}'], accent=TEAL)
iconcol3(s, [("The flaw","One switch statement inside the manager grows to carry every ordering rule."),
             ("The cost","Each new context edits tested code, which breaks the Open/Closed principle."),
             ("What we need","The ordering should swap at runtime, and new orderings should drop in without touching the manager.")],
         y=5.02, specs=[(AMBER,AMBER_T,"alert-triangle","amber"),(RED,RED_T,"git-branch-01","red"),(GREEN,GREEN_T,"magic-wand-01","green")])
footer(s, 7)
notes(s, NAME1 + ".\n"
    "Ordering. Same list, three moments — deadline, severity, priority; only the rule changes. A switch inside the manager grows forever, and every new context edits tested code: an Open/Closed violation. Need: swap the ordering at runtime. That's Strategy. On to section two.")

# 08 SECTION 02 DIVIDER -------------------------------------------------------
s = slide(DARK)
divider(s, "Section 02", "The design patterns.",
        "Two patterns chosen to match the two problems, plus a third that the task lifecycle gave us at no extra cost.",
        "7C3AED", "puzzle-piece-01", 2)
# pattern colour legend, on a light key-strip so all three brand hues read on the colour field
rrect(s, M, 6.12, 6.98, 0.54, WHITE, radius=0.16)
leg=[("Factory Method","creational","BC5A2B"),("Strategy","behavioural","0E7C72"),("State","behavioural","7C3AED")]
lx=M+0.30
for lab,cat,hexc in leg:
    rrect(s, lx, 6.34, 0.26, 0.10, C(hexc), radius=0.5)
    text(s, lx+0.36, 6.21, 3.0, 0.36, [[{"t": lab+"  ", "size": 11.5, "color": INK, "font": SANS_SB},
                                        {"t": cat, "size": 10, "color": MUTE}]])
    lx += 0.36 + (2.18 if lab!="Strategy" else 1.66)
notes(s, NAME1 + ".\n"
    "Section two — the patterns, and most of the grade. For each: definition, why it fits, advantage, how we built it. Map the problems to the patterns, then Factory, Strategy, and a State bonus. Colour code through the deck: clay Factory, teal Strategy, violet State.")

# 09 PATTERN SELECTION --------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Pattern selection", VIOLET); tracker(s, 2)
title(s, "Matching patterns to problems.")
sub(s, "We did not start from the patterns. We started from the two problems, and each one maps cleanly to a single pattern.")
rows=[("package","clay",CLAY,CLAY_T,"Problem 1  ·  different creation logic","Factory Method","Creational","Decouples the caller from the concrete task classes."),
      ("switch-horizontal-01","teal",TEAL,TEAL_T,"Problem 2  ·  context-dependent ordering","Strategy","Behavioural","Makes each ordering a swappable object, chosen at runtime."),
      ("refresh-cw-01","violet",VIOLET,VIOLET_T,"Bonus  ·  the task lifecycle","State (in an enum)","Behavioural","Each status declares its own legal transitions.")]
y0=3.0
for i,(icon,key,acc,tint,prob,pat,cat,why) in enumerate(rows):
    y=y0+i*1.18
    rrect(s, M, y, SW-2*M, 1.0, CARD, CARDBD, 1.0, radius=0.05)
    chip(s, M+0.22, y+0.24, 0.52, tint, icon, key)
    text(s, M+1.0, y, 3.7, 1.0, [{"t": prob, "size": 12, "color": BODY, "line": 1.25}], anchor=MSO_ANCHOR.MIDDLE)
    place_icon(s, "arrow-narrow-right", "mute", M+5.05, y+0.5, 0.34)
    text(s, M+5.4, y, 3.2, 1.0, [[{"t": pat, "size": 16, "color": acc, "font": SERIF_SB}],
                                 [{"t": cat+" pattern", "size": 10, "color": MUTE, "space_before": 1, "font": SANS_MD}]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, M+8.55, y, SW-2*M-8.55-0.3, 1.0, [{"t": why, "size": 11.5, "color": BODY, "line": 1.25}], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 9)
notes(s, NAME1 + ".\n"
    "The bridge. Problem 1, creation, maps to Factory Method (clay). Problem 2, ordering, maps to Strategy (teal). Bonus: the lifecycle is naturally a State machine in one enum (violet). Natural mappings, not forced. Starting with Factory Method.")

# 10 FACTORY METHOD · definition ---------------------------------------------
s = slide(PAPER); eyebrow(s, "Pattern 1  ·  Factory Method", CLAY); tracker(s, 2)
title(s, "Factory Method, and why it fits.")
fm=[("book-open-01","clay",CLAY_T,"Definition","Define a method for making an object, and let each subclass decide which concrete class it produces."),
    ("puzzle-piece-01","clay",CLAY_T,"Why here","Every task type has its own construction rules and defaults. The caller should not have to know them."),
    ("plus-circle","clay",CLAY_T,"Advantage","A new task type is a new class. Code that creates tasks never changes when a type is added."),
    ("file-02","clay",CLAY_T,"Real world","A document app that opens PDF, DOCX, and TXT files through one Open action, without naming a concrete reader.")]
gap=0.5; colw=(SW-2*M-gap)/2; rh=1.74
for i,(icon,key,tint,h,b) in enumerate(fm):
    c,r=i%2,i//2; x=M+c*(colw+gap); y=2.55+r*(rh+0.26)
    card(s, x, y, colw, rh, tint, icon, key, h, b, tsize=14)
footer(s, 10)
notes(s, NAME1 + ".\n"
    "Factory Method: a method makes the object, each subclass decides the concrete class. We have an abstract TaskFactory and three subclasses. Why: each type has its own rules and defaults the caller shouldn't carry. Advantage: a new type is a new class, no creation code changes. Like an editor opening many formats through one Open. Next, the code.")

# 11 FACTORY METHOD · code ----------------------------------------------------
s = slide(PAPER); eyebrow(s, "Pattern 1  ·  Factory Method", CLAY); tracker(s, 2)
title(s, "How we built it.")
sub(s, "The manager keeps a registry of factories keyed by a string. The caller asks for a type by name and never sees a concrete class.")
code(s, M, 2.9, SW-2*M, [
    'manager.createTask("BUG", "Login broken", "OAuth callback fails", 8);',
    'manager.createTask("FEATURE", "Dark mode", "Top user request", 5);'], accent=CLAY)
gap=0.5; colw=(SW-2*M-gap)/2
card(s, M, 4.62, colw, 1.78, CLAY_T, "package", "clay", "An abstract class, not an interface",
     "Each subclass owns its defaults: a bug is MEDIUM severity, a feature is 8h of effort at value 5, a doc targets developers.", tsize=13.5, bsize=11.5)
card(s, M+colw+gap, 4.62, colw, 1.78, CLAY_T, "layers-three-01", "indigo", "A template method on the base",
     "createTaskWithDeadline wraps createTask and attaches a deadline once. Written once, reused by all three factories.", tsize=13.5, bsize=11.5)
footer(s, 11)
notes(s, NAME1 + ".\n"
    "The manager keeps a Map from a string key to a factory; createTask(\"BUG\", ...) looks it up — the caller never imports BugTask. We added Documentation late and it just appeared in the menu. Two choices: an abstract class so each subclass owns its defaults, and createTaskWithDeadline as a Template Method on the base, written once. Now, Strategy.")

# 12 STRATEGY · definition ----------------------------------------------------
s = slide(PAPER); eyebrow(s, "Pattern 2  ·  Strategy", TEAL); tracker(s, 2)
title(s, "Strategy, and why it fits.")
st=[("book-open-01","teal",TEAL_T,"Definition","Define a family of interchangeable algorithms, wrap each one, and select between them at runtime."),
    ("puzzle-piece-01","teal",TEAL_T,"Why here","The same task list must be ordered differently in different moments, while the app is running."),
    ("plus-circle","teal",TEAL_T,"Advantage","Add or switch an ordering without touching the code that holds and manages the list."),
    ("compass","teal",TEAL_T,"Real world","Like picking a route in a maps app: fastest, shortest, or no tolls, over the same map.")]
gap=0.5; colw=(SW-2*M-gap)/2; rh=1.74
for i,(icon,key,tint,h,b) in enumerate(st):
    c,r=i%2,i//2; x=M+c*(colw+gap); y=2.55+r*(rh+0.26)
    card(s, x, y, colw, rh, tint, icon, key, h, b, tsize=14)
footer(s, 12)
notes(s, NAME1 + ".\n"
    "Strategy: a family of interchangeable algorithms behind one interface, chosen at runtime. Ours is PriorityStrategy, one sort method, three implementations. Why: the same list needs different orders while the app runs. Advantage: a new ordering is a new class; the manager never changes. Like routes in a maps app. Next, the code.")

# 13 STRATEGY · code ----------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Pattern 2  ·  Strategy", TEAL); tracker(s, 2)
title(s, "How we built it.")
sub(s, "Each ordering is a swappable object behind one interface. Changing the sort is a single setter call; the manager never learns which one is active.")
code(s, M, 2.9, SW-2*M, [
    'manager.setPriorityStrategy(new SeverityFirstStrategy());',
    '// the next call to getPrioritizedTasks() returns the new order'], accent=TEAL)
gap=0.5; colw=(SW-2*M-gap)/2
card(s, M, 4.5, colw, 1.9, TEAL_T, "switch-horizontal-01", "teal", "An interface, not a raw Comparator",
     "PriorityStrategy names the role. SeverityFirst also lifts bugs to the top before sorting the rest, which a pairwise Comparator handles awkwardly.", tsize=13.5)
card(s, M+colw+gap, 4.5, colw, 1.9, TEAL_T, "settings-01", "indigo", "A setter, not a constructor argument",
     "Users change the sort mid-session. A setter avoids rebuilding the manager and copying every task into a fresh instance.", tsize=13.5)
footer(s, 13)
notes(s, NAME1 + ".\n"
    "Small implementation: the manager holds one PriorityStrategy; one setter call changes the order, no recompile. Two choices: a named interface, not a raw Comparator, because SeverityFirst lifts bugs first (stateful); and a setter, not constructor injection, because users swap mid-session. Next slide shows it live.")

# 14 STRATEGY · live evidence -------------------------------------------------
s = slide(PAPER); eyebrow(s, "Pattern 2  ·  Strategy  ·  evidence", TEAL); tracker(s, 2)
title(s, "The same list, reordered live.")
gap=0.55; colw=(SW-2*M-gap)/2
img_panel(s, "gui-strategy.png", M, 2.5, colw, 3.7, accent=TEAL, caption="Urgent First sort: priority 5 down to 1.")
img_panel(s, "gui-severity.png", M+colw+gap, 2.5, colw, 3.7, accent=TEAL, caption="Severity First sort: both bugs rise to the top.")
footer(s, 14)
notes(s, NAME1 + ".\n"
    "Two real GUI screenshots, same five tasks. Left, Urgent First by priority; right, after switching to Severity First, both bugs jump to the top. Nothing recompiled — only the strategy object changed, via one setter on the dropdown. We'll do this live in the demo.")

# 15 BONUS · STATE ------------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Bonus pattern  ·  State", VIOLET); tracker(s, 2)
title(s, "The lifecycle is a state machine.")
img_panel(s, "state-diagram.png", M, 2.5, 5.95, 4.0, accent=VIOLET)
bx=7.15
points=[("TaskStatus owns its transitions","Each enum constant declares its legal next states through canTransitionTo()."),
        ("The base class enforces them","AbstractTask.setStatus() checks that table and throws on an illegal move."),
        ("No shortcuts","The engine refuses to jump OPEN straight to DONE; the cycle has to be walked."),
        ("State, for zero extra files","The whole pattern lives in one enum, with no extra classes.")]
for i,(h,b) in enumerate(points):
    y=2.55+i*1.0
    place_icon(s, "refresh-cw-01", "violet", bx+0.16, y+0.16, 0.32)
    text(s, bx+0.44, y, SW-M-bx-0.44, 0.4, [{"t": h, "size": 13, "color": INK, "font": SANS_SB}])
    text(s, bx+0.44, y+0.30, SW-M-bx-0.44, 0.7, [{"t": b, "size": 11, "color": BODY, "line": 1.28}])
footer(s, 15)
notes(s, NAME1 + ".\n"
    "Bonus. The rubric needs one creational and one behavioural; the lifecycle is a free State machine. Path: OPEN, IN_PROGRESS, REVIEW, DONE, plus BLOCKED and reject-back. Each status declares its legal next states via canTransitionTo, and setStatus throws on an illegal jump like OPEN to DONE. One enum, no extra classes. Over to " + NAME2 + " for the architecture.")

# 16 SECTION 03 DIVIDER -------------------------------------------------------
s = slide(DARK)
divider(s, "Section 03", "Architecture and implementation.",
        "How the design looks as classes, how one request flows through it, and how it satisfies all five SOLID principles.",
        "0E7C72", "grid-01", 3)
notes(s, NAME2 + ".\n"
    "Section three — the system as a whole. The class diagram by pattern, one create-task call at runtime, the file layout, and SOLID.")

# 17 CLASS · FACTORY METHOD ---------------------------------------------------
s = slide(PAPER); eyebrow(s, "Architecture  ·  structure  ·  Factory Method", CLAY); tracker(s, 3)
title(s, "Class view — the Factory Method side.", size=23)
sub(s, "TaskManager talks only to the abstract TaskFactory, which creates a Task. Each concrete factory and each concrete task slots in underneath.", y=2.12, size=11.5, color=MUTE)
img_panel(s, "class-factory.png", M, 2.74, SW-2*M, 3.98, accent=CLAY)
footer(s, 17)
notes(s, NAME2 + ".\n"
    "Factory side, split out for clarity. TaskManager depends only on the abstract TaskFactory; the three factories extend it; it creates a Task. Right is the product family. Every arrow points at an abstraction — Dependency Inversion — so a new type never touches the manager.")

# 18 CLASS · STRATEGY ---------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Architecture  ·  structure  ·  Strategy", TEAL); tracker(s, 3)
title(s, "Class view — the Strategy side.", size=23)
sub(s, "TaskManager holds one PriorityStrategy and can swap it at runtime. Each ordering is an interchangeable implementation of the same interface.", y=2.12, size=11.5, color=MUTE)
img_panel(s, "class-strategy.png", M, 2.74, SW-2*M, 3.98, accent=TEAL)
footer(s, 18)
notes(s, NAME2 + ".\n"
    "Strategy side, deliberately simple. The manager holds one PriorityStrategy through its two methods. The three orderings each implement one sort. Knowing only the interface, we add or swap an ordering with no edit to the manager — Open/Closed, straight from the pattern.")

# 19 SEQUENCE · CREATING A TASK -----------------------------------------------
s = slide(PAPER); eyebrow(s, "Architecture  ·  behaviour  ·  creation", CLAY); tracker(s, 3)
title(s, "Creating a task, step by step.", size=23)
sub(s, "The caller passes a type string; the manager looks up the registered factory and returns a Task. No concrete class is ever named by the caller.", y=2.12, size=11.5, color=MUTE)
img_panel(s, "seq-create.png", M, 2.74, SW-2*M, 3.98, accent=CLAY)
footer(s, 19)
notes(s, NAME2 + ".\n"
    "Runtime view of Factory Method. Main asks the manager for a BUG; the manager looks up the registered factory, which builds a BugTask and returns it as a Task. The caller never writes new BugTask. The dynamic side of the class diagram.")

# 20 SEQUENCE · ORDERING THE LIST ---------------------------------------------
s = slide(PAPER); eyebrow(s, "Architecture  ·  behaviour  ·  ordering", TEAL); tracker(s, 3)
title(s, "Ordering the list, step by step.", size=23)
sub(s, "Set a strategy, then ask for the prioritized list. The manager delegates the sort to whichever strategy is currently set.", y=2.12, size=11.5, color=MUTE)
img_panel(s, "seq-order.png", M, 2.74, SW-2*M, 3.98, accent=TEAL)
footer(s, 20)
notes(s, NAME2 + ".\n"
    "Runtime view of Strategy. Set a strategy — DeadlineFirst — then ask for the prioritized list. The manager doesn't sort; it delegates to whichever strategy is set. Swap in SeverityFirst and the same call returns a new order, no recompile. The manager owns the list, the strategy owns the rule.")

# 21 IMPLEMENTATION OVERVIEW --------------------------------------------------
s = slide(PAPER); eyebrow(s, "Implementation  ·  structure", TEAL); tracker(s, 3)
title(s, "Sixteen files, three layers.")
sub(s, "No package declarations, only java.util and java.time imported. The columns mirror the three layers of the class diagram.")
gap=0.45; colw=(SW-2*M-2*gap)/3
listpanel(s, M, 2.74, colw, 3.6, INDIGO_T, "cube-01", "indigo", "Product layer",
    ["Task (interface)","AbstractTask (base)","BugTask, FeatureTask","DocumentationTask","TaskStatus (enum)"], INDIGO, isize=11.5, gap=0.5)
listpanel(s, M+colw+gap, 2.74, colw, 3.6, VIOLET_T, "puzzle-piece-01", "violet", "Pattern layer",
    ["TaskFactory (abstract)","Bug / Feature / Doc factories","PriorityStrategy (interface)","UrgentFirst, DeadlineFirst","SeverityFirst"], VIOLET, isize=11.5, gap=0.5)
listpanel(s, M+2*(colw+gap), 2.74, colw, 3.6, TEAL_T, "settings-01", "indigo", "Coordination",
    ["TaskManager (coordinator)","Main (automated tests)","TaskManagementApp (console)","gui.TaskManagerGUI (Swing)"], TEAL, isize=11.5, gap=0.5)
rrect(s, M, 6.5, SW-2*M, 0.46, PANEL, radius=0.06)
text(s, M+0.3, 6.5, SW-2*M-0.6, 0.46, [{"t": "All three entry points drive the same engine through its public API.   2 interfaces · 1 enum · 1 abstract · 12 concrete classes.", "size": 11, "color": BODY, "line": 1.2}], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 21)
notes(s, NAME2 + ".\n"
    "Sixteen files, three layers: product (Task, AbstractTask, three tasks, the enum), pattern (the abstract factory and its three, the strategy interface and its three), coordination (one TaskManager plus three entry points). Only java.util and java.time. All three entry points drive the same engine, so GUI and console behave identically.")

# 22 SOLID --------------------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Implementation  ·  principles", TEAL); tracker(s, 3)
title(s, "How the design meets SOLID.")
sol=[("target-01","indigo",INDIGO_T,"S · Single responsibility","Factories build, strategies sort, the manager coordinates. One reason to change each."),
     ("lock-unlocked-01","indigo",INDIGO_T,"O · Open / Closed","A new task type or sort is a new file plus one line. Zero edits to existing classes."),
     ("switch-vertical-01","indigo",INDIGO_T,"L · Liskov substitution","Every factory works through the abstract reference; every strategy through the interface."),
     ("columns-02","indigo",INDIGO_T,"I · Interface segregation","PriorityStrategy declares one method; the Task interface stays minimal."),
     ("anchor","indigo",INDIGO_T,"D · Dependency inversion","The manager's fields are all interfaces and abstract types, never concretes."),
     ("layers-three-01","indigo",INDIGO_T,"The throughline","Abstractions sit in the middle of the system; concrete classes live at the edges.")]
gap=0.45; colw=(SW-2*M-2*gap)/3; rh=1.78
for i,(icon,key,tint,h,b) in enumerate(sol):
    c,r=i%3,i//3; x=M+c*(colw+gap); y=2.5+r*(rh+0.24)
    card(s, x, y, colw, rh, tint, icon, key, h, b, tsize=12.5, bsize=10.8, cs=0.46)
footer(s, 22)
notes(s, NAME2 + ".\n"
    "SOLID falls out of the two patterns. S: factories build, strategies sort, manager coordinates. O: a new type or sort is a new file, zero edits. L: every factory and strategy stands in for its abstraction. I: one-method strategy interface, minimal Task. D: the manager references only abstractions — no new BugTask anywhere inside it. On to the live demonstration.")

# 23 SECTION 04 DIVIDER -------------------------------------------------------
s = slide(DARK)
divider(s, "Section 04", "Live demonstration.",
        "The compiled system, run three ways: the automated test suite, the interactive console, and the Swing GUI.",
        "1E7A45", "terminal", 4)
notes(s, NAME2 + ".\n"
    "Section four, the live demo. Terminal first to prove the architecture, then the GUI. Rehearsed to about three minutes; screenshots as backup if the projector fails.")

# 24 DEMO 1 · TERMINAL --------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Live demonstration  ·  demo 1  ·  the terminal", GREEN); tracker(s, 4)
title(s, "Demo 1 — the terminal.", size=27)
text(s, M, 2.04, SW-2*M, 0.4, [{"t": "Open a terminal in the project root folder, then paste the command for each step.", "size": 12, "color": BODY, "line": 1.3}])
GL=C("D8D4CA"); GG=C("5BD08F"); GM=C("857F73")
rows=[("$ java -cp bin Main", GG),
      ("", GL),
      ("########  Task Management System  ########", GM),
      ("", GL),
      ("  TEST 1   Factory Method Pattern", GL),
      ("     [PASS] correct types, no concretes", GG),
      ("  TEST 2   Strategy Pattern", GL),
      ("     [PASS] one list, three orderings", GG),
      ("  TEST 3   Lifecycle / State machine", GL),
      ("     [PASS] illegal moves are blocked", GG),
      ("  TEST 4-6 edge cases ........  6 / 6", GM),
      ("", GL),
      ("########     ALL TESTS PASSED     ########", GG)]
console(s, M, 2.62, 5.25, 4.06, rows, header="java -cp bin Main")
cx=M+5.62; cw=SW-M-cx
cmdcard(s, cx, 2.62, cw, "STEP 1 · BUILD ONCE", "javac -d bin src/main/java/*.java src/main/java/gui/*.java", GREEN, csize=10.5)
cmdcard(s, cx, 3.66, cw, "STEP 2 · RUN THE AUTOMATED TESTS", "java -cp bin Main", GREEN)
cmdcard(s, cx, 4.70, cw, "STEP 3 · OPEN THE INTERACTIVE CONSOLE", "java -cp bin TaskManagementApp", GREEN)
rrect(s, cx, 5.86, cw, 0.82, PANEL, radius=0.06)
text(s, cx+0.26, 5.86, cw-0.5, 0.82, [[{"t": "Inside the console menu:", "size": 10.5, "color": INK, "font": SANS_SB}],
     [{"t": "1 create a task (Factory)   ·   4 change the sort (Strategy)   ·   3 view sorted   ·   5 change status (State)", "size": 9.5, "color": BODY, "line": 1.25, "space_before": 3}]], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 24)
notes(s, NAME2 + ".\n"
    "Terminal first — it proves the architecture, not just the UI. Build once, then java -cp bin Main: six sections, ends ALL TESTS PASSED (the screen on the left). Then java -cp bin TaskManagementApp for the interactive console on the same engine — menu 1 creates via the factory, 4 then 3 swaps and re-lists, 5 walks the lifecycle. Then the GUI.")

# 25 DEMO 2 · GRAPHICAL USER INTERFACE ----------------------------------------
s = slide(PAPER); eyebrow(s, "Live demonstration  ·  demo 2  ·  graphical user interface", GREEN); tracker(s, 4)
title(s, "Demo 2 — the graphical interface.", size=25)
text(s, M, 2.04, SW-2*M, 0.4, [{"t": "From the same project root, one command launches the whole interface — the rest is clicks.", "size": 12, "color": BODY, "line": 1.3}])
img_panel(s, "gui-strategy.png", M, 2.62, 5.25, 4.06, accent=GREEN)
cx=M+5.62; cw=SW-M-cx
cmdcard(s, cx, 2.62, cw, "PASTE THIS TO LAUNCH THE GUI", "java -jar TaskManagerGUI.jar", GREEN, csize=15, h=1.08)
steps=[("browser","indigo",INDIGO_T,"Load the demo data","Demo ▸ Load Strategy Demo seeds the table with tasks."),
       ("switch-horizontal-01","teal",TEAL_T,"Strategy, live","Sort by: Urgent, Deadline, Severity — the table reorders, no recompile."),
       ("package-plus","clay",CLAY_T,"Factory, live","Add a task; the Type field picks which factory builds it."),
       ("refresh-cw-01","violet",VIOLET_T,"State machine","Mark OPEN ▸ DONE: refused. OPEN ▸ IN_PROGRESS: allowed.")]
for i,(icon,key,tint,h,b) in enumerate(steps):
    y=4.06+i*0.72
    chip(s, cx, y, 0.44, tint, icon, key, frac=0.58)
    text(s, cx+0.60, y-0.04, cw-0.60, 0.3, [{"t": h, "size": 12, "color": INK, "font": SANS_SB}])
    text(s, cx+0.60, y+0.23, cw-0.60, 0.42, [{"t": b, "size": 10.2, "color": BODY, "line": 1.18}])
footer(s, 25)
notes(s, NAME2 + ".\n"
    "Same engine, Swing window. One command: java -jar TaskManagerGUI.jar, then load the demo data. Then clicks: cycle Sort by for Strategy; add a task, where Type picks the factory; mark OPEN to DONE — refused, OPEN to IN_PROGRESS — allowed, the State machine. On to the evaluation.")

# 26 SECTION 05 DIVIDER -------------------------------------------------------
s = slide(DARK)
divider(s, "Section 05", "Results, evaluation and conclusion.",
        "What the patterns delivered in practice, the honest limits of this build, and the main lesson.",
        "9A6304", "trophy-01", 5)
notes(s, NAME2 + ".\n"
    "Final section — measure against the objective, the honest limits, and the conclusion.")

# 27 RESULTS ------------------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Results  ·  what the patterns delivered", AMBER); tracker(s, 5)
title(s, "New types and orderings, without editing existing code.", size=27)
gap=0.5; colw=(SW-2*M-gap)/2
listpanel(s, M, 2.55, colw, 3.7, GREEN_T, "trend-up-01", "green", "Extension, in numbers", [
    "New task type: 2 new files, 1 line of registration, 0 edits.",
    "New ordering: 1 new file, 1 setter call, 0 edits.",
    "Test 5 in Main asserts this Open/Closed property at runtime."], GREEN, isize=12, gap=0.66)
listpanel(s, M+colw+gap, 2.55, colw, 3.7, GREEN_T, "check-circle", "green", "What worked in practice", [
    "Documentation type was added late, with zero edits to existing code.",
    "The GUI dropdown proves the Strategy swap, live.",
    "The lifecycle enum makes every illegal transition unreachable.",
    "Main doubles as the test harness, with no JUnit needed."], GREEN, isize=12, gap=0.66)
footer(s, 27)
notes(s, NAME2 + ".\n"
    "Did it work? A new type costs two files and one line; a new ordering, one file and one setter — zero edits either way, and Test 5 checks it at runtime. In practice: Documentation was added late with no edits, the GUI proves the live swap, the enum blocks illegal transitions, and Main was the test harness — no JUnit.")

# 28 LIMITATIONS --------------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Evaluation  ·  limitations and alternatives", AMBER); tracker(s, 5)
title(s, "An honest look at the design.")
iconcol3(s, [("Limitations","All data is in memory; nothing persists. Single user, no concurrency. Validation throws on the first error rather than collecting them all."),
             ("Alternatives we weighed","Abstract Factory: rejected, there is only one product family. A raw Comparator: loses the named role and the stateful sort."),
             ("Future work","Persistence via Repository, tags via Specification, async dispatch, and a small REST layer over the same engine.")],
         y=2.6, specs=[(AMBER,AMBER_T,"alert-circle","amber"),(INDIGO,INDIGO_T,"intersect-circle","indigo"),(INDIGO,INDIGO_T,"clock-fast-forward","indigo")])
rrect(s, M, 5.5, SW-2*M, 0.92, PANEL, radius=0.06)
text(s, M+0.3, 5.5, SW-2*M-0.6, 0.92, [{"t": "Every limitation above is a scoping choice, not a structural one. The engine is decoupled enough that each item is an addition, not a rewrite.", "size": 12, "color": INK, "font": SANS_MD, "line": 1.35}], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 28)
notes(s, NAME2 + ".\n"
    "Honest limits: in-memory only, single-user, validation throws on first error — deliberate scoping. Alternatives weighed: Abstract Factory (rejected — one product family), raw Comparator (loses the named role and the bugs-first sort). Future: persistence, tags, async, a REST layer. Each is an addition, not a rewrite.")

# 29 CONCLUSION ---------------------------------------------------------------
s = slide(PAPER); eyebrow(s, "Conclusion", AMBER); tracker(s, 5)
title(s, "What we set out to do, and what we learned.")
concl=[("check-verified-01","green",GREEN_T,"What we achieved","A working task system where new types and new orderings cost no edits to existing, tested code."),
       ("puzzle-piece-01","violet",VIOLET_T,"The patterns earned their place","Each was chosen to solve a concrete problem from section one, not to satisfy a checklist."),
       ("book-open-01","indigo",INDIGO_T,"The lesson","Naming a role, a factory or a strategy, makes the codebase explain itself to the next reader."),
       ("trophy-01","amber",AMBER_T,"The bigger point","Design patterns are a shared vocabulary that lets a team extend software without breaking what already works.")]
gap=0.5; colw=(SW-2*M-gap)/2; rh=1.74
for i,(icon,key,tint,h,b) in enumerate(concl):
    c,r=i%2,i//2; x=M+c*(colw+gap); y=2.55+r*(rh+0.26)
    card(s, x, y, colw, rh, tint, icon, key, h, b, tsize=13.5)
footer(s, 29)
notes(s, NAME2 + ".\n"
    "Achieved the objective: new types and orderings with no edits to working code. The patterns earned their place — each answered a real problem, not a checklist. The lesson: naming a factory or a strategy makes the code explain itself. The bigger point: patterns are a shared vocabulary for extending software safely. Thank you — questions welcome.")

# 30 THANK YOU (no names) -----------------------------------------------------
s = slide(DARK)
text(s, M, 2.5, 11.9, 1.8, [[{"t": "Thank you.", "size": 48, "color": WHITE, "font": SERIF_SB, "line": 1.04}],
                            [{"t": "Questions welcome.", "size": 48, "color": INDIGO_D, "font": SERIF_SB, "line": 1.04, "space_before": 4}]])
hline(s, M, 4.95, SW-2*M, RULE_DK, 1.0)
text(s, M, 5.18, 9.8, 1.0, [{"t": "We can speak to any part: the problem, the patterns, the architecture, the code, or the demo.", "size": 13, "color": GRAYW, "line": 1.4}])
# pattern legend echo
leg=[("Factory Method", CLAY),("Strategy", TEAL),("State", VIOLET)]
lx=M
for lab,col in leg:
    rrect(s, lx, 6.18, 0.26, 0.10, col, radius=0.5)
    text(s, lx+0.36, 6.06, 2.6, 0.34, [{"t": lab, "size": 11, "color": GRAYW, "font": SANS_SB}])
    lx += 0.36 + (2.0 if lab!="Strategy" else 1.5)
text(s, SW-M-3.4, 6.06, 3.4, 0.34, [{"t": "SEN3006 · SOFTWARE ARCHITECTURE", "size": 9.5, "color": GRAYW, "track": 1.4, "font": SANS_SB}], align=PP_ALIGN.RIGHT)
notes(s, "Both.\n"
    "Questions split by area: " + NAME1 + " takes the problem and the three patterns; " + NAME2 + " takes the architecture, demo, SOLID, and evaluation. Likely asks: abstract class vs interface (per-subclass defaults + Template Method); strategy vs Comparator (named role + partition-then-sort); string registry (runtime lookup); no JUnit (zero-dependency rule, Main as harness).")

# 31 APPENDIX · component view -----------------------------------------------
s = slide(PAPER); eyebrow(s, "Appendix  ·  supporting view"); tracker(s, 5)
title(s, "Component view.", size=27)
sub(s, "The module structure: the UI depends on the manager, which delegates to the factory and strategy modules over the shared domain model.")
img_panel(s, "component-diagram.png", M, 3.0, SW-2*M, 3.0, accent=INDIGO)
text(s, M, 6.18, SW-2*M, 0.3, [{"t": "Each box is a module; every arrow is a compile-time dependency pointing inward toward the manager and the abstractions.", "size": 9.5, "color": FAINT, "track": 0.4}], align=PP_ALIGN.CENTER)
footer(s, 31)
notes(s, "Appendix, for questions.\n"
    "Component view: UI, manager, factory, strategy, and domain modules. Every dependency points inward toward the manager and the abstractions — the module-level echo of the class diagram.")

# 32 APPENDIX · deployment view ----------------------------------------------
s = slide(PAPER); eyebrow(s, "Appendix  ·  supporting view"); tracker(s, 5)
title(s, "Deployment view.", size=27)
sub(s, "One JVM, one shared engine, three entry points. No network, no database, no external services.")
img_panel(s, "deployment-diagram.png", 2.7, 2.95, SW-2*2.7, 3.5, accent=INDIGO)
footer(s, 32)
notes(s, "Appendix, for questions.\n"
    "Deployment view: one JVM, one shared engine, three entry points. No network, no database — what zero dependencies means in practice.")

prs.save(OUT); print("SAVED", OUT, "|", len(prs.slides._sldIdLst), "slides")
