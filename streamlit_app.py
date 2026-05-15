import streamlit as st
import os
import uuid
from report_generator import generate_report, TEMPLATES, DEFAULT_TEMPLATE

st.set_page_config(
    page_title="Hotel Report Generator",
    page_icon="🏨",
    layout="centered"
)

# ─────────────────────────────────────────────
# PREMIUM DARK DESIGN — Full CSS Injection
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Animated Mesh Gradient Background ── */
[data-testid="stAppViewContainer"] {
    background: #080c14 !important;
    min-height: 100vh;
}
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(13,148,136,0.16) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(59,130,246,0.10) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: meshShift 18s ease-in-out infinite alternate;
}
@keyframes meshShift {
    0%   { opacity: 1; filter: hue-rotate(0deg); }
    100% { opacity: 0.85; filter: hue-rotate(20deg); }
}

/* ── Stars / Particle dots ── */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(circle, rgba(255,255,255,0.25) 1px, transparent 1px),
        radial-gradient(circle, rgba(255,255,255,0.15) 1px, transparent 1px);
    background-size: 120px 120px, 60px 60px;
    background-position: 0 0, 30px 30px;
    pointer-events: none;
    z-index: 0;
    opacity: 0.3;
}

[data-testid="stMain"] {
    position: relative;
    z-index: 1;
}

/* ── Remove default Streamlit top padding ── */
[data-testid="stMainBlockContainer"] {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 680px !important;
}

/* ── Hero Section ── */
.hero-wrapper {
    text-align: center;
    padding: 2.5rem 0 2rem;
    position: relative;
}
.hero-icon-ring {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 88px; height: 88px;
    border-radius: 26px;
    background: linear-gradient(135deg, #1e3a5f 0%, #0f2544 100%);
    box-shadow:
        0 0 0 1px rgba(99,102,241,0.4),
        0 0 40px rgba(99,102,241,0.25),
        0 20px 60px rgba(0,0,0,0.5);
    font-size: 42px;
    margin-bottom: 1.25rem;
    animation: float 4s ease-in-out infinite;
    position: relative;
}
.hero-icon-ring::after {
    content: '';
    position: absolute;
    inset: -2px;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(99,102,241,0.6), rgba(13,148,136,0.6));
    z-index: -1;
    filter: blur(8px);
    animation: glowPulse 3s ease-in-out infinite alternate;
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}
@keyframes glowPulse {
    0%   { opacity: 0.5; }
    100% { opacity: 1; }
}

.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    color: #a5b4fc;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.85rem;
    border-radius: 100px;
    margin-bottom: 0.9rem;
}
.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    color: #f1f5f9 !important;
    margin: 0 0 0.6rem !important;
    letter-spacing: -0.03em;
}
.hero-title .grad {
    background: linear-gradient(135deg, #38bdf8, #818cf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.97rem !important;
    color: #94a3b8 !important;
    max-width: 420px;
    margin: 0 auto 0.5rem !important;
    line-height: 1.6;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.3), rgba(13,148,136,0.3), transparent);
    margin: 0.5rem 0 1.8rem;
}

/* ── Step Badges ── */
.step-label {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.45rem;
}
.step-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px; height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #0d9488);
    font-size: 0.7rem;
    font-weight: 700;
    color: #fff;
    flex-shrink: 0;
}
.step-text {
    font-size: 0.82rem;
    font-weight: 600;
    color: #94a3b8;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Card Container ── */
.card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 20px;
    padding: 2rem 2rem 1.5rem;
    backdrop-filter: blur(24px);
    box-shadow:
        0 4px 6px rgba(0,0,0,0.2),
        0 20px 60px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.05);
    margin-bottom: 1.25rem;
}

/* ── Form inputs override ── */
div[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
}

div[data-testid="stTextInput"] label p,
div[data-testid="stFileUploader"] label p,
div[data-testid="stSelectbox"] label p,
div[data-testid="stRadio"] label p {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    text-align: left !important;
    margin-bottom: 0.15rem !important;
}

div[data-baseweb="input"] {
    background: rgba(30, 41, 59, 0.8) !important;
    border: 1px solid rgba(148, 163, 184, 0.25) !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="input"] > div {
    background: transparent !important;
}
div[data-baseweb="input"] input {
    color: #f1f5f9 !important;
    -webkit-text-fill-color: #f1f5f9 !important;
    font-size: 0.95rem !important;
}
div[data-baseweb="input"] input::placeholder {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}

/* ── File Uploader ── */
section[data-testid="stFileUploadDropzone"] {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1.5px dashed rgba(99,102,241,0.4) !important;
    border-radius: 14px !important;
    transition: all 0.25s ease !important;
}
section[data-testid="stFileUploadDropzone"]:hover {
    border-color: #6366f1 !important;
    background: rgba(99,102,241,0.08) !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.15) !important;
}
section[data-testid="stFileUploadDropzone"] p,
section[data-testid="stFileUploadDropzone"] span {
    color: #94a3b8 !important;
}
section[data-testid="stFileUploadDropzone"] small {
    color: #64748b !important;
}

/* ── Template Radio Cards ── */
div[data-testid="stRadio"] > div {
    gap: 0.6rem !important;
}
div[data-testid="stRadio"] > div > label {
    background: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid rgba(148,163,184,0.15) !important;
    border-radius: 14px !important;
    padding: 0.85rem 1rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: rgba(99,102,241,0.5) !important;
    background: rgba(99,102,241,0.08) !important;
}
div[data-testid="stRadio"] > div > label[data-selected="true"],
div[data-testid="stRadio"] > div > label:has(input:checked) {
    border-color: rgba(99,102,241,0.7) !important;
    background: rgba(99,102,241,0.12) !important;
    box-shadow: 0 0 0 1px rgba(99,102,241,0.35) !important;
}
div[data-testid="stRadio"] > div > label p {
    color: #e2e8f0 !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: rgba(30, 41, 59, 0.8) !important;
    border: 1px solid rgba(148,163,184,0.25) !important;
    border-radius: 12px !important;
    color: #f1f5f9 !important;
}
div[data-baseweb="select"] span {
    color: #f1f5f9 !important;
}
div[data-baseweb="select"]:focus-within > div {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}

/* ── Submit Button ── */
div[data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    background: linear-gradient(135deg, #6366f1 0%, #0d9488 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 0.8rem 1rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4), 0 1px 0 rgba(255,255,255,0.1) inset !important;
    margin-top: 0.5rem !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.55), 0 1px 0 rgba(255,255,255,0.1) inset !important;
}
div[data-testid="stFormSubmitButton"] button:active {
    transform: translateY(0px) !important;
}
div[data-testid="stFormSubmitButton"] button p {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ── Download Button ── */
div[data-testid="stDownloadButton"] {
    margin-top: 0.5rem !important;
}
div[data-testid="stDownloadButton"] button {
    width: 100% !important;
    background: rgba(16, 185, 129, 0.12) !important;
    color: #34d399 !important;
    border: 1px solid rgba(52, 211, 153, 0.35) !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(16,185,129,0.1) !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background: rgba(16, 185, 129, 0.2) !important;
    box-shadow: 0 6px 20px rgba(16,185,129,0.2) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stDownloadButton"] button p {
    color: #34d399 !important;
    font-weight: 600 !important;
}

/* ── Alert Messages ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 3px !important;
}

/* ── Caption / small text ── */
div[data-testid="stCaptionContainer"] p {
    color: #64748b !important;
    font-size: 0.8rem !important;
    text-align: left !important;
}

/* ── Spinner ── */
div[data-testid="stSpinner"] p {
    color: #94a3b8 !important;
}

/* ── Success result card ── */
.result-card {
    background: rgba(16,185,129,0.07);
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    margin-bottom: 0.75rem;
}
.result-icon { font-size: 2.2rem; margin-bottom: 0.4rem; }
.result-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #34d399;
    margin-bottom: 0.2rem;
}
.result-sub { font-size: 0.83rem; color: #64748b; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #334155;
    font-size: 0.78rem;
}
.footer span { color: #475569; }

/* ── Hide Streamlit branding ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-icon-ring">🏨</div><br>
    <div class="hero-badge">✦ Automated Excel Report</div>
    <div class="hero-title">Hotel Report <span class="grad">Generator</span></div>
    <p class="hero-sub">อัปโหลดไฟล์ Raw Data จากระบบ แล้วรับไฟล์รายงาน Excel สวยงาม พร้อมกราฟและสถิติ ภายในไม่กี่วินาที</p>
</div>
<div class="section-divider"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BUILD TEMPLATE OPTIONS
# ─────────────────────────────────────────────
_template_options = list(TEMPLATES.keys())
_template_labels  = {k: v['name'] for k, v in TEMPLATES.items()}
_template_descs   = {k: v['description'] for k, v in TEMPLATES.items()}

# ─────────────────────────────────────────────
# MAIN FORM CARD
# ─────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

with st.form("report_form"):

    # Step 1 — Hotel Name
    st.markdown("""
    <div class="step-label">
        <div class="step-num">1</div>
        <div class="step-text">ชื่อโรงแรม</div>
    </div>""", unsafe_allow_html=True)
    hotel_name = st.text_input(
        label="hotel_name_input",
        label_visibility="collapsed",
        placeholder="เช่น My Resort Hotel & Spa"
    )

    st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)

    # Step 2 — File Upload
    st.markdown("""
    <div class="step-label">
        <div class="step-num">2</div>
        <div class="step-text">ไฟล์ Raw Data (.xlsx)</div>
    </div>""", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="file_uploader",
        label_visibility="collapsed",
        type=['xlsx']
    )

    st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)

    # Step 3 — Template Selection
    st.markdown("""
    <div class="step-label">
        <div class="step-num">3</div>
        <div class="step-text">รูปแบบ Report</div>
    </div>""", unsafe_allow_html=True)

    selected_template = st.radio(
        label="template_select",
        label_visibility="collapsed",
        options=_template_options,
        format_func=lambda k: _template_labels[k],
        index=_template_options.index(DEFAULT_TEMPLATE) if DEFAULT_TEMPLATE in _template_options else 0,
        horizontal=False
    )
    st.caption(f"ℹ️ {_template_descs.get(selected_template, '')}")

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # Submit
    submitted = st.form_submit_button("✨  สร้าง Report")

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PROCESS & RESULT
# ─────────────────────────────────────────────
if submitted:
    if not hotel_name.strip():
        st.error("⚠️ กรุณากรอกชื่อโรงแรม")
    elif not uploaded_file:
        st.error("⚠️ กรุณาเลือกไฟล์ Raw Data")
    else:
        with st.spinner("⚙️ กำลังประมวลผลข้อมูล..."):
            try:
                tmp_up  = os.path.join(os.getcwd(), "tmp_uploads")
                tmp_out = os.path.join(os.getcwd(), "tmp_outputs")
                os.makedirs(tmp_up,  exist_ok=True)
                os.makedirs(tmp_out, exist_ok=True)

                uid         = str(uuid.uuid4())
                input_path  = os.path.join(tmp_up,  f"{uid}_input.xlsx")
                output_path = os.path.join(tmp_out, f"{uid}_report.xlsx")

                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                generate_report(input_path, hotel_name, output_path, template_name=selected_template)

                safe_name    = hotel_name.replace(' ', '_')
                tpl_label    = _template_labels.get(selected_template, selected_template)

                # ── Result card
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-icon">✅</div>
                    <div class="result-title">สร้าง Report สำเร็จแล้ว!</div>
                    <div class="result-sub">{hotel_name} &nbsp;·&nbsp; {tpl_label}</div>
                </div>
                """, unsafe_allow_html=True)

                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥  ดาวน์โหลดไฟล์ Report",
                        data=file,
                        file_name=f"report_{safe_name}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            finally:
                if os.path.exists(input_path):
                    try:
                        os.remove(input_path)
                    except:
                        pass

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span>Hotel Report Generator</span> &nbsp;·&nbsp; Powered by Python & openpyxl
</div>
""", unsafe_allow_html=True)
