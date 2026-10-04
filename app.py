import streamlit as st
from rules import diagnose, SYMPTOMS

st.set_page_config(
    page_title="Computer Troubleshooting Expert System",
    page_icon="🖥️",
    layout="centered",
)

# ---------------- Custom styling ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 20% 0%, #1e1b4b 0%, #0f172a 45%, #020617 100%);
}

.hero {
    text-align: center;
    padding: 1.2rem 1rem 0.6rem 1rem;
}
.hero .icon-badge {
    font-size: 3rem;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}
.hero h1 {
    font-size: 2.3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6, #38bdf8);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 6s ease infinite;
    margin: 0.3rem 0 0.1rem 0;
}
@keyframes shine {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero p.subtitle {
    color: #94a3b8;
    font-size: 0.85rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 600;
}

.intro-box {
    background: rgba(148, 163, 184, 0.07);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin: 1rem 0 1.6rem 0;
    color: #cbd5e1;
    font-size: 0.95rem;
}

.step-label {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    color: white;
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.8rem;
    letter-spacing: 1px;
    margin-bottom: 0.7rem;
    box-shadow: 0 4px 14px rgba(56, 189, 248, 0.25);
}

/* Symptom card checkboxes */
.symptom-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.5rem 0.7rem;
    margin-bottom: 0.5rem;
    transition: all 0.2s ease;
}
.symptom-card:hover {
    border-color: rgba(56, 189, 248, 0.5);
    background: rgba(56, 189, 248, 0.06);
}
div[data-testid="stCheckbox"] label p {
    font-size: 0.95rem !important;
    font-weight: 500;
}

.chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.8rem 0 0.4rem 0;
}
.chip {
    background: linear-gradient(90deg, rgba(56,189,248,0.2), rgba(129,140,248,0.2));
    border: 1px solid rgba(129,140,248,0.4);
    color: #e0e7ff;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
}

div.stButton > button {
    background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
    background-size: 200% auto;
    color: white;
    border: none;
    padding: 0.7rem 2.2rem;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1.05rem;
    letter-spacing: 0.5px;
    box-shadow: 0 6px 20px rgba(129, 140, 248, 0.35);
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background-position: right center;
    transform: translateY(-2px);
    color: white;
    box-shadow: 0 10px 24px rgba(129, 140, 248, 0.45);
}

.confidence-badge {
    display: inline-block;
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.conf-high { background: rgba(74, 222, 128, 0.18); color: #4ade80; border: 1px solid rgba(74,222,128,0.4); }
.conf-medium { background: rgba(250, 204, 21, 0.18); color: #facc15; border: 1px solid rgba(250,204,21,0.4); }
.conf-low { background: rgba(148, 163, 184, 0.18); color: #94a3b8; border: 1px solid rgba(148,163,184,0.4); }

.result-card {
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    margin-top: 1rem;
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(6px);
}
.cause-card {
    background: linear-gradient(135deg, rgba(248, 113, 113, 0.16), rgba(248, 113, 113, 0.04));
    border-color: rgba(248, 113, 113, 0.3);
}
.fix-card {
    background: linear-gradient(135deg, rgba(74, 222, 128, 0.16), rgba(74, 222, 128, 0.04));
    border-color: rgba(74, 222, 128, 0.3);
}
.card-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    opacity: 0.8;
    margin-bottom: 0.35rem;
    font-weight: 700;
}
.card-text {
    font-size: 1.08rem;
    font-weight: 500;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

SYMPTOM_ICONS = {
    "Slow Performance": "🐢",
    "No Display / Black Screen": "⬛",
    "No Power / Won't Turn On": "🔌",
    "Overheating": "🔥",
    "No Internet / No Network": "📶",
    "Strange Noise (fan/beep)": "🔊",
    "Blue Screen (BSOD)": "🟦",
    "Virus / Malware Suspected": "🦠",
    "No Sound": "🔇",
    "Keyboard or Mouse Not Working": "⌨️",
    "Frequent Restarts / Crashes": "🔁",
    "Low Disk Space Warning": "💾",
}

CONFIDENCE = {
    "Combo Rule": ("HIGH CONFIDENCE", "conf-high"),
    "Single-Symptom Rule": ("MEDIUM CONFIDENCE", "conf-medium"),
    "Default Rule": ("NO MATCH", "conf-low"),
}

# ---------------- Header ----------------
st.markdown("""
<div class="hero">
    <div class="icon-badge">🖥️</div>
    <h1>Computer Troubleshooting Expert System</h1>
    <p class="subtitle">Rule-Based AI &nbsp;·&nbsp;  Mini Project</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro-box">
    💡 This is a <b>Rule-Based AI application</b> (not a chatbot). Tick the
    symptom(s) your computer is showing — a fixed knowledge base of IF-THEN
    rules will diagnose the likely cause and suggest a fix, with full
    reasoning shown.
</div>
""", unsafe_allow_html=True)

# ---------------- Step 1: card-grid symptom picker ----------------
st.markdown('<span class="step-label">① SELECT SYMPTOMS</span>', unsafe_allow_html=True)

selected = []
cols = st.columns(2)
for i, symptom in enumerate(SYMPTOMS):
    with cols[i % 2]:
        icon = SYMPTOM_ICONS.get(symptom, "•")
        checked = st.checkbox(f"{icon}  {symptom}", key=f"sym_{i}")
        if checked:
            selected.append(symptom)

if selected:
    chips = "".join(f'<span class="chip">{SYMPTOM_ICONS.get(s,"")} {s}</span>' for s in selected)
    st.markdown(f'<div class="chip-row">{chips}</div>', unsafe_allow_html=True)

# ---------------- Step 2 ----------------
st.markdown('<span class="step-label">② RUN INFERENCE ENGINE</span>', unsafe_allow_html=True)

if st.button("🔍  Diagnose My Computer"):
    output = diagnose(selected)

    if output["rule_level"] != "Default Rule":
        st.balloons()

    label, css_class = CONFIDENCE.get(output["rule_level"], ("", "conf-low"))
    st.markdown(f'<span class="confidence-badge {css_class}">{label}</span>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card cause-card">
        <div class="card-label">⚠️ Likely Cause</div>
        <div class="card-text">{output['cause']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card fix-card">
        <div class="card-label">✅ Suggested Fix</div>
        <div class="card-text">{output['solution']}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🧠  See how the system reasoned (rule trace)"):
        st.write(f"**Rule level used:** {output['rule_level']}")
        if "matched_on" in output:
            st.write(f"**Matched on:** {output['matched_on']}")

st.divider()
st.caption("Knowledge Base → Inference → Result  |  Built with Python + Streamlit")