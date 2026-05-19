import streamlit as st
import os
import uuid
import base64
from report_generator import generate_report, TEMPLATES, DEFAULT_TEMPLATE

st.set_page_config(
    page_title="Hotel Report Generator 🐱",
    page_icon="🐱",
    layout="centered"
)

# ─────────────────────────────────────────────
# Load cat mascot as base64 for embedding
# ─────────────────────────────────────────────
CAT_IMG_B64 = ""
_cat_path = os.path.join(os.path.dirname(__file__), "static", "cat_mascot.png")
if os.path.exists(_cat_path):
    with open(_cat_path, "rb") as _f:
        CAT_IMG_B64 = base64.b64encode(_f.read()).decode()

# ─────────────────────────────────────────────
# 🐱 CUTE CAT LIGHT THEME — Full CSS Injection
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&family=Quicksand:wght@400;500;600;700&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* ── Warm Light Background with paw print pattern ── */
[data-testid="stAppViewContainer"] {
    background: #f4f5f7 !important;
    min-height: 100vh;
}
[data-testid="stAppViewContainer"]::before {
    content: '🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾  🐾';
    position: fixed;
    inset: 0;
    font-size: 18px;
    letter-spacing: 30px;
    line-height: 55px;
    word-spacing: 20px;
    opacity: 0.04;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
    color: #5b5e67;
}

/* ── Soft floating gradient blobs ── */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 50% 40% at 15% 20%, rgba(51,74,102,0.08) 0%, transparent 70%),
        radial-gradient(ellipse 45% 35% at 85% 75%, rgba(246,204,93,0.06) 0%, transparent 70%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(164,167,176,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: blobFloat 20s ease-in-out infinite alternate;
}
@keyframes blobFloat {
    0%   { opacity: 1; }
    100% { opacity: 0.7; }
}

[data-testid="stMain"] {
    position: relative;
    z-index: 1;
}

/* ── Remove default Streamlit top padding ── */
.block-container,
[data-testid="stMainBlockContainer"] {
    padding-top: 0rem !important;
    padding-bottom: 4rem !important;
    max-width: 680px !important;
}

/* ── Hero Section ── */
.hero-wrapper {
    text-align: center;
    padding: 2rem 0 1.5rem;
    position: relative;
}
.cat-mascot {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid #e2e4e9;
    box-shadow:
        0 0 0 6px rgba(51,74,102,0.08),
        0 12px 40px rgba(51,74,102,0.12);
    animation: catBounce 3s ease-in-out infinite;
    margin-bottom: 1rem;
}
@keyframes catBounce {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    25% { transform: translateY(-6px) rotate(-2deg); }
    75% { transform: translateY(-3px) rotate(2deg); }
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #e2e4e9, #f4f5f7);
    border: 1px solid rgba(51,74,102,0.15);
    color: #334a66;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 0.9rem;
}
.hero-title {
    font-family: 'Quicksand', sans-serif !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    color: #2d313a !important;
    margin: 0 0 0.5rem !important;
    letter-spacing: -0.02em;
}
.hero-title .grad {
    background: linear-gradient(135deg, #334a66, #5c7490, #7a7d87);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.95rem !important;
    color: #5b5e67 !important;
    max-width: 440px;
    margin: 0 auto 0.5rem !important;
    line-height: 1.7;
}
.hero-cats {
    font-size: 1.4rem;
    letter-spacing: 0.2em;
    margin-top: 0.3rem;
    opacity: 0.6;
}

/* ── Divider ── */
.section-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(51,74,102,0.2), rgba(246,204,93,0.3), transparent);
    margin: 0.3rem 0 1.8rem;
    position: relative;
}
.section-divider::after {
    content: '📋';
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 1.1rem;
    background: #f4f5f7;
    padding: 0 0.6rem;
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
    width: 24px; height: 24px;
    border-radius: 50%;
    background: linear-gradient(135deg, #334a66, #5c7490);
    font-size: 0.72rem;
    font-weight: 800;
    color: #fff;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(51,74,102,0.25);
}
.step-text {
    font-size: 0.82rem;
    font-weight: 700;
    color: #5b5e67;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.step-emoji {
    font-size: 0.95rem;
}

/* ── Form Card (Glassmorphism light) ── */
div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.75) !important;
    border: 1.5px solid rgba(51,74,102,0.15) !important;
    border-radius: 24px !important;
    padding: 2rem 2rem 1.5rem !important;
    backdrop-filter: blur(20px) !important;
    box-shadow:
        0 4px 6px rgba(51,74,102,0.04),
        0 16px 48px rgba(51,74,102,0.06),
        inset 0 1px 0 rgba(255,255,255,0.8) !important;
    margin-bottom: 1.25rem !important;
}

div[data-testid="stTextInput"] label p,
div[data-testid="stFileUploader"] label p,
div[data-testid="stSelectbox"] label p,
div[data-testid="stRadio"] label p {
    color: #334a66 !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    text-align: left !important;
    margin-bottom: 0.15rem !important;
}

/* ── Text Input ── */
div[data-baseweb="input"] {
    background: rgba(255,255,255,0.9) !important;
    border: 1.5px solid rgba(51,74,102,0.15) !important;
    border-radius: 14px !important;
    transition: all 0.25s ease !important;
}
div[data-baseweb="input"] > div {
    background: transparent !important;
}
div[data-baseweb="input"] input {
    color: #2d313a !important;
    -webkit-text-fill-color: #2d313a !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}
div[data-baseweb="input"] input::placeholder {
    color: #a4a7b0 !important;
    -webkit-text-fill-color: #a4a7b0 !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #334a66 !important;
    box-shadow: 0 0 0 3px rgba(51,74,102,0.15), 0 4px 12px rgba(51,74,102,0.08) !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] > section,
[data-testid="stFileUploadDropzone"],
[data-testid="stFileUploaderDropzone"] {
    background: rgba(226,228,233,0.3) !important;
    border: 2px dashed rgba(51,74,102,0.3) !important;
    border-radius: 16px !important;
    transition: all 0.25s ease !important;
}
[data-testid="stFileUploadDropzone"]:hover,
[data-testid="stFileUploaderDropzone"]:hover,
[data-testid="stFileUploader"]:hover > section {
    border-color: #334a66 !important;
    background: rgba(226,228,233,0.5) !important;
    box-shadow: 0 0 20px rgba(51,74,102,0.08) !important;
}
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span {
    color: #5b5e67 !important;
}
[data-testid="stFileUploader"] small,
[data-testid="stFileUploaderDropzone"] small {
    color: #7a7d87 !important;
}
[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button {
    color: #334a66 !important;
    background: rgba(51,74,102,0.08) !important;
    border: 1px solid rgba(51,74,102,0.2) !important;
    border-radius: 10px !important;
}

/* ── Uploaded File Item ── */
div[data-testid="stFileUploader"] > div:last-child,
div[data-testid="stFileUploaderFileData"],
[data-testid="stUploadedFile"] {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(51,74,102,0.2) !important;
    border-radius: 12px !important;
    padding: 0.5rem !important;
    margin-top: 0.5rem !important;
}
div[data-testid="stFileUploader"] > div:last-child div,
div[data-testid="stFileUploader"] > div:last-child span,
div[data-testid="stFileUploader"] > div:last-child p,
[data-testid="stUploadedFile"] div, 
[data-testid="stUploadedFile"] span, 
[data-testid="stUploadedFile"] p {
    color: #2d313a !important;
    text-shadow: none !important;
}
div[data-testid="stFileUploader"] > div:last-child svg,
[data-testid="stUploadedFile"] svg {
    stroke: #334a66 !important;
}

/* ── Template Radio Cards ── */
div[data-testid="stRadio"] > div {
    gap: 0.6rem !important;
}
div[data-testid="stRadio"] > div > label {
    background: rgba(255,255,255,0.8) !important;
    border: 1.5px solid rgba(51,74,102,0.15) !important;
    border-radius: 16px !important;
    padding: 0.85rem 1rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
}
div[data-testid="stRadio"] > div > label:hover {
    border-color: rgba(51,74,102,0.4) !important;
    background: rgba(226,228,233,0.3) !important;
    transform: translateY(-1px);
}
div[data-testid="stRadio"] > div > label[data-selected="true"],
div[data-testid="stRadio"] > div > label:has(input:checked) {
    border-color: #334a66 !important;
    background: rgba(51,74,102,0.05) !important;
    box-shadow: 0 0 0 2px rgba(51,74,102,0.15), 0 4px 12px rgba(51,74,102,0.08) !important;
}
div[data-testid="stRadio"] > div > label p {
    color: #334a66 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.9) !important;
    border: 1.5px solid rgba(51,74,102,0.15) !important;
    border-radius: 14px !important;
    color: #2d313a !important;
}
div[data-baseweb="select"] span {
    color: #2d313a !important;
}
div[data-baseweb="select"]:focus-within > div {
    border-color: #334a66 !important;
    box-shadow: 0 0 0 3px rgba(51,74,102,0.15) !important;
}

/* ── Submit Button ── */
div[data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    background: linear-gradient(135deg, #334a66 0%, #455a73 50%, #5c7490 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 16px !important;
    font-family: 'Quicksand', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    padding: 0.85rem 1rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s ease !important;
    box-shadow:
        0 4px 20px rgba(51,74,102,0.35),
        0 1px 0 rgba(255,255,255,0.2) inset !important;
    margin-top: 0.5rem !important;
    position: relative;
    overflow: hidden;
}
div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow:
        0 8px 30px rgba(51,74,102,0.45),
        0 1px 0 rgba(255,255,255,0.2) inset !important;
}
div[data-testid="stFormSubmitButton"] button:active {
    transform: translateY(0px) scale(0.99) !important;
}
div[data-testid="stFormSubmitButton"] button p {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* ── Download Button ── */
div[data-testid="stDownloadButton"] {
    margin-top: 0.5rem !important;
}
div[data-testid="stDownloadButton"] button {
    width: 100% !important;
    background: rgba(16, 185, 129, 0.08) !important;
    color: #059669 !important;
    border: 1.5px solid rgba(16,185,129,0.3) !important;
    border-radius: 16px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(16,185,129,0.08) !important;
}
div[data-testid="stDownloadButton"] button:hover {
    background: rgba(16, 185, 129, 0.15) !important;
    box-shadow: 0 6px 20px rgba(16,185,129,0.15) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stDownloadButton"] button p {
    color: #059669 !important;
    font-weight: 700 !important;
}

/* ── Alert Messages ── */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border-left-width: 4px !important;
}

/* ── Caption / small text ── */
div[data-testid="stCaptionContainer"] p {
    color: #7a7d87 !important;
    font-size: 0.8rem !important;
    text-align: left !important;
}

/* ── Spinner ── */
div[data-testid="stSpinner"] p {
    color: #5b5e67 !important;
}

/* ── Success result card ── */
.result-card {
    background: linear-gradient(135deg, rgba(16,185,129,0.06), rgba(52,211,153,0.08));
    border: 1.5px solid rgba(16,185,129,0.2);
    border-radius: 20px;
    padding: 1.5rem 1.5rem;
    text-align: center;
    margin-bottom: 0.75rem;
}
.result-icon { font-size: 2.5rem; margin-bottom: 0.4rem; }
.result-title {
    font-family: 'Quicksand', sans-serif;
    font-size: 1.15rem;
    font-weight: 800;
    color: #059669;
    margin-bottom: 0.2rem;
}
.result-sub { font-size: 0.85rem; color: #5b5e67; }
.result-cat { font-size: 1.2rem; margin-top: 0.3rem; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: #a4a7b0;
    font-size: 0.8rem;
}
.footer span { color: #5b5e67; font-weight: 600; }
.footer-cats {
    font-size: 1.3rem;
    letter-spacing: 0.3em;
    margin-bottom: 0.4rem;
}

/* ── Floating Cat Decorations ── */
.floating-cat {
    position: fixed;
    font-size: 1.8rem;
    opacity: 0.12;
    pointer-events: none;
    z-index: 0;
    animation: floatCat 8s ease-in-out infinite;
}
.cat-1 { top: 10%; left: 5%; animation-delay: 0s; }
.cat-2 { top: 30%; right: 3%; animation-delay: 2s; }
.cat-3 { bottom: 20%; left: 8%; animation-delay: 4s; }
.cat-4 { bottom: 10%; right: 6%; animation-delay: 6s; }
@keyframes floatCat {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    25% { transform: translateY(-15px) rotate(5deg); }
    50% { transform: translateY(-8px) rotate(-3deg); }
    75% { transform: translateY(-12px) rotate(3deg); }
}

/* ── Hide Streamlit branding ── */
#MainMenu { display: none !important; }
footer { display: none !important; }
header { display: none !important; }
</style>

<!-- Floating cat decorations -->
<div class="floating-cat cat-1">💼</div>
<div class="floating-cat cat-2">📋</div>
<div class="floating-cat cat-3">💻</div>
<div class="floating-cat cat-4">✨</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────
if CAT_IMG_B64:
    cat_img_html = f'<img src="data:image/png;base64,{CAT_IMG_B64}" class="cat-mascot" alt="Cat Mascot">'
else:
    cat_img_html = '<div style="font-size:5rem; margin-bottom:1rem;">🐱</div>'

st.markdown(f"""
<div class="hero-wrapper">
    {cat_img_html}
    <br>
    <div class="hero-badge">📋 Automated Excel Report</div>
    <div class="hero-title">Hotel Report <span class="grad">Generator</span></div>
    <p class="hero-sub">อัปโหลดไฟล์ Raw Data จากระบบ แล้วรับไฟล์รายงาน Excel สวยงาม พร้อมกราฟและสถิติ ภายในไม่กี่วินาที 💼✨</p>
    <div class="hero-cats">💼 🐱 📋</div>
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

with st.form("report_form"):

    # Step 1 — Hotel Name
    st.markdown("""
    <div class="step-label">
        <div class="step-num">1</div>
        <div class="step-text">ชื่อโรงแรม</div>
        <span class="step-emoji">🏨</span>
    </div>""", unsafe_allow_html=True)
    hotel_name = st.text_input(
        label="hotel_name_input",
        label_visibility="collapsed",
        placeholder="เช่น My Resort Hotel & Spa 🏨"
    )

    st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)

    # Step 2 — File Upload
    st.markdown("""
    <div class="step-label">
        <div class="step-num">2</div>
        <div class="step-text">ไฟล์ Raw Data (.xlsx)</div>
        <span class="step-emoji">📁</span>
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
        <span class="step-emoji">📋</span>
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
    submitted = st.form_submit_button("📋  สร้าง Report")

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
        with st.spinner("💻 ระบบกำลังประมวลผลข้อมูล..."):
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
                    <div class="result-cat">🐱✨</div>
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
    <div class="footer-cats">💻 💼 📋</div>
    <span>Hotel Report Generator</span> &nbsp;·&nbsp; Professional Edition
    <br><small style="opacity:0.6">Powered by Python & openpyxl</small>
</div>
""", unsafe_allow_html=True)
