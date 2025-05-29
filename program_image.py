import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("แสดงภาพจาก URL (3 รูป)")

# รายการ URL ของภาพ
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://thumb.ac-illust.com/29/29ce6de610daafcb4d063cd8fdbadbce_t.jpeg",
    "https://s.isanook.com/ca/0/ud/276/1381733/9_cat-1333922_1920.jpg"
]

# สร้างคอลัมน์
cols = st.columns(3)

# ตัวแปรเก็บ index ของภาพที่เลือก
selected_index = None

# แสดงภาพและปุ่มเลือกในแต่ละคอลัมน์
for i, url in enumerate(image_urls):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        cols[i].image(img, caption=f'ภาพที่ {i+1}', use_container_width=True)
        if cols[i].button(f"เลือกภาพที่ {i+1}"):
            selected_index = i
    else:
        cols[i].error("โหลดภาพไม่สำเร็จ")

# แสดงภาพใหญ่ที่เลือกด้านล่าง
if selected_index is not None:
    st.markdown("---")
    st.subheader("ภาพที่คุณเลือก:")
    response = requests.get(image_urls[selected_index])
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=f"ภาพที่ {selected_index+1} (ขนาดใหญ่)", use_container_width=True)
    else:
        st.error("ไม่สามารถโหลดภาพที่เลือกได้")
