import streamlit as st
import os
import uuid
from report_generator import generate_report

st.set_page_config(
    page_title="Hotel Report Generator",
    page_icon="🏨",
    layout="centered"
)

# --- INJECT CUSTOM CSS FOR DARK GLASSMORPHISM THEME ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background Orbs (works for both light and dark) */
.bg-orbs {
    position: fixed; inset: 0; pointer-events: none; z-index: -1; overflow: hidden;
}
.orb {
    position: absolute; border-radius: 50%; filter: blur(80px); 
    opacity: 0.15; /* subtle in both modes */
    animation: drift 20s ease-in-out infinite;
}
.orb-1 {
    width: 600px; height: 600px; background: radial-gradient(circle, #1d4ed8, transparent);
    top: -200px; left: -200px; animation-delay: 0s;
}
.orb-2 {
    width: 500px; height: 500px; background: radial-gradient(circle, #0d9488, transparent);
    bottom: -150px; right: -100px; animation-delay: -7s;
}
.orb-3 {
    width: 350px; height: 350px; background: radial-gradient(circle, #6366f1, transparent);
    top: 40%; left: 50%; animation-delay: -14s;
}
@keyframes drift {
    0%, 100% { transform: translate(0, 0) scale(1); }
    33% { transform: translate(40px, -30px) scale(1.05); }
    66% { transform: translate(-20px, 30px) scale(0.97); }
}

/* Header Text */
h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    text-align: center;
    color: var(--text-color) !important;
}

h1 span {
    background: linear-gradient(135deg, #14b8a6, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stMarkdown p {
    text-align: center;
    color: color-mix(in srgb, var(--text-color) 70%, transparent);
}

/* Glassmorphism Form Container */
div[data-testid="stForm"] {
    background: color-mix(in srgb, var(--secondary-background-color) 70%, transparent) !important;
    border-radius: 20px !important;
    padding: 30px !important;
    border: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent) !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 10px 40px color-mix(in srgb, var(--text-color) 5%, transparent) !important;
}

/* Inputs & Labels */
div[data-testid="stTextInput"] label p, div[data-testid="stFileUploader"] label p { 
    color: var(--text-color) !important; 
    font-weight: 600 !important; 
    text-align: left; 
}

/* Fix Input Box Visibility */
div[data-baseweb="input"] {
    background-color: var(--background-color) !important;
    border: 1px solid color-mix(in srgb, var(--text-color) 20%, transparent) !important;
    border-radius: 12px !important;
}
div[data-baseweb="input"] > div {
    background-color: transparent !important;
}
div[data-baseweb="input"] input {
    color: var(--text-color) !important;
    -webkit-text-fill-color: var(--text-color) !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #2dd4bf !important;
    box-shadow: 0 0 0 3px color-mix(in srgb, #2dd4bf 20%, transparent) !important;
}

/* File Uploader Box */
section[data-testid="stFileUploadDropzone"] {
    background-color: color-mix(in srgb, var(--background-color) 50%, transparent) !important;
    border: 1.5px dashed color-mix(in srgb, var(--text-color) 20%, transparent) !important;
    border-radius: 14px !important;
    color: var(--text-color) !important;
}
section[data-testid="stFileUploadDropzone"]:hover {
    border-color: #2dd4bf !important;
    background-color: color-mix(in srgb, #2dd4bf 10%, transparent) !important;
}

/* Form Submit Button */
div[data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    background: linear-gradient(135deg, #0d9488, #2563eb) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 10px !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 15px color-mix(in srgb, #0d9488 40%, transparent) !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px color-mix(in srgb, #0d9488 60%, transparent) !important;
}
div[data-testid="stFormSubmitButton"] button p {
    color: #ffffff !important;
}

/* Download Button */
div[data-testid="stDownloadButton"] button {
    width: 100% !important;
    background: color-mix(in srgb, #10b981 10%, transparent) !important;
    color: #10b981 !important;
    border: 1px solid color-mix(in srgb, #10b981 30%, transparent) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

/* Success / Error messages */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    background-color: color-mix(in srgb, var(--text-color) 5%, transparent) !important;
}

/* Show default streamlit elements so user can change theme */
#MainMenu {visibility: visible;}
footer {visibility: hidden;}
header {visibility: visible;}
</style>

<div class="bg-orbs">
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
  <div class="orb orb-3"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1>Hotel Report <span>Generator</span></h1>", unsafe_allow_html=True)
st.markdown("อัปโหลดไฟล์ Raw Data (Excel) จากระบบเพื่อสร้าง Report สรุปข้อมูลอัตโนมัติ")

with st.form("report_form"):
    hotel_name = st.text_input("ชื่อโรงแรม", placeholder="เช่น My Hotel Resort & Spa")
    uploaded_file = st.file_uploader("เลือกไฟล์ Raw Data (.xlsx)", type=['xlsx'])
    
    submitted = st.form_submit_button("✨ สร้าง Report")

if submitted:
    if not hotel_name.strip():
        st.error("⚠️ กรุณากรอกชื่อโรงแรม")
    elif not uploaded_file:
        st.error("⚠️ กรุณาเลือกไฟล์ Raw Data")
    else:
        with st.spinner('กำลังประมวลผลข้อมูล...'):
            try:
                os.makedirs('/tmp/hotel_uploads', exist_ok=True)
                os.makedirs('/tmp/hotel_outputs', exist_ok=True)
                
                uid = str(uuid.uuid4())
                input_path = f"/tmp/hotel_uploads/{uid}_input.xlsx"
                output_path = f"/tmp/hotel_outputs/{uid}_report.xlsx"
                
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                generate_report(input_path, hotel_name, output_path)
                
                st.success("✅ สร้าง Report สำเร็จแล้ว!")
                
                safe_name = hotel_name.replace(' ', '_')
                with open(output_path, "rb") as file:
                    btn = st.download_button(
                        label="📥 ดาวน์โหลดไฟล์ Report",
                        data=file,
                        file_name=f'report_{safe_name}.xlsx',
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผล: {str(e)}")
            finally:
                if os.path.exists(input_path):
                    try:
                        os.remove(input_path)
                    except:
                        pass
