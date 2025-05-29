import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLO

# โหลดโมเดล YOLO เพียงครั้งเดียว
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")  # ใช้ YOLOv8 nano

model = load_model()

# ------------------- ส่วนแสดงภาพ -------------------

st.title("แสดงภาพ + ตัด Slice + รวมภาพ + ตรวจจับวัตถุด้วย YOLOv8")

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

images = []  # เก็บภาพโหลดแล้ว

# โหลดภาพและแสดงตัวเลือก
for i, url in enumerate(image_urls):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        images.append(img)
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
    st.subheader("ภาพที่คุณเลือก")
    selected_img = images[st.session_state.selected_index]
    w_percent = st.session_state.img_width / selected_img.width
    h_size = int(selected_img.height * w_percent)
    img_resized = selected_img.resize((st.session_state.img_width, h_size))

    st.image(img_resized, caption="ภาพที่เลือก", use_column_width=False)

    st.markdown("---")
    st.subheader("ตัดภาพ (Image Slice)")

    slice_x_start = st.slider("เริ่มต้นตำแหน่ง X", 0, st.session_state.img_width - 1, 200)
    slice_x_end = st.slider("สิ้นสุดตำแหน่ง X", slice_x_start + 1, st.session_state.img_width, 300)
    slice_y_start = st.slider("เริ่มต้นตำแหน่ง Y", 0, h_size - 1, 300)
    slice_y_end = st.slider("สิ้นสุดตำแหน่ง Y", slice_y_start + 1, h_size, 500)

    box = (slice_x_start, slice_y_start, slice_x_end, slice_y_end)
    img_slice = img_resized.crop(box)

    st.image(img_slice, caption="ภาพ Slice", use_column_width=False)

    st.markdown("---")
    st.subheader("รวมภาพ 2 ภาพ")

    # เลือกอีกภาพจาก dropdown
    other_index = st.selectbox("เลือกภาพที่ต้องการรวมด้วย", [i for i in range(len(images)) if i != st.session_state.selected_index], format_func=lambda i: f"ภาพที่ {i+1}")
    combine_mode = st.radio("เลือกภาพที่อยู่ด้านหน้า", ("ภาพหลักอยู่หน้า", "อีกภาพอยู่หน้า"))

    other_img = images[other_index].resize((st.session_state.img_width, h_size))

    # รวมภาพโดยแสดงผลภาพเด่นตามที่เลือก
    if combine_mode == "ภาพหลักอยู่หน้า":
        result_img = Image.blend(other_img, img_resized, alpha=0.4)
    else:
        result_img = Image.blend(img_resized, other_img, alpha=0.4)

    st.image(result_img, caption="ภาพที่รวมกันแล้ว", use_column_width=True)

    # ---------------- ตรวจจับวัตถุด้วย YOLOv8 ----------------
    st.markdown("---")
    st.subheader("ตรวจจับวัตถุในภาพที่รวมแล้ว")

    def detect_objects(image):
        try:
            img_array = np.array(image)
            results = model(img_array)
            objects = []
            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls)
                    label = model.names[class_id]
                    objects.append(label)
            return list(set(objects))  # ลบซ้ำ
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการตรวจจับวัตถุ: {e}")
            return []

    if st.button("ตรวจจับวัตถุจากภาพที่รวมแล้ว"):
        with st.spinner("กำลังตรวจจับวัตถุ..."):
            detected_objects = detect_objects(result_img)
            if detected_objects:
                st.success("ตรวจพบวัตถุต่อไปนี้:")
                for obj in detected_objects:
                    st.write(f"- {obj}")
            else:
                st.warning("ไม่พบวัตถุในภาพ")

else:
    st.info("กรุณาเลือกภาพด้านบนก่อน")
