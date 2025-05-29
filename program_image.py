import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("แสดงภาพจาก URL (3 รูป) พร้อมแกน X,Y นอกภาพ")

image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://thumb.ac-illust.com/29/29ce6de610daafcb4d063cd8fdbadbce_t.jpeg",
    "https://s.isanook.com/ca/0/ud/276/1381733/9_cat-1333922_1920.jpg"
]

cols = st.columns(3)

if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None

if 'img_width' not in st.session_state:
    st.session_state.img_width = 600

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
st.write("**ลากเลือกขนาดความกว้างภาพ (พิกเซล):**")
width_slider = st.slider("ความกว้างภาพ", min_value=100, max_value=1000, value=st.session_state.img_width, step=10)
st.session_state.img_width = width_slider

if st.session_state.selected_index is not None:
    st.markdown("---")
    st.subheader("ภาพที่คุณเลือก:")
    response = requests.get(image_urls[st.session_state.selected_index])
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        w_percent = st.session_state.img_width / img.width
        h_size = int(img.height * w_percent)
        img_resized = img.resize((st.session_state.img_width, h_size))
        st.image(img_resized, caption=f"ภาพที่ {st.session_state.selected_index+1}", width=st.session_state.img_width)

        # แสดงแกน X และ Y นอกภาพ (เป็นข้อความ)
        st.markdown("**แกน X (พิกเซล):**")
        x_ticks = list(range(0, img.width + 1, 100))
        st.write(x_ticks)

        st.markdown("**แกน Y (พิกเซล):**")
        y_ticks = list(range(0, img.height + 1, 100))
        st.write(y_ticks)

    else:
        st.error("ไม่สามารถโหลดภาพที่เลือกได้")
