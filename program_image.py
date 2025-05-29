import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("แสดงภาพจาก")

# รายการ URL ของภาพ (แก้ไขใหม่)
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://thumb.ac-illust.com/29/29ce6de610daafcb4d063cd8fdbadbce_t.jpeg",
    "https://s.isanook.com/ca/0/ud/276/1381733/9_cat-1333922_1920.jpg"
]

# สร้าง layout แบบ 3 คอลัมน์
cols = st.columns(3)

# แสดงภาพในแต่ละคอลัมน์
for i, url in enumerate(image_urls):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        cols[i].image(img, caption=f'ภาพที่ {i+1}', use_container_width=True)  # ✅ ใช้ use_container_width
    else:
        cols[i].error("โหลดภาพไม่สำเร็จ")
