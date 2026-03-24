"""
Generates the COSC 3P32 Assignment 3 solution PDF.
Run with:  python3 generate_pdf.py
Output:    Assignment3_Solutions.pdf
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Preformatted, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── register Unicode-capable fonts ───────────────────────────────────────────
# Try common locations for DejaVu fonts; fall back to Helvetica if unavailable.
import os, sys

_DEJAVU_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu",              # Debian/Ubuntu
    "/usr/share/fonts/dejavu",                       # Fedora/RHEL
    "/usr/local/share/fonts/truetype/dejavu",        # BSD / custom installs
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts"),  # local
]

from reportlab.lib.fonts import addMapping

_dejavu_dir = next(
    (d for d in _DEJAVU_CANDIDATES if os.path.isfile(os.path.join(d, "DejaVuSans.ttf"))),
    None,
)

if _dejavu_dir:
    pdfmetrics.registerFont(TTFont("DejaVu",      os.path.join(_dejavu_dir, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(_dejavu_dir, "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Mono", os.path.join(_dejavu_dir, "DejaVuSansMono.ttf")))
    addMapping("DejaVu", 0, 0, "DejaVu")
    addMapping("DejaVu", 1, 0, "DejaVu-Bold")
    BASE_FONT, BASE_BOLD, BASE_MONO = "DejaVu", "DejaVu-Bold", "DejaVu-Mono"
else:
    # Helvetica is built-in but lacks full Unicode; arrows display as best-effort.
    print("Warning: DejaVu fonts not found; falling back to Helvetica.", file=sys.stderr)
    BASE_FONT, BASE_BOLD, BASE_MONO = "Helvetica", "Helvetica-Bold", "Courier"

# ── document setup ────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    "Assignment3_Solutions.pdf",
    pagesize=letter,
    leftMargin=1 * inch,
    rightMargin=1 * inch,
    topMargin=0.9 * inch,
    bottomMargin=0.9 * inch,
)

# ── styles ────────────────────────────────────────────────────────────────────
title_style = ParagraphStyle(
    "Title2", fontName=BASE_BOLD, fontSize=14, spaceAfter=2, alignment=TA_CENTER
)
subtitle_style = ParagraphStyle(
    "Subtitle2", fontName=BASE_FONT, fontSize=10, spaceAfter=10,
    textColor=colors.HexColor("#444444"), alignment=TA_CENTER
)
h1 = ParagraphStyle(
    "H1", fontName=BASE_BOLD, fontSize=12, spaceBefore=14, spaceAfter=4,
    textColor=colors.HexColor("#1a1a8c"),
)
h2 = ParagraphStyle(
    "H2", fontName=BASE_BOLD, fontSize=10.5, spaceBefore=10, spaceAfter=3,
    textColor=colors.HexColor("#333333"),
)
body = ParagraphStyle(
    "Body2", fontName=BASE_FONT, fontSize=9.5, spaceAfter=4, leading=14
)
body_indent = ParagraphStyle(
    "BodyIndent", fontName=BASE_FONT, fontSize=9.5, spaceAfter=3, leading=14,
    leftIndent=18
)
code_style = ParagraphStyle(
    "Code2", fontName=BASE_MONO, fontSize=8.5, leading=13, spaceAfter=4,
    backColor=colors.HexColor("#f5f5f5"), leftIndent=14, rightIndent=14,
    spaceBefore=2
)

def H(text, style=h1):  return Paragraph(text, style)
def P(text, style=body): return Paragraph(text, style)
def PI(text):            return Paragraph(text, body_indent)
def B(text):             return Paragraph(f"<font name='{BASE_BOLD}'>{text}</font>", body)
def SP(n=6):             return Spacer(1, n)
def HR():                return HRFlowable(width="100%", thickness=0.5,
                                           color=colors.grey, spaceAfter=6)
def CODE(text):          return Preformatted(text, code_style)

_HDR = {"BACKGROUND": (0,0,-1,0),
        "clr":  colors.HexColor("#dde4f0"),
        "fn":   BASE_BOLD}

def make_table(data, col_widths, center_all=True):
    tbl = Table(data, colWidths=col_widths)
    align = "CENTER" if center_all else "LEFT"
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#dde4f0")),
        ("FONTNAME",   (0,0), (-1,0), BASE_BOLD),
        ("FONTNAME",   (0,1), (-1,-1), BASE_FONT),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN",      (0,0), (-1,-1), align),
        ("LEFTPADDING",(0,0), (-1,-1), 5),
        ("RIGHTPADDING",(0,0), (-1,-1), 5),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
    ]))
    return tbl

# ── content ───────────────────────────────────────────────────────────────────
story = []

story += [
    Paragraph("COSC 3P32 – File and Database Systems", title_style),
    Paragraph("Assignment #3 – Solutions", subtitle_style),
    HR(),
    SP(4),
]

# ══════════════════════════════════════════════════════════════════════════════
# Q1
# ══════════════════════════════════════════════════════════════════════════════
story += [H("Question 1 [4 marks]")]

story += [
    P("<b>Relation:</b>  Assignments(cid, semester, aid, type, duedate, weight, maxmarks)"),
    P("<b>Codes:</b>  C = cid,  S = semester,  A = aid,  T = type,  "
      "D = duedate,  W = weight,  M = maxmarks"),
    SP(),
]

q1 = [
    ("a)", "The key (cid, semester, aid) determines all remaining attributes:",
     "CSA → TDWM"),
    ("b)", "There is only one assignment for a given course, semester, and due date:",
     "CSD → A"),
    ("c)", "Same weight for a given course and semester implies the same max marks:",
     "CSW → M"),
    ("d)", "Same type for the same course implies the same weight:",
     "CT → W"),
]
for lbl, desc, fd in q1:
    story += [
        B(f"{lbl}  {desc}"),
        PI(f"<b><font name='{BASE_MONO}'>{fd}</font></b>"),
        SP(4),
    ]
story.append(SP(8))

# ══════════════════════════════════════════════════════════════════════════════
# Q2
# ══════════════════════════════════════════════════════════════════════════════
story += [
    H("Question 2 [20 marks]"),
    P("<b>Schema:</b>  R = VWXYZ"),
    P("<b>FDs:</b>  F = { VW→XY,  V→X,  W→Z,  YZ→Z,  Z→V }"),
    SP(),
]

# --- 2a ---
story += [H("Part a)  Three independent reasons the table is not a legal instance  [6 marks]", h2)]

tbl = make_table(
    [["V","W","X","Y","Z"],
     ["v1","w1","x1","y1","z1"],
     ["v2","w1","x2","y2","z1"],
     ["v2","w2","x1","y2","z2"]],
    [0.7*inch]*5
)
story += [tbl, SP(6)]

story += [
    B("Reason 1 – V→X violated  (rows 2 and 3)."),
    PI("Both rows have V = v2, yet X = x2 in row 2 and X = x1 in row 3.  "
       "The FD V→X requires a unique X value for every V value."),
    SP(4),
    B("Reason 2 – Z→V violated  (rows 1 and 2)."),
    PI("Both rows have Z = z1, yet V = v1 in row 1 and V = v2 in row 2.  "
       "The FD Z→V requires a unique V value for every Z value."),
    SP(4),
    B("Reason 3 – W→V violated  (rows 1 and 2)."),
    PI("W→Z and Z→V together imply W→V (a member of F⁺).  "
       "Both rows have W = w1, yet V = v1 in row 1 and V = v2 in row 2, "
       "violating this derived dependency."),
    SP(10),
]

# --- 2b ---
story += [H("Part b)  FDs on R₁ = VWX and R₂ = WYZ  [4 marks]", h2)]

story += [
    B("R₁ = VWX"),
    PI("Project F onto {V, W, X} by computing closures:"),
    PI("• V⁺ ∩ VWX = {V,X}  →  V→X"),
    PI("• W⁺ = {W,Z,V,X} (via W→Z, Z→V, V→X);  W⁺ ∩ VWX = {V,W,X}  →  W→V  "
       "(W→X is implied by W→V + V→X and not listed separately)"),
    SP(2),
    PI("Non-trivial FDs on R₁ (not trivial, not implied by others in the set):"),
    PI(f"<b><font name='{BASE_MONO}'>V→X,   W→V</font></b>"),
    SP(8),

    B("R₂ = WYZ"),
    PI("Project F onto {W, Y, Z}:"),
    PI("• W⁺ = VWXYZ (W→Z, Z→V, V→X, then VW→XY adds Y);  W⁺ ∩ WYZ = WYZ  "
       "→  W→Z  and  W→Y"),
    PI("• Z⁺ ∩ WYZ = {Z};  Y⁺ ∩ WYZ = {Y};  YZ⁺ ∩ WYZ = {Y,Z}  →  all trivial"),
    SP(2),
    PI("Non-trivial FDs on R₂:"),
    PI(f"<b><font name='{BASE_MONO}'>W→Z,   W→Y</font></b>   (equivalently W→YZ)"),
    SP(10),
]

# --- 2c ---
story += [H("Part c)  Is the decomposition lossless-join?  [2 marks]", h2)]
story += [
    P("R₁ ∩ R₂ = <b>{W}</b>."),
    P("W⁺ under F = VWXYZ, so W→VWX = R₁.  "
      "Because the shared attribute W is a superkey of R₁, "
      "the decomposition is <b>lossless-join</b>.  ✓"),
    SP(10),
]

# --- 2d ---
story += [H("Part d)  Lossless-join BCNF decomposition  [5 marks]", h2)]

story += [
    B("Step 0 – Find the candidate key of R."),
    PI("W⁺: W→(W→Z)→Z→(Z→V)→V→(V→X)→X, "
       "and with both V,W available VW→(VW→XY)→Y.  W⁺ = VWXYZ = R."),
    PI("Unique candidate key of R:  <b>W</b>."),
    SP(4),

    B("Step 0 – Identify BCNF violations."),
    PI("• VW→XY: VW ⊇ {W} (key) → superkey ✓"),
    PI("• <b>V→X</b>:  V⁺ = VX ≠ R  →  violation"),
    PI("• W→Z: W is key → superkey ✓"),
    PI("• YZ→Z: trivial ✓"),
    PI("• <b>Z→V</b>:  Z⁺ = VXZ ≠ R  →  violation"),
    SP(4),

    B("Step 1 – Decompose using V→X   (V⁺ = {V,X})."),
    PI("R_A = VX   (key: V;  FD: V→X;  BCNF ✓)"),
    PI("R_B = VWYZ   (key: W;  "
       "BCNF violation: Z→V because Z⁺ ∩ VWYZ = VZ ≠ VWYZ)"),
    SP(4),

    B("Step 2 – Decompose R_B = VWYZ using Z→V   (Z⁺ ∩ VWYZ = {V,Z})."),
    PI("R_C = VZ   (key: Z;  FD: Z→V;  BCNF ✓)"),
    PI("R_D = WYZ   (key: W;  FDs: W→Z, W→Y;  both have superkey on LHS  → BCNF ✓)"),
    SP(6),

    B("Final BCNF decomposition:"),
    SP(4),
]
story.append(
    make_table(
        [["Relation","Key","FDs"],
         ["VX", "V", "V→X"],
         ["VZ", "Z", "Z→V"],
         ["WYZ","W","W→Z,   W→Y"]],
        [1.2*inch, 0.7*inch, 2.8*inch]
    )
)
story.append(SP(10))

# --- 2e ---
story += [H("Part e)  Is the BCNF decomposition dependency-preserving?  [3 marks]", h2)]

story += [
    B("Compute the minimal cover of F:"),
    PI("1. Decompose RHS:  { VW→X, VW→Y, V→X, W→Z, YZ→Z, Z→V }"),
    PI("2. Remove trivial FD YZ→Z."),
    PI("3. Minimize LHS of VW→X:  W⁺ (without VW→X) = {W,Z,V,X};  "
       "X ∈ W⁺  →  V redundant  →  replace with W→X."),
    PI("4. Minimize LHS of VW→Y:  W⁺ (without VW→Y) = {W,Z,V,X};  "
       "Y ∉ W⁺  →  V is not redundant.  VW→Y stays."),
    PI("5. Remove redundant FDs:  W→X is implied by W→Z, Z→V, V→X  →  remove W→X."),
    PI(f"<b>Minimal cover:  "
       f"<font name='{BASE_MONO}'>{{ VW→Y,  V→X,  W→Z,  Z→V }}</font></b>"),
    SP(6),
]
story.append(
    make_table(
        [["FD","Preserved in","Without join?"],
         ["V→X",  "VX",  "✓"],
         ["W→Z",  "WYZ", "✓"],
         ["Z→V",  "VZ",  "✓"],
         ["VW→Y", "WYZ has W→Y;  augmentation gives VW→Y", "✓"]],
        [0.9*inch, 3.0*inch, 0.9*inch],
        center_all=False
    )
)
story += [
    SP(6),
    P("All FDs in the minimal cover are preserved without joining. "
      "The decomposition <b>is dependency-preserving</b>.  ✓"),
    SP(14),
]

# ══════════════════════════════════════════════════════════════════════════════
# Q3
# ══════════════════════════════════════════════════════════════════════════════
story += [
    H("Question 3 [11 marks]"),
    P("<b>Schema:</b>  R = ABCDEGH"),
    P("<b>FDs:</b>  F = { B→AGH,  CD→B,  C→EG,  E→AD,  G→E }"),
    SP(),
]

# --- 3a ---
story += [H("Part a)  Minimal cover  [6 marks]", h2)]

story += [
    B("Step 1 – Decompose all RHS into singletons:"),
    PI("{ B→A,  B→G,  B→H,  CD→B,  C→E,  C→G,  E→A,  E→D,  G→E }"),
    SP(4),

    B("Step 2 – Minimize left-hand sides."),
    PI("Only CD→B has a multi-attribute LHS."),
    PI("• Remove C?  D⁺ = {D}.  B ∉ D⁺  →  C is not redundant."),
    PI("• Remove D?  C⁺ (without CD→B) = {C,E,G,A,D}.  B ∉ C⁺  →  D is not redundant."),
    PI("CD→B stays unchanged."),
    SP(4),

    B("Step 3 – Remove redundant FDs:"),
    PI("• B→A:  B⁺ = {B,G,H,E,A,D}  (via B→G→E→A).  A ∈ B⁺  →  "
       "<b>redundant, remove</b>."),
    PI("• B→G:  B⁺ without B→G = {B,H}.  G ∉  →  not redundant."),
    PI("• B→H:  B⁺ without B→H = {B,G,E,A,D}.  H ∉  →  not redundant."),
    PI("• CD→B:  (CD)⁺ without CD→B = {C,D,E,G,A}.  B ∉  →  not redundant."),
    PI("• C→E:  C⁺ without C→E = {C,G,E,A,D}  (via C→G→E).  E ∈ C⁺  →  "
       "<b>redundant, remove</b>."),
    PI("• C→G:  C⁺ without C→G = {C}.  G ∉  →  not redundant."),
    PI("• E→A:  E⁺ without E→A = {E,D}.  A ∉  →  not redundant."),
    PI("• E→D:  E⁺ without E→D = {E,A}.  D ∉  →  not redundant."),
    PI("• G→E:  G⁺ without G→E = {G}.  E ∉  →  not redundant."),
    SP(6),

    B("Minimal cover:"),
    PI(f"<b><font name='{BASE_MONO}'>{{ B→GH,  CD→B,  C→G,  E→AD,  G→E }}</font></b>"),
    PI("(individual FDs: B→G,  B→H,  CD→B,  C→G,  E→A,  E→D,  G→E)"),
    SP(10),
]

# --- 3b ---
story += [H("Part b)  Candidate keys  [2 marks]", h2)]

story += [
    P("RHS attributes in the minimal cover: {G, H, B, A, D, E}."),
    P("Attribute <b>C</b> never appears on any RHS  →  C must be in every candidate key."),
    SP(4),
    P("Compute C⁺:"),
    PI("C →(C→G)→ G →(G→E)→ E →(E→A, E→D)→ A, D.  "
       "Now C and D are in the closure →(CD→B)→ B →(B→H)→ H."),
    PI("C⁺ = ABCDEGH = R.  ✓"),
    SP(4),
    P("C alone is a superkey; no proper subset is a superkey.  "
      "<b>Unique candidate key: { C }</b>"),
    SP(10),
]

# --- 3c ---
story += [H("Part c)  3NF Synthesis  [3 marks]", h2)]

story += [
    B("Step 1 – Create one relation per FD group in the minimal cover:"),
    SP(4),
    make_table(
        [["Relation","Generating FD(s)","Key"],
         ["BGH",  "B→GH",  "B"],
         ["BCD",  "CD→B",  "CD  (also C alone, since C→D holds via the chain C→G→E→D)"],
         ["CG",   "C→G",   "C"],
         ["ADE",  "E→AD",  "E"],
         ["GE",   "G→E",   "G"]],
        [0.7*inch, 1.3*inch, 2.8*inch],
        center_all=False
    ),
    SP(6),

    B("Step 2 – Ensure a candidate key of R is present."),
    PI("The unique candidate key is {C}.  Relation BCD contains C  "
       "→  no extra key relation needed. ✓"),
    SP(4),

    B("Step 3 – Remove redundant relations."),
    PI("No relation is a subset of any other.  None removed."),
    SP(6),

    B("Final 3NF decomposition:  { BGH, BCD, CG, ADE, GE }"),
    SP(6),

    make_table(
        [["Relation", "Non-trivial FDs  (not implied by others in the same set)"],
         ["BGH",  "B→GH"],
         ["BCD",  "C→BD,   B→D\n"
                  "(C is the sole candidate key of BCD;  "
                  "C→D holds via C→G→E→D;  "
                  "B→D holds via B→G→E→D projected onto BCD;\n"
                  "CD→B is implied by C→B, a part of C→BD)"],
         ["CG",   "C→G"],
         ["ADE",  "E→AD"],
         ["GE",   "G→E"]],
        [0.65*inch, 4.15*inch],
        center_all=False
    ),
    SP(6),

    P("<b>Lossless-join:</b>  BCD contains C (the sole candidate key of R).  "
      "The 3NF synthesis algorithm guarantees a lossless-join decomposition. ✓"),
    P("<b>Dependency-preserving:</b>  Every FD in the minimal cover is directly "
      "represented in one of the relations  "
      "(B→GH ∈ BGH,  CD→B ∈ BCD,  C→G ∈ CG,  E→AD ∈ ADE,  G→E ∈ GE). ✓"),
    SP(14),
]

# ══════════════════════════════════════════════════════════════════════════════
# Q4
# ══════════════════════════════════════════════════════════════════════════════
story += [
    H("Question 4 [15 marks]"),
    P("<b>Schema:</b>  Restaurant(<u>rname</u>, address, phone, stars)   "
      "Chef(<u>cname</u>, specialdish, rating)   "
      "CooksFor(<u>cname, rname</u>, salary)   "
      "Offers(<u>rname, dishname</u>, price)"),
    SP(),
]

story += [H("Part a)  CHECK: chef rating between 0 and 10  [2 marks]", h2)]
story += [
    P("Add to the <b>Chef</b> table definition:"),
    CODE("CHECK (rating >= 0 AND rating <= 10)"),
    SP(8),
]

story += [H("Part b)  CHECK: no chef salary at 'BigMac' exceeds 100  [2 marks]", h2)]
story += [
    P("Add to the <b>CooksFor</b> table definition:"),
    CODE("CHECK (rname <> 'BigMac' OR salary <= 100)"),
    SP(8),
]

story += [H("Part c)  Assertion: every restaurant has at least one chef  [3 marks]", h2)]
story += [
    CODE("""\
CREATE ASSERTION every_restaurant_has_chef
CHECK (
    NOT EXISTS (
        SELECT *
        FROM   Restaurant R
        WHERE  NOT EXISTS (
                   SELECT *
                   FROM   CooksFor CF
                   WHERE  CF.rname = R.rname
               )
    )
);"""),
    SP(8),
]

story += [H("Part d)  Assertion: every offered dish has a chef whose special dish it is  [3 marks]", h2)]
story += [
    CODE("""\
CREATE ASSERTION every_dish_has_special_chef
CHECK (
    NOT EXISTS (
        SELECT *
        FROM   Offers O
        WHERE  NOT EXISTS (
                   SELECT *
                   FROM   Chef C
                   WHERE  C.specialdish = O.dishname
               )
    )
);"""),
    SP(8),
]

story += [H("Part e)  Trigger: 10% salary raise when stars increase  [5 marks]", h2)]
story += [
    CODE("""\
CREATE TRIGGER stars_raise
AFTER UPDATE OF stars ON Restaurant
REFERENCING OLD ROW AS old_row
            NEW ROW AS new_row
FOR EACH ROW
WHEN (new_row.stars > old_row.stars)
BEGIN ATOMIC
    UPDATE CooksFor
    SET    salary = salary * 1.10
    WHERE  rname = new_row.rname;
END;"""),
    SP(4),
    P("The <b>WHEN</b> clause ensures the trigger fires only when the star rating "
      "<i>increases</i>.  The <b>FOR EACH ROW</b> granularity makes the updated "
      "restaurant's rname available via new_row.  The 10% raise is applied to every "
      "chef currently listed in CooksFor for that restaurant."),
]

# ── build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print("PDF written to Assignment3_Solutions.pdf")
