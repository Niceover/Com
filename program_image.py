import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

st.title("แสดงภาพพร้อมแกน X,Y ด้วย Matplotlib และ Image Slice (ลากตำแหน่ง Slice ได้)")

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

# แสดงภาพตัวอย่างเล็ก 3 รูป พร้อมปุ่มเลือก
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

        # ----------- เริ่มส่วน Image Slice (ลากตำแหน่ง slice ได้) -----------
        st.markdown("---")
        st.subheader("Image Slice (ตัดภาพ)")

        # slider สำหรับตำแหน่ง slice ของแกน X และ Y
        slice_x_start = st.slider("เริ่มต้นตำแหน่ง X", 0, st.session_state.img_width - 1, 200)
        slice_x_end = st.slider("สิ้นสุดตำแหน่ง X", slice_x_start + 1, st.session_state.img_width, 300)
        slice_y_start = st.slider("เริ่มต้นตำแหน่ง Y", 0, h_size - 1, 300)
        slice_y_end = st.slider("สิ้นสุดตำแหน่ง Y", slice_y_start + 1, h_size, 500)

        # Crop ภาพตามตำแหน่ง slice ที่เลือก
        box = (slice_x_start, slice_y_start, slice_x_end, slice_y_end)
        img_slice = img_resized.crop(box)

        slice_w = slice_x_end - slice_x_start
        slice_h = slice_y_end - slice_y_start

        # แสดงภาพ slice ด้วย matplotlib (พร้อมแกน X,Y)
        fig2, ax2 = plt.subplots()
        ax2.imshow(img_slice)
        ax2.set_xlabel("แกน X (พิกเซล)")
        ax2.set_ylabel("แกน Y (พิกเซล)")
        ax2.set_title("ภาพ Slice (ตัดออกมา)")
        ax2.set_xlim(0, slice_w)
        ax2.set_ylim(slice_h, 0)  # กลับแกน y
        st.pyplot(fig2)

        # แสดงภาพ Slice ด้วย st.image()
        st.image(img_slice, caption="ภาพ Slice (แสดงด้วย st.image())", use_container_width=False)

    else:
        st.error("โหลดภาพไม่สำเร็จ")
