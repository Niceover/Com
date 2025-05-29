import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("แสดงภาพจาก URL (3 รูป) พร้อมปรับขนาดแกน X และ Y")

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

image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://thumb.ac-illust.com/29/29ce6de610daafcb4d063cd8fdbadbce_t.jpeg",
    "https://s.isanook.com/ca/0/ud/276/1381733/9_cat-1333922_1920.jpg"
]

cols = st.columns(3)

if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None

for i, url in enumerate(image_urls):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        cols[i].image(img, caption=f'ภาพที่ {i+1}', width=180)
        with cols[i]:
            if st.button(f"เลือกภาพที่ {i+1}", key=f"btn{i}"):
                st.session_state.selected_index = i
    else:
        cols[i].error("โหลดภาพไม่สำเร็จ")

st.markdown("---")
st.write("**ลากปรับขนาดภาพตามแกน X และ Y (px):**")

# ปรับความกว้าง (X)
img_width = st.slider("ความกว้าง (แกน X)", min_value=100, max_value=900, value=600, step=10)
# ปรับความสูง (Y)
img_height = st.slider("ความสูง (แกน Y)", min_value=100, max_value=900, value=400, step=10)

if st.session_state.selected_index is not None:
    st.markdown("---")
    st.subheader("ภาพที่คุณเลือก (ขนาดปรับได้ตามแกน X และ Y):")
    response = requests.get(image_urls[st.session_state.selected_index])
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        # ปรับขนาดภาพแบบไม่รักษาสัดส่วน (stretch)
        img_resized = img.resize((img_width, img_height))
        st.image(img_resized, caption=f"ภาพที่ {st.session_state.selected_index+1}", width=img_width)
    else:
        st.error("ไม่สามารถโหลดภาพที่เลือกได้")
