"""
app.py  ─  AI Resume Analyzer — Premium Full Dashboard
-------------------------------------------------------
• All inputs on main page (no sidebar)
• 5 clickable result tabs:
    📊 Match Score | 🛠️ Skills | 💼 Career | 📚 Roadmap | 📄 Resume Guide
• Roadmap: JD-aware motivational lines + time estimates
• Resume Guide: 4 clickable role templates with full preview
"""

import math
import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills, get_resume_summary
from utils.matcher import calculate_match_score, get_matched_and_missing_skills
from utils.roadmap import recommend_careers, generate_roadmap
from data.skills_db import SKILLS_DB

# ══════════════════════════════════════════════════════════════════════════════
#  DATA — MOTIVATIONS + TIME ESTIMATES
# ══════════════════════════════════════════════════════════════════════════════
SKILL_MOTIVATIONS = {
    "python":             "🐍 Python powers 80% of AI/ML workflows globally — this is your most impactful next step.",
    "machine learning":   "🤖 ML engineers are the most sought-after tech professionals right now. Close this gap and watch your inbox explode with opportunities.",
    "deep learning":      "🧠 Deep Learning separates good data scientists from great ones. Master it and you'll be building the systems of tomorrow.",
    "sql":                "🗄️ SQL is the universal language of data — every role in data, analytics, and engineering requires it. Start here.",
    "tableau":            "📊 Data storytelling is a superpower. Tableau lets your insights speak louder than a thousand lines of code.",
    "power bi":           "📈 Microsoft's data stack dominates enterprise. Power BI fluency gets you hired faster in corporate environments.",
    "pandas":             "🐼 Pandas is the cornerstone of Python data work — non-negotiable for any data role. Learn it once, use it forever.",
    "numpy":              "🔢 NumPy is the engine beneath every ML model. Every mathematical concept in AI runs through it.",
    "scikit-learn":       "⚙️ scikit-learn is the industry go-to for production ML. Build 3 real projects with it and you'll be hireable.",
    "tensorflow":         "🔥 TensorFlow is the standard for enterprise deep learning. Google, Netflix, and Uber all use it in production.",
    "pytorch":            "🔦 PyTorch is taking over both research and industry. Knowing it puts you ahead of 90% of candidates.",
    "nlp":                "💬 NLP is exploding with the rise of LLMs. Understanding these fundamentals makes you ChatGPT-era ready.",
    "flask":              "🌐 Flask lets you deploy models as APIs — turning code into real products is what gets you hired.",
    "django":             "🏗️ Django is Python's most powerful web framework. It's the bridge between data and full-stack Python roles.",
    "git":                "🌿 Git is the #1 collaboration tool in all of tech. No modern employer hires without it.",
    "docker":             "🐳 Docker is the industry standard for deployment. Containerize your projects and impress every hiring manager.",
    "statistics":         "📐 Statistics is the foundation of all ML. Strong stats intuition = stronger, more trustworthy models.",
    "data visualization": "🎨 Visualization bridges code and insight. Decision-makers remember charts — not raw numbers.",
    "rest api":           "🔌 REST APIs connect the modern tech world. This skill makes you a full-stack thinker in any data role.",
    "mongodb":            "🍃 NoSQL is the backbone of scalable modern apps. MongoDB fluency opens backend and data engineering doors.",
    "mysql":              "🛢️ MySQL is the world's most-used relational database. Mastering it gives you foundational data skills.",
    "postgresql":         "🐘 PostgreSQL is the production-grade DB of choice. Knowing it sets you above every entry-level SQL candidate.",
    "r":                  "📉 R is the statistician's secret weapon. For research-heavy and academic data roles, it's indispensable.",
    "javascript":         "⚡ JS makes data interactive. A web-visible ML project gets 10x more recruiter attention than a Jupyter notebook.",
    "data analysis":      "🔍 Data analysis is where value creation starts. Sharpen this skill and every dataset becomes an opportunity.",
    "excel":              "📋 Excel is still the most-used data tool in business. Advanced Excel skills deliver immediate, visible value.",
    "github":             "🐙 GitHub is your professional portfolio. A well-curated profile is worth more than a cover letter.",
    "css":                "🎨 CSS brings your data projects to life on the web. Visual polish separates amateur work from professional.",
    "html":               "🌐 HTML is the backbone of everything on the web. Every data dashboard, every portfolio — it starts here.",
    "streamlit":          "⚡ Streamlit is the fastest way to turn ML into shareable apps. Knowing it means your models get seen.",
    "java":               "☕ Java remains one of the most widely-used enterprise languages. This skill opens big-tech and fintech doors.",
    "c++":                "💻 C++ powers high-performance systems and game engines. Mastering it signals strong engineering fundamentals.",
    "c":                  "⚙️ C is the language that built modern computing. Knowing it gives you deep insight into how software really works.",
}

SKILL_TIME = {
    "python": "4–6 weeks", "machine learning": "6–8 weeks", "deep learning": "8–10 weeks",
    "sql": "2–3 weeks", "tableau": "2–3 weeks", "power bi": "2–3 weeks",
    "pandas": "2–3 weeks", "numpy": "1–2 weeks", "scikit-learn": "3–4 weeks",
    "tensorflow": "6–8 weeks", "pytorch": "6–8 weeks", "nlp": "4–6 weeks",
    "flask": "2–3 weeks", "django": "3–4 weeks", "git": "1–2 weeks",
    "docker": "2–3 weeks", "statistics": "4–5 weeks", "data visualization": "2–3 weeks",
    "rest api": "2–3 weeks", "mongodb": "2–3 weeks", "mysql": "2–3 weeks",
    "data analysis": "3–4 weeks", "r": "4–5 weeks", "javascript": "6–8 weeks",
}

def get_jd_role(jd_text: str) -> str:
    """Detect likely job role from JD text for contextual motivation."""
    jd_lower = jd_text.lower()
    if any(k in jd_lower for k in ["data scientist", "machine learning engineer", "ml engineer"]):
        return "Data Science / ML"
    if any(k in jd_lower for k in ["python developer", "backend engineer", "software engineer", "full stack"]):
        return "Python / Software Engineering"
    if any(k in jd_lower for k in ["data analyst", "business analyst", "analytics engineer"]):
        return "Data Analytics"
    if any(k in jd_lower for k in ["ai engineer", "artificial intelligence", "deep learning", "nlp engineer"]):
        return "AI / Deep Learning"
    return "Tech"

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeAI — Smart Career Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── SESSION STATE ─────────────────────────────────────────────────────────────

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@400;500&display=swap');

*, *::before, *::after {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}

.stApp {
    background: #070b14 !important;
    background-image:
        radial-gradient(ellipse 75% 55% at 5% 5%,   rgba(99,102,241,0.14) 0%, transparent 65%),
        radial-gradient(ellipse 55% 45% at 95% 95%,  rgba(139,92,246,0.09) 0%, transparent 65%) !important;
}
#MainMenu, footer, header { visibility: hidden !important; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 2rem 4rem 7rem 4rem !important; max-width: 1200px !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important; border: none !important; border-radius: 14px !important;
    padding: 0.88rem 2rem !important; font-weight: 700 !important; font-size: 1rem !important;
    width: 100% !important; transition: all 0.25s ease !important;
    box-shadow: 0 4px 22px rgba(99,102,241,0.42) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.65) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] > div {
    background: rgba(99,102,241,0.04) !important;
    border: 2px dashed rgba(99,102,241,0.28) !important;
    border-radius: 12px !important; transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"] > div:hover { border-color: rgba(99,102,241,0.55) !important; }
[data-testid="stFileUploader"] label { display: none !important; }

/* ── Textarea ── */
.stTextArea textarea {
    background: rgba(10,14,28,0.9) !important;
    border: 1px solid rgba(99,102,241,0.22) !important;
    border-radius: 12px !important; color: #cbd5e1 !important;
    font-size: 0.875rem !important; padding: 0.9rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.55) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important; outline: none !important;
}
.stTextArea textarea::placeholder { color: #3d4a63 !important; }
.stTextArea label { display: none !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(11,16,32,0.88) !important;
    border: 1px solid rgba(99,102,241,0.18) !important;
    border-radius: 18px !important; padding: 0.35rem !important; gap: 0.3rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border: none !important; border-radius: 13px !important;
    color: #475569 !important; font-weight: 600 !important; font-size: 0.87rem !important;
    padding: 0.65rem 1.3rem !important; transition: all 0.22s ease !important; cursor: pointer !important;
}
.stTabs [data-baseweb="tab"]:hover { background: rgba(99,102,241,0.1) !important; color: #a5b4fc !important; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,rgba(99,102,241,0.32),rgba(139,92,246,0.32)) !important;
    color: #e2e8f0 !important; box-shadow: 0 2px 12px rgba(99,102,241,0.22) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Alert / Spinner ── */
.stAlert { border-radius: 14px !important; }
.stSpinner > div > div { border-top-color: #6366f1 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }

/* ── Typography ── */
p, li, span, td, th { color: #94a3b8 !important; }
h1, h2, h3, h4 { color: #f1f5f9 !important; }

/* ── Score ring animation ── */
@keyframes drawRing {
    from { stroke-dashoffset: var(--circ); }
    to   { stroke-dashoffset: var(--offset); }
}

/* ── Roadmap timeline ── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.roadmap-card { animation: fadeSlideUp 0.5s ease forwards; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding:2.5rem 0 2rem;">
    <div style="display:inline-block;
         background:linear-gradient(135deg,rgba(99,102,241,0.15),rgba(139,92,246,0.15));
         border:1px solid rgba(99,102,241,0.35); border-radius:50px;
         padding:0.4rem 1.2rem; color:#a5b4fc; font-size:0.7rem; font-weight:700;
         letter-spacing:2.5px; margin-bottom:1.3rem;">
        ⚡ AI-POWERED CAREER INTELLIGENCE
    </div>
    <h1 style="font-size:3.4rem; font-weight:900; line-height:1.05;
         background:linear-gradient(135deg,#f8fafc 0%,#a5b4fc 45%,#67e8f9 100%);
         -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
         margin:0 0 1rem;">
        AI Resume Analyzer
    </h1>
    <p style="font-size:1rem; color:#4b5563; max-width:540px; margin:0 auto; line-height:1.8;">
        Upload your resume, paste a job description — get your
        <span style="color:#a5b4fc;font-weight:600;">match score</span>,
        <span style="color:#67e8f9;font-weight:600;">skill gaps</span>,
        <span style="color:#c084fc;font-weight:600;">motivational roadmap</span> &amp;
        <span style="color:#34d399;font-weight:600;">resume templates</span>.
    </p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  INPUT SECTION
# ══════════════════════════════════════════════════════════════════════════════
col_up, col_jd = st.columns([1, 1.5], gap="large")

with col_up:
    st.markdown("""
    <div style="background:rgba(11,16,32,0.8); backdrop-filter:blur(24px);
         border:1px solid rgba(99,102,241,0.2); border-radius:20px;
         padding:1.4rem 1.5rem 0.75rem; margin-bottom:0.5rem;">
        <div style="color:#a5b4fc; font-size:0.68rem; font-weight:700;
             letter-spacing:2px; margin-bottom:0.5rem;">📄 &nbsp;UPLOAD RESUME (PDF)</div>
        <div style="color:#334155; font-size:0.8rem; line-height:1.5; margin-bottom:0.75rem;">
            Drag &amp; drop or click to upload your <strong style="color:#6366f1;">PDF resume</strong>.
        </div>
    </div>""", unsafe_allow_html=True)
    uploaded_resume = st.file_uploader("Resume PDF", type=["pdf"], label_visibility="collapsed")

with col_jd:
    st.markdown("""
    <div style="background:rgba(11,16,32,0.8); backdrop-filter:blur(24px);
         border:1px solid rgba(99,102,241,0.2); border-radius:20px;
         padding:1.4rem 1.5rem 0.75rem; margin-bottom:0.5rem;">
        <div style="color:#a5b4fc; font-size:0.68rem; font-weight:700;
             letter-spacing:2px; margin-bottom:0.5rem;">📋 &nbsp;JOB DESCRIPTION</div>
        <div style="color:#334155; font-size:0.8rem; line-height:1.5; margin-bottom:0.75rem;">
            Paste the <strong style="color:#6366f1;">full job description</strong> to match against.
        </div>
    </div>""", unsafe_allow_html=True)
    jd_text_input = st.text_area(
        "Job Description", height=175, label_visibility="collapsed",
        placeholder="Paste the full job description here…",
    )

st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)
_, btn_col, _ = st.columns([1.5, 2, 1.5])
with btn_col:
    analyze_button = st.button("🔍  Analyze My Resume", use_container_width=True)

st.markdown("""
<div style="height:1px; margin:2rem 0;
     background:linear-gradient(90deg,transparent,rgba(99,102,241,0.3),transparent);">
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPER — pill tags
# ══════════════════════════════════════════════════════════════════════════════
def make_pills(skills, color, bg, border, empty_msg):
    if not skills:
        return f'<span style="color:#334155;font-size:0.85rem;font-style:italic;">{empty_msg}</span>'
    pills = ""
    for s in skills:
        pills += f"""<span style="display:inline-block;background:{bg};
            border:1px solid {border};color:{color};border-radius:50px;
            padding:0.35rem 0.95rem;font-size:0.78rem;font-weight:600;
            margin:0.28rem 0.22rem 0.28rem 0;white-space:nowrap;">{s.title()}</span>"""
    return pills


# ══════════════════════════════════════════════════════════════════════════════
#  SECTION LABEL helper
# ══════════════════════════════════════════════════════════════════════════════
def section_label(text):
    st.markdown(f"""
    <div style="color:#334155; font-size:0.67rem; font-weight:700;
         letter-spacing:2px; text-transform:uppercase; margin-bottom:0.6rem;">
        {text}
    </div>""", unsafe_allow_html=True)


def get_skill_category(skill: str) -> str:
    s_lower = skill.lower().strip()
    for cat, items in SKILLS_DB.items():
        if s_lower in [i.lower() for i in items]:
            return cat
    return "Other Technical & Domain Skills"


def categorize_skills(skills_list: list) -> dict:
    cat_map = {}
    for skill in skills_list:
        c = get_skill_category(skill)
        cat_map.setdefault(c, []).append(skill)
    return cat_map


# ══════════════════════════════════════════════════════════════════════════════
#  ANALYSIS RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if analyze_button:
    if not uploaded_resume:
        st.error("⚠️ Please upload a PDF resume to continue.")
    elif not jd_text_input.strip():
        st.error("⚠️ Please paste a job description to continue.")
    else:
        with st.spinner("Analyzing your resume with AI…"):
            resume_text = extract_text_from_pdf(uploaded_resume)

        if resume_text.startswith("ERROR"):
            st.error(resume_text)
        else:
            # ── RUN LOCAL ANALYSIS ENGINE ──
            resume_skills      = extract_skills(resume_text)
            jd_skills          = extract_skills(jd_text_input)
            match_score        = calculate_match_score(resume_text, jd_text_input)
            matched_skills, missing_skills = get_matched_and_missing_skills(resume_skills, jd_skills)
            career_suggestions = recommend_careers(resume_skills)
            roadmap            = generate_roadmap(missing_skills)
            summary            = get_resume_summary(resume_text)

            key_strengths      = [f"Strong background in {s.title()}" for s in matched_skills[:3]] or ["Technical background with relevant domain potential"]
            critical_gaps      = [f"Missing critical skill: {s.title()}" for s in missing_skills[:3]] or ["No major missing skills identified!"]
            jd_role            = get_jd_role(jd_text_input)

            # Score theme
            if match_score >= 70:
                s_color="#22c55e"; s_glow="rgba(34,197,94,0.28)"; s_border="rgba(34,197,94,0.25)"; s_bg="rgba(34,197,94,0.07)"; s_label="🎯 Excellent Match"
            elif match_score >= 40:
                s_color="#f59e0b"; s_glow="rgba(245,158,11,0.28)"; s_border="rgba(245,158,11,0.25)"; s_bg="rgba(245,158,11,0.07)"; s_label="⚡ Moderate Match"
            else:
                s_color="#ef4444"; s_glow="rgba(239,68,68,0.28)";  s_border="rgba(239,68,68,0.25)";  s_bg="rgba(239,68,68,0.07)";  s_label="⚠️ Low Match"

            R=84; circ=2*math.pi*R; off=circ*(1-match_score/100)

            # ── 4 CORE PROJECT DASHBOARD TABS ────────────────────────────────
            tab_score, tab_skills, tab_career, tab_roadmap = st.tabs([
                "📊  Match Score",
                "🛠️  Skills Analysis",
                "💼  Career Paths",
                "📚  Roadmap",
            ])

            # ╔══════════════════════════════╗
            # ║  TAB 1 — MATCH SCORE         ║
            # ╚══════════════════════════════╝
            with tab_score:
                st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)
                col_ring, col_kpis = st.columns([4, 6], gap="large")

                with col_ring:
                    st.markdown(f"""
                    <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                         border:1px solid {s_border};border-radius:24px;
                         padding:2.5rem 1.5rem;text-align:center;
                         box-shadow:0 0 55px {s_glow},0 8px 45px rgba(0,0,0,0.55);">
                        <div style="color:#334155;font-size:0.67rem;font-weight:700;
                             letter-spacing:2.5px;margin-bottom:1.5rem;">JOB MATCH SCORE</div>
                        <div style="position:relative;display:inline-block;">
                            <svg width="200" height="200" viewBox="0 0 200 200">
                                <circle cx="100" cy="100" r="{R}" fill="none"
                                        stroke="rgba(99,102,241,0.09)" stroke-width="14"/>
                                <circle cx="100" cy="100" r="{R}" fill="none"
                                        stroke="{s_color}" stroke-width="14" stroke-linecap="round"
                                        stroke-dasharray="{circ:.3f}" stroke-dashoffset="{circ:.3f}"
                                        transform="rotate(-90 100 100)"
                                        style="--circ:{circ:.3f};--offset:{off:.3f};
                                               animation:drawRing 1.5s cubic-bezier(.4,0,.2,1) forwards;">
                                </circle>
                                <circle cx="100" cy="100" r="{R}" fill="none"
                                        stroke="{s_color}" stroke-width="7"
                                        stroke-linecap="round" opacity="0.2"
                                        stroke-dasharray="{circ:.3f}" stroke-dashoffset="{circ:.3f}"
                                        transform="rotate(-90 100 100)"
                                        style="--circ:{circ:.3f};--offset:{off:.3f};
                                               animation:drawRing 1.5s cubic-bezier(.4,0,.2,1) forwards;
                                               filter:blur(5px);">
                                </circle>
                            </svg>
                            <div style="position:absolute;top:50%;left:50%;
                                 transform:translate(-50%,-50%);text-align:center;">
                                <div style="font-size:2.75rem;font-weight:900;
                                     color:{s_color};line-height:1;">{int(match_score)}%</div>
                                <div style="font-size:0.62rem;color:#334155;
                                     font-weight:700;letter-spacing:1.5px;margin-top:0.2rem;">MATCH</div>
                            </div>
                        </div>
                        <div style="margin-top:1.25rem;display:inline-block;
                             background:{s_bg};border:1px solid {s_border};
                             border-radius:50px;padding:0.42rem 1.25rem;">
                            <span style="color:{s_color};font-weight:700;font-size:0.88rem;">{s_label}</span>
                        </div>
                    </div>
                    <style>
                    @keyframes drawRing {{
                        from {{ stroke-dashoffset: var(--circ); }}
                        to   {{ stroke-dashoffset: var(--offset); }}
                    }}
                    </style>
                    """, unsafe_allow_html=True)

                with col_kpis:
                    n_careers = len([c for c in career_suggestions if c[0] != "General Tech Role"])
                    kpis = [
                        ("🛠️","Resume Skills",  str(len(resume_skills)),  "#6366f1","rgba(99,102,241,0.10)","rgba(99,102,241,0.28)"),
                        ("✅","Skills Matched", str(len(matched_skills)), "#22c55e","rgba(34,197,94,0.08)", "rgba(34,197,94,0.28)"),
                        ("❌","Skills Missing", str(len(missing_skills)), "#ef4444","rgba(239,68,68,0.08)", "rgba(239,68,68,0.28)"),
                        ("💼","Career Fits",    str(n_careers),           "#f59e0b","rgba(245,158,11,0.08)","rgba(245,158,11,0.28)"),
                    ]
                    kpi_html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;height:100%;">'
                    for icon, label, val, color, bg, border in kpis:
                        kpi_html += f"""
                        <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                             border:1px solid {border};border-radius:20px;
                             padding:1.6rem 1.4rem;position:relative;overflow:hidden;
                             box-shadow:0 4px 22px rgba(0,0,0,0.38);">
                            <div style="position:absolute;top:0;left:0;width:3px;height:100%;
                                 background:{color};border-radius:3px 0 0 3px;"></div>
                            <div style="font-size:1.55rem;margin-bottom:0.6rem;">{icon}</div>
                            <div style="font-size:2.1rem;font-weight:900;color:{color};
                                 line-height:1;margin-bottom:0.3rem;">{val}</div>
                            <div style="font-size:0.69rem;color:#334155;font-weight:700;
                                 letter-spacing:1px;text-transform:uppercase;">{label}</div>
                        </div>"""
                    kpi_html += "</div>"
                    st.markdown(kpi_html, unsafe_allow_html=True)

                st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)
                section_label("📝 &nbsp;AI Executive Summary & Alignment")
                st.markdown(f"""
                <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                     border:1px solid rgba(99,102,241,0.14);border-left:3px solid #6366f1;
                     border-radius:0 20px 20px 0;padding:1.5rem 1.75rem;
                     box-shadow:0 4px 25px rgba(0,0,0,0.32);position:relative;margin-bottom:1.5rem;">
                    <div style="position:absolute;top:0.9rem;left:1.1rem;font-size:2.8rem;
                         color:rgba(99,102,241,0.10);font-family:Georgia,serif;line-height:1;">❝</div>
                    <p style="color:#94a3b8!important;font-size:0.91rem;line-height:1.85;
                         margin:0;padding-left:1rem;font-style:italic;">{summary}</p>
                </div>""", unsafe_allow_html=True)

                col_str, col_gap = st.columns(2, gap="medium")
                with col_str:
                    st.markdown("""
                    <div style="background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.22);
                         border-radius:18px;padding:1.25rem 1.5rem;">
                        <div style="color:#4ade80;font-weight:700;font-size:0.9rem;margin-bottom:0.75rem;">
                            💪 Candidate Key Strengths (RAG Evaluated)
                        </div>""", unsafe_allow_html=True)
                    for s in key_strengths:
                        st.markdown(f'<div style="color:#cbd5e1;font-size:0.83rem;margin-bottom:0.35rem;">▸ {s}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_gap:
                    st.markdown("""
                    <div style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.22);
                         border-radius:18px;padding:1.25rem 1.5rem;">
                        <div style="color:#f87171;font-weight:700;font-size:0.9rem;margin-bottom:0.75rem;">
                            🚨 Critical Gaps & Areas to Improve
                        </div>""", unsafe_allow_html=True)
                    for g in critical_gaps:
                        st.markdown(f'<div style="color:#cbd5e1;font-size:0.83rem;margin-bottom:0.35rem;">▸ {g}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            with tab_skills:
                st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)

                # ── 1. TOP SKILLS METRIC SUMMARY BAR ──
                cov_pct = round(len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0
                kpis_skills = [
                    ("📋", "Job Skills Required", str(len(jd_skills)), "#8b5cf6", "rgba(139,92,246,0.18)"),
                    ("📄", "Resume Skills Detected", str(len(resume_skills)), "#3b82f6", "rgba(59,130,246,0.18)"),
                    ("✅", "Matched Skills", str(len(matched_skills)), "#22c55e", "rgba(34,197,94,0.18)"),
                    ("🎯", "Skill Coverage Rate", f"{cov_pct}%", "#f59e0b", "rgba(245,158,11,0.18)"),
                ]
                kpi_cols = st.columns(4, gap="medium")
                for idx, (icon, lbl, val, color, border) in enumerate(kpis_skills):
                    with kpi_cols[idx]:
                        st.markdown(f"""
                        <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                             border:1px solid {border};border-radius:18px;padding:1.2rem 1rem;
                             text-align:center;box-shadow:0 4px 20px rgba(0,0,0,0.35);">
                            <div style="font-size:1.5rem;margin-bottom:0.3rem;">{icon}</div>
                            <div style="font-size:1.85rem;font-weight:900;color:{color};line-height:1;margin-bottom:0.25rem;">{val}</div>
                            <div style="font-size:0.67rem;color:#475569;font-weight:700;letter-spacing:1px;text-transform:uppercase;">{lbl}</div>
                        </div>""", unsafe_allow_html=True)

                st.markdown('<div style="height:1.75rem;"></div>', unsafe_allow_html=True)

                # ── 2. SKILL SPHERES COMPARISON (JOB DISTRIBUTION VS RESUME) ──
                section_label("🌐 &nbsp;Skill Spheres Breakdown (Job Distribution vs. Resume)")
                st.markdown('<div style="color:#64748b;font-size:0.85rem;margin-top:-0.4rem;margin-bottom:1.1rem;">Full distribution analysis comparing all required job description skill spheres (languages, AI/ML, frameworks, DB/Cloud, soft skills) against your resume.</div>', unsafe_allow_html=True)

                jd_cats = categorize_skills(jd_skills)
                res_cats = categorize_skills(resume_skills)
                all_categories = list(dict.fromkeys(list(SKILLS_DB.keys()) + list(jd_cats.keys()) + list(res_cats.keys())))

                cat_colors = {
                    "Programming Languages": "#6366f1",
                    "AI, ML & Data Science": "#8b5cf6",
                    "Frameworks & Developer Tools": "#06b6d4",
                    "Databases & Cloud Infrastructure": "#3b82f6",
                    "Visualization & Analytics": "#f59e0b",
                    "Soft Skills & Professional Competencies": "#ec4899",
                    "Other Technical & Domain Skills": "#10b981"
                }

                dist_html = """
                <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                     border:1px solid rgba(99,102,241,0.18);border-radius:22px;
                     padding:1.75rem 2rem;margin-bottom:2rem;box-shadow:0 4px 30px rgba(0,0,0,0.38);">"""

                for cat in all_categories:
                    c_j = jd_cats.get(cat, [])
                    c_r = res_cats.get(cat, [])
                    if not c_j and not c_r:
                        continue
                    c_m = [s for s in c_j if s.lower() in [r.lower() for r in c_r]]
                    c_missing = [s for s in c_j if s.lower() not in [r.lower() for r in c_r]]
                    c_pct = round(len(c_m) / len(c_j) * 100) if c_j else (100 if c_r else 0)
                    c_color = cat_colors.get(cat, "#6366f1")

                    dist_html += f"""
                    <div style="margin-bottom:1.5rem;padding-bottom:1.35rem;border-bottom:1px solid rgba(255,255,255,0.05);">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.55rem;">
                            <div style="display:flex;align-items:center;gap:0.65rem;">
                                <span style="color:#e2e8f0;font-weight:800;font-size:0.98rem;">{cat}</span>
                                <span style="background:{c_color}20;border:1px solid {c_color}44;color:{c_color};
                                      font-size:0.72rem;font-weight:700;padding:0.18rem 0.65rem;border-radius:20px;">
                                    {len(c_m)} / {len(c_j)} Matched
                                </span>
                            </div>
                            <span style="color:{c_color};font-weight:800;font-size:0.93rem;">{c_pct}% Sphere Match</span>
                        </div>
                        <div style="background:rgba(255,255,255,0.04);border-radius:50px;height:9px;overflow:hidden;margin-bottom:0.9rem;">
                            <div style="height:100%;width:{c_pct}%;background:linear-gradient(90deg,{c_color},{c_color}aa);
                                 border-radius:50px;box-shadow:0 0 12px {c_color}44;"></div>
                        </div>
                        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.85rem;font-size:0.8rem;">
                            <div style="background:rgba(15,23,42,0.6);border-radius:14px;padding:0.8rem 1rem;border:1px solid rgba(139,92,246,0.15);">
                                <div style="color:#a78bfa;font-weight:700;font-size:0.73rem;margin-bottom:0.4rem;text-transform:uppercase;letter-spacing:0.5px;">
                                    📋 Job Sphere Required ({len(c_j)})
                                </div>
                                {make_pills(c_j, '#c084fc', 'rgba(139,92,246,0.1)', 'rgba(139,92,246,0.25)', 'None required')}
                            </div>
                            <div style="background:rgba(15,23,42,0.6);border-radius:14px;padding:0.8rem 1rem;border:1px solid rgba(59,130,246,0.15);">
                                <div style="color:#60a5fa;font-weight:700;font-size:0.73rem;margin-bottom:0.4rem;text-transform:uppercase;letter-spacing:0.5px;">
                                    📄 Resume Possessed ({len(c_r)})
                                </div>
                                {make_pills(c_r, '#93c5fd', 'rgba(59,130,246,0.1)', 'rgba(59,130,246,0.25)', 'None found')}
                            </div>
                            <div style="background:rgba(15,23,42,0.6);border-radius:14px;padding:0.8rem 1rem;border:1px solid rgba(239,68,68,0.15);">
                                <div style="color:#f87171;font-weight:700;font-size:0.73rem;margin-bottom:0.4rem;text-transform:uppercase;letter-spacing:0.5px;">
                                    ⚠️ Sphere Gap ({len(c_missing)})
                                </div>
                                {make_pills(c_missing, '#fca5a5', 'rgba(239,68,68,0.1)', 'rgba(239,68,68,0.25)', 'None missing! 🎉')}
                            </div>
                        </div>
                    </div>"""
                dist_html += "</div>"
                st.markdown(dist_html, unsafe_allow_html=True)

                # ── 3. 3-COLUMN OVERALL SKILLS DISTRIBUTION ──
                col_jd_dist, col_res_dist, col_m_dist = st.columns(3, gap="medium")
                with col_jd_dist:
                    section_label("📋 &nbsp;All Job Distribution Skills")
                    st.markdown(f"""
                    <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                         border:1px solid rgba(139,92,246,0.2);border-radius:20px;
                         padding:1.35rem;min-height:140px;box-shadow:0 4px 20px rgba(0,0,0,0.32);">
                        {make_pills(jd_skills, '#c084fc', 'rgba(139,92,246,0.09)', 'rgba(139,92,246,0.3)', 'No skills extracted from JD.')}
                    </div>""", unsafe_allow_html=True)

                with col_res_dist:
                    section_label("📄 &nbsp;Detected Resume Skills")
                    st.markdown(f"""
                    <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                         border:1px solid rgba(59,130,246,0.2);border-radius:20px;
                         padding:1.35rem;min-height:140px;box-shadow:0 4px 20px rgba(0,0,0,0.32);">
                        {make_pills(resume_skills, '#93c5fd', 'rgba(59,130,246,0.09)', 'rgba(59,130,246,0.3)', 'No skills detected on Resume.')}
                    </div>""", unsafe_allow_html=True)

                with col_m_dist:
                    section_label("✅ &nbsp;Matched Skills Across Spheres")
                    st.markdown(f"""
                    <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                         border:1px solid rgba(34,197,94,0.2);border-radius:20px;
                         padding:1.35rem;min-height:140px;box-shadow:0 4px 20px rgba(0,0,0,0.32);">
                        {make_pills(matched_skills, '#4ade80', 'rgba(34,197,94,0.09)', 'rgba(34,197,94,0.3)', 'No overlapping skills.')}
                    </div>""", unsafe_allow_html=True)

                st.markdown('<div style="height:2rem;"></div>', unsafe_allow_html=True)

                # ── 4. WHAT SPHERE SKILLS YOUR RESUME NEEDS ──
                section_label("🚨 &nbsp;What Sphere Skills Your Resume Needs to Add")
                st.markdown('<div style="color:#64748b;font-size:0.85rem;margin-top:-0.4rem;margin-bottom:1.1rem;">Specific skill gaps identified across all skill spheres from the Job Description with recommendations on how to add them to your resume.</div>', unsafe_allow_html=True)

                if not missing_skills:
                    st.markdown("""
                    <div style="background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.25);
                         border-radius:18px;padding:1.6rem;text-align:center;">
                        <div style="font-size:2.2rem;margin-bottom:0.5rem;">🎉</div>
                        <div style="color:#22c55e;font-weight:700;font-size:1.05rem;">Your resume covers 100% of all required skills across all spheres!</div>
                        <div style="color:#94a3b8;font-size:0.85rem;margin-top:0.3rem;">No missing skills detected for this job description. Perfect match!</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    for sk in missing_skills:
                        sk_cat = get_skill_category(sk)
                        sk_motivation = SKILL_MOTIVATIONS.get(sk.lower(), f"Mastering {sk.upper()} will directly strengthen your resume alignment for {jd_role} roles.")
                        
                        st.markdown(f"""
                        <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                             border:1px solid rgba(239,68,68,0.22);border-left:4px solid #ef4444;
                             border-radius:0 18px 18px 0;padding:1.35rem 1.6rem;margin-bottom:1rem;
                             box-shadow:0 4px 22px rgba(0,0,0,0.35);">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.65rem;">
                                <div style="display:flex;align-items:center;gap:0.75rem;">
                                    <span style="color:#f87171;font-weight:800;font-size:1.05rem;text-transform:capitalize;">❌ {sk}</span>
                                    <span style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);
                                          color:#fca5a5;font-size:0.72rem;font-weight:700;padding:0.2rem 0.6rem;border-radius:20px;">
                                        {sk_cat}
                                    </span>
                                </div>
                                <span style="background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.3);
                                      color:#fbbf24;font-size:0.72rem;font-weight:700;padding:0.2rem 0.65rem;border-radius:20px;">
                                    🔥 Critical Skill Gap Needed
                                </span>
                            </div>
                            <div style="color:#cbd5e1;font-size:0.88rem;line-height:1.65;margin-bottom:0.8rem;">
                                {sk_motivation}
                            </div>
                            <div style="background:rgba(15,23,42,0.75);border:1px dashed rgba(99,102,241,0.28);
                                 border-radius:12px;padding:0.8rem 1.1rem;font-size:0.83rem;color:#a5b4fc;">
                                💡 <strong style="color:#e0e7ff;">Resume Upgrade Guidance:</strong> 
                                Add <strong style="color:#818cf8;">{sk.upper()}</strong> to your Technical Skills section under <em>"{sk_cat}"</em> and include at least 1 bullet point in your Experience or Projects section demonstrating hands-on usage of <em>{sk}</em>.
                            </div>
                        </div>""", unsafe_allow_html=True)


            # ╔══════════════════════════════╗
            # ║  TAB 3 — CAREER PATHS        ║
            # ╚══════════════════════════════╝
            with tab_career:
                st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)
                c_colors = ["#6366f1","#8b5cf6","#06b6d4","#f59e0b"]
                career_html = """
                <div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);
                     border:1px solid rgba(99,102,241,0.15);border-radius:22px;
                     padding:2rem 2.25rem;box-shadow:0 4px 30px rgba(0,0,0,0.38);">"""
                for i, (career, overlap, total) in enumerate(career_suggestions):
                    pct   = round(overlap/total*100) if total > 0 else 0
                    color = c_colors[i % len(c_colors)]
                    mb    = "2rem" if i < len(career_suggestions)-1 else "0"
                    career_html += f"""
                    <div style="margin-bottom:{mb};">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.65rem;">
                            <div>
                                <span style="color:#e2e8f0;font-weight:700;font-size:1rem;">{career}</span>
                                <span style="color:#334155;font-size:0.78rem;margin-left:0.75rem;">
                                    {overlap}/{total} core skills matched
                                </span>
                            </div>
                            <span style="color:{color};font-weight:900;font-size:1rem;">{pct}%</span>
                        </div>
                        <div style="background:rgba(255,255,255,0.04);border-radius:50px;height:9px;overflow:hidden;">
                            <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,{color},{color}bb);
                                 border-radius:50px;box-shadow:0 0 14px {color}55;"></div>
                        </div>
                    </div>"""
                career_html += "</div>"
                st.markdown(career_html, unsafe_allow_html=True)

            # ╔══════════════════════════════════════════════════════════════╗
            # ║  TAB 4 — BEAUTIFUL MOTIVATIONAL ROADMAP                     ║
            # ╚══════════════════════════════════════════════════════════════╝
            with tab_roadmap:
                st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)

                if not roadmap:
                    st.markdown("""
                    <div style="background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.25);
                         border-radius:18px;padding:2.5rem;text-align:center;">
                        <div style="font-size:2.5rem;margin-bottom:0.6rem;">🎉</div>
                        <div style="color:#22c55e;font-weight:700;font-size:1.05rem;">Full Skill Coverage!</div>
                        <div style="color:#374151;font-size:0.85rem;margin-top:0.4rem;">
                            No roadmap needed — your resume covers all required skills for this role.
                        </div>
                    </div>""", unsafe_allow_html=True)
                else:
                    # ── Roadmap header ──
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,rgba(99,102,241,0.12),rgba(139,92,246,0.12));
                         border:1px solid rgba(99,102,241,0.25);border-radius:20px;
                         padding:1.5rem 2rem;margin-bottom:2rem;">
                        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.75rem;">
                            <div style="font-size:2rem;">🗺️</div>
                            <div>
                                <div style="color:#e2e8f0;font-weight:800;font-size:1.1rem;">
                                    Your Personalized Learning Roadmap
                                </div>
                                <div style="color:#6366f1;font-size:0.8rem;font-weight:600;margin-top:0.2rem;">
                                    Tailored for <strong>{jd_role}</strong> roles · {len(roadmap)} skills to master
                                </div>
                            </div>
                        </div>
                        <div style="color:#475569;font-size:0.88rem;line-height:1.7;padding-left:3.25rem;">
                            💡 Every skill below was identified from the job description you provided.
                            Complete them in order for the fastest path to your target role.
                            <span style="color:#a5b4fc;font-weight:600;">You're closer than you think.</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    r_colors = ["#6366f1","#8b5cf6","#06b6d4","#22c55e","#f59e0b","#f43f5e","#a78bfa"]

                    for i, (skill, suggestion) in enumerate(roadmap.items()):
                        color      = r_colors[i % len(r_colors)]
                        motivation = SKILL_MOTIVATIONS.get(
                            skill.lower(),
                            f"🚀 Mastering '{skill.title()}' is exactly what {jd_role} recruiters are hiring for right now."
                        )
                        time_est   = SKILL_TIME.get(skill.lower(), "2–4 weeks")
                        is_last    = (i == len(roadmap) - 1)

                        connector = (
                            f'<div style="width:2px;flex:1;background:linear-gradient(180deg,{color}66,{color}11);'
                            f'min-height:1.5rem;margin:0.3rem 0;"></div>'
                            if not is_last else ''
                        )
                        mb_card = "1.25rem" if not is_last else "0"

                        card_html = (
                            f'<div class="roadmap-card" style="display:flex;gap:0;margin-bottom:0;animation-delay:{i*0.08}s;">'
                            # Timeline column
                            f'<div style="display:flex;flex-direction:column;align-items:center;margin-right:1.25rem;flex-shrink:0;">'
                            f'<div style="width:46px;height:46px;border-radius:50%;'
                            f'background:linear-gradient(135deg,{color}22,{color}44);'
                            f'border:2px solid {color};display:flex;align-items:center;justify-content:center;'
                            f'font-size:0.82rem;font-weight:900;color:{color};'
                            f'box-shadow:0 0 16px {color}44;flex-shrink:0;z-index:1;">{i+1:02d}</div>'
                            f'{connector}'
                            f'</div>'
                            # Card body
                            f'<div style="flex:1;background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);'
                            f'border:1px solid rgba(99,102,241,0.12);border-top:2px solid {color};'
                            f'border-radius:16px;padding:1.5rem 1.75rem;margin-bottom:{mb_card};'
                            f'box-shadow:0 4px 24px rgba(0,0,0,0.3);">'
                            # Skill name + badge
                            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;'
                            f'margin-bottom:0.85rem;flex-wrap:wrap;gap:0.5rem;">'
                            f'<div style="color:#e2e8f0;font-weight:800;font-size:1.05rem;">{skill.title()}</div>'
                            f'<div style="background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.25);'
                            f'border-radius:50px;padding:0.25rem 0.8rem;color:#a5b4fc;font-size:0.72rem;font-weight:600;white-space:nowrap;">'
                            f'⏱️ &nbsp;{time_est}</div>'
                            f'</div>'
                            # Motivational banner
                            f'<div style="background:linear-gradient(135deg,{color}18,{color}0a);'
                            f'border-left:3px solid {color};border-radius:0 10px 10px 0;'
                            f'padding:0.75rem 1rem;margin-bottom:1rem;">'
                            f'<div style="color:{color};font-size:0.88rem;font-weight:600;line-height:1.6;">{motivation}</div>'
                            f'</div>'
                            # Learning resource
                            f'<div style="display:flex;align-items:flex-start;gap:0.6rem;">'
                            f'<span style="font-size:0.9rem;margin-top:0.05rem;flex-shrink:0;">📖</span>'
                            f'<div style="color:#64748b;font-size:0.84rem;line-height:1.7;">{suggestion}</div>'
                            f'</div>'
                            f'</div>'
                            f'</div>'
                        )
                        st.markdown(card_html, unsafe_allow_html=True)



                    # ── Closing motivation banner ──
                    skills_word = "skill's" if len(roadmap) > 1 else "skill"
                    banner_html = (
                        '<div style="margin-top:2rem;background:linear-gradient(135deg,rgba(99,102,241,0.12),rgba(139,92,246,0.12));'
                        'border:1px solid rgba(99,102,241,0.25);border-radius:18px;padding:1.75rem 2rem;text-align:center;">'
                        '<div style="font-size:2rem;margin-bottom:0.75rem;">🏆</div>'
                        f'<div style="color:#e2e8f0;font-weight:800;font-size:1.1rem;margin-bottom:0.5rem;">You\'re {len(roadmap)} {skills_word} away from your dream role.</div>'
                        f'<div style="color:#6366f1;font-size:0.88rem;line-height:1.7;max-width:500px;margin:0 auto;">'
                        f'Every expert was once a beginner. Start with Step 01 today — just 30 minutes a day '
                        f'gets you hired in {jd_role} in months, not years. '
                        '<span style="color:#a5b4fc;font-weight:700;">You\'ve got this. 🚀</span>'
                        '</div></div>'
                    )
                    st.markdown(banner_html, unsafe_allow_html=True)



            # ── FOOTER ─────────────────────────────────────────────────────
            st.markdown("""
            <div style="margin-top:4.5rem;padding-top:2rem;
                 border-top:1px solid rgba(99,102,241,0.08);text-align:center;">
                <div style="color:#1e293b;font-size:0.73rem;">
                    Built with ❤️ &nbsp;·&nbsp;
                    <span style="color:#6366f1;">Python</span> &nbsp;·&nbsp;
                    <span style="color:#8b5cf6;">Streamlit</span> &nbsp;·&nbsp;
                    <span style="color:#06b6d4;">RAG Vector Index</span> &nbsp;·&nbsp;
                    <span style="color:#22c55e;">scikit-learn</span> &nbsp;·&nbsp;
                    <span style="color:#f59e0b;">pdfplumber</span>
                </div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  LANDING STATE
# ══════════════════════════════════════════════════════════════════════════════
else:
    features = [
        ("🎯", "Match Score",         "TF-IDF + Cosine Similarity scores your resume vs. any job description — 0 to 100%."),
        ("🛠️", "Skill Gap Analysis",  "See exactly which skills match and which are missing from your resume vs. the JD."),
        ("💼", "Career Recommendations","AI recommends the best-fit career paths based on your personal skill profile."),
        ("📚", "Motivational Roadmap", "JD-aware motivational lines + curated resources for every missing skill."),
        ("🤖", "RAG AI Assistant",     "Interactive LLM RAG engine to ask questions, draft cover letters & prep interviews."),
        ("📊", "Analytics Dashboard",  "Score ring, KPI cards, career progress bars — all in one beautiful dashboard."),
    ]

    col_a, col_b = st.columns(2, gap="large")
    cols = [col_a, col_b, col_a, col_b, col_a, col_b]

    for i, (icon, title, desc) in enumerate(features):
        with cols[i]:
            feat_html = (
                f'<div style="background:rgba(11,16,32,0.8);backdrop-filter:blur(24px);'
                f'border:1px solid rgba(99,102,241,0.15);border-radius:22px;'
                f'padding:1.75rem 1.85rem;margin-bottom:1.25rem;'
                f'box-shadow:0 4px 30px rgba(0,0,0,0.4);">'
                f'<div style="font-size:2rem;margin-bottom:0.85rem;">{icon}</div>'
                f'<div style="color:#e2e8f0;font-weight:700;font-size:0.98rem;margin-bottom:0.5rem;">{title}</div>'
                f'<div style="color:#4b5563;font-size:0.85rem;line-height:1.75;">{desc}</div>'
                f'</div>'
            )
            st.markdown(feat_html, unsafe_allow_html=True)

    banner_html = (
        '<div style="margin-top:0.5rem;background:rgba(99,102,241,0.06);'
        'border:1px solid rgba(99,102,241,0.22);border-radius:16px;'
        'padding:1.3rem 2rem;text-align:center;">'
        '<span style="font-size:1rem;">⬆️</span>'
        '<span style="color:#6366f1;font-weight:600;font-size:0.93rem;margin-left:0.5rem;">'
        'Fill in your resume &amp; job description above, then click '
        '<strong>Analyze My Resume</strong> to unlock all features.'
        '</span></div>'
    )
    st.markdown(banner_html, unsafe_allow_html=True)

