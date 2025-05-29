import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

st.title("แสดงภาพพร้อมแกน X,Y ด้วย Matplotlib และ Image Slice")

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
width_slider = st.slider("ปรับขนาดภาพ (ความกว้าง px)", 100, 900, st.session_state.img_width)
st.session_state.img_width = width_slider

if st.session_state.selected_index is not None:
    st.markdown("---")
    st.subheader("ภาพที่คุณเลือกพร้อมแกน X, Y")

    response = requests.get(image_urls[st.session_state.selected_index])
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

        # ปรับขนาดภาพตาม slider
        w_percent = st.session_state.img_width / img.width
        h_size = int(img.height * w_percent)
        img_resized = img.resize((st.session_state.img_width, h_size))

        # วาดภาพด้วย matplotlib พร้อมแกน
        fig, ax = plt.subplots()
        ax.imshow(img_resized)
        ax.set_xlabel("แกน X (พิกเซล)")
        ax.set_ylabel("แกน Y (พิกเซล)")
        ax.set_title(f"ภาพที่ {st.session_state.selected_index + 1}")

        # ตั้งค่าช่วงแกนให้ตรงกับขนาดภาพ
        ax.set_xlim(0, st.session_state.img_width)
        ax.set_ylim(h_size, 0)  # กลับแกน y ให้ภาพไม่กลับหัว

        st.pyplot(fig)

        # ----------- เริ่มส่วน Image Slice -----------
        st.markdown("---")
        st.subheader("Image Slice (ตัดภาพ)")

        # กำหนดตำแหน่งและขนาด slice ในภาพ resized
        col1, col2, col3, col4 = st.columns(4)
        slice_x = col1.number_input("X (ซ้าย)", min_value=0, max_value=st.session_state.img_width - 1, value=0)
        slice_y = col2.number_input("Y (บน)", min_value=0, max_value=h_size - 1, value=0)
        slice_w = col3.number_input("ความกว้าง", min_value=1, max_value=st.session_state.img_width - slice_x, value=100)
        slice_h = col4.number_input("ความสูง", min_value=1, max_value=h_size - slice_y, value=100)

        # Crop ภาพตาม slice ที่กำหนด
        box = (slice_x, slice_y, slice_x + slice_w, slice_y + slice_h)
        img_slice = img_resized.crop(box)

        # แสดงภาพ slice พร้อมแกน X,Y ด้วย matplotlib
        fig2, ax2 = plt.subplots()
        ax2.imshow(img_slice)
        ax2.set_xlabel("แกน X (พิกเซล)")
        ax2.set_ylabel("แกน Y (พิกเซล)")
        ax2.set_title("ภาพ Slice (ตัดออกมา)")

        ax2.set_xlim(0, slice_w)
        ax2.set_ylim(slice_h, 0)  # กลับแกน y

        st.pyplot(fig2)
    else:
        st.error("โหลดภาพไม่สำเร็จ")
