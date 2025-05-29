import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("แสดงภาพจาก URL (3 รูป)")

# CSS ปรับขนาดปุ่มให้เท่ากัน
button_style = """
    <style>
    .stButton > button {
        width: 100%;
        height: 40px;
        font-size: 16px;
    }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# รายการ URL ของภาพ
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://thumb.ac-illust.com/29/29ce6de610daafcb4d063cd8fdbadbce_t.jpeg",
    "https://s.isanook.com/ca/0/ud/276/1381733/9_cat-1333922_1920.jpg"
]

# สร้าง layout แบบ 3 คอลัมน์
cols = st.columns(3)

# ตัวแปรเก็บ index ภาพที่เลือก
selected_index = None

# แสดงภาพและปุ่มในแต่ละคอลัมน์
for i, url in enumerate(image_urls):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        # แสดงภาพขนาดเล็ก (ความกว้าง 180px)
        cols[i].image(img, caption=f'ภาพที่ {i+1}', width=180)
        with cols[i]:
            if st.button(f"เลือกภาพที่ {i+1}", key=f"btn{i}"):
                selected_index = i
    else:
        cols[i].error("โหลดภาพไม่สำเร็จ")

# แสดงภาพใหญ่ด้านล่างหากมีการเลือก
if selected_index is not None:
    st.markdown("---")
    st.subheader("ภาพที่คุณเลือก:")
    response = requests.get(image_urls[selected_index])
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        # แสดงภาพขนาดใหญ่ (ความกว้าง 600px)
        st.image(img, caption=f"ภาพที่ {selected_index+1} (ขนาดใหญ่)", width=600)
    else:
        st.error("ไม่สามารถโหลดภาพที่เลือกได้")
