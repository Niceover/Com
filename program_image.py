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

image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://thumb.ac-illust.com/29/29ce6de610daafcb4d063cd8fdbadbce_t.jpeg",
    "https://s.isanook.com/ca/0/ud/276/1381733/9_cat-1333922_1920.jpg"
]

cols = st.columns(3)

if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None

# แสดงภาพและปุ่มเลือกภาพ
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

# Slider สำหรับปรับขนาดภาพ
st.markdown("---")
st.write("**ลากปรับขนาดภาพ (ความกว้าง px):**")
img_width = st.slider("ขนาดภาพ", min_value=100, max_value=900, value=600, step=10)

# แสดงภาพใหญ่ตามขนาดที่เลือก
if st.session_state.selected_index is not None:
    st.markdown("---")
    st.subheader("ภาพที่คุณเลือก:")
    response = requests.get(image_urls[st.session_state.selected_index])
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        st.image(img, caption=f"ภาพที่ {st.session_state.selected_index+1} (ขนาดปรับได้)", width=img_width)
    else:
        st.error("ไม่สามารถโหลดภาพที่เลือกได้")
