import streamlit as st
import os
import uuid
from report_generator import generate_report

st.set_page_config(
    page_title="Hotel Report Generator",
    page_icon="🏨",
    layout="centered"
)

st.title("🏨 Hotel Report Generator")
st.markdown("อัปโหลดไฟล์ Raw Data (Excel) จากระบบเพื่อสร้าง Report สรุปข้อมูลอัตโนมัติ")

with st.form("report_form"):
    hotel_name = st.text_input("ชื่อโรงแรม", placeholder="เช่น My Hotel Resort & Spa")
    uploaded_file = st.file_uploader("เลือกไฟล์ Raw Data (.xlsx)", type=['xlsx'])
    
    submitted = st.form_submit_button("สร้าง Report", type="primary")

if submitted:
    if not hotel_name.strip():
        st.error("⚠️ กรุณากรอกชื่อโรงแรม")
    elif not uploaded_file:
        st.error("⚠️ กรุณาเลือกไฟล์ Raw Data")
    else:
        with st.spinner('กำลังประมวลผลข้อมูล...'):
            try:
                # สร้างโฟลเดอร์ชั่วคราว
                os.makedirs('/tmp/hotel_uploads', exist_ok=True)
                os.makedirs('/tmp/hotel_outputs', exist_ok=True)
                
                uid = str(uuid.uuid4())
                input_path = f"/tmp/hotel_uploads/{uid}_input.xlsx"
                output_path = f"/tmp/hotel_outputs/{uid}_report.xlsx"
                
                # บันทึกไฟล์ที่อัปโหลด
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # เรียกใช้ฟังก์ชันประมวลผล
                generate_report(input_path, hotel_name, output_path)
                
                st.success("✅ สร้าง Report สำเร็จแล้ว!")
                
                # ปุ่มดาวน์โหลด
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
                # ทำความสะอาดไฟล์
                if os.path.exists(input_path):
                    try:
                        os.remove(input_path)
                    except:
                        pass
