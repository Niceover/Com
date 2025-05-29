import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# หัวข้อแอป
st.title("แสดงภาพจาก URL")

# URL ของภาพ
url = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg"

# ดาวน์โหลดภาพจาก URL
response = requests.get(url)

if response.status_code == 200:
    # แปลงเป็น Image object
    img = Image.open(BytesIO(response.content))
    st.image(img, caption='Bulldog Inglese', use_column_width=True)
else:
    st.error("ไม่สามารถโหลดภาพได้")

