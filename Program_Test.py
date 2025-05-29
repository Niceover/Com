import streamlit as st
import requests
from PIL import Image
import io
import numpy as np
from ultralytics import YOLO

# โหลดโมเดล YOLO
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")  # ใช้โมเดล YOLOv8 nano เพื่อความเร็ว

model = load_model()

# ฟังก์ชันสำหรับโหลดภาพจาก URL
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        return img
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดภาพจาก URL: {e}")
        return None

# ฟังก์ชันสำหรับตรวจจับวัตถุ
def detect_objects(image):
    try:
        # แปลงภาพเป็น numpy array
        img_array = np.array(image)
        # ทำการตรวจจับวัตถุ
        results = model(img_array)
        # ดึงชื่อวัตถุที่ตรวจพบ
        objects = []
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls)
                label = model.names[class_id]
                objects.append(label)
        return list(set(objects))  # ลบวัตถุที่ซ้ำ
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการตรวจจับวัตถุ: {e}")
        return []

# ส่วนติดต่อผู้ใช้
st.title("โปรแกรมตรวจจับวัตถุในภาพ")
st.write("อัปโหลดภาพหรือป้อน URL ของภาพเพื่อตรวจจับวัตถุ")

# ตัวเลือกสำหรับเลือกวิธีโหลดภาพ
option = st.radio("เลือกวิธีโหลดภาพ:", ("อัปโหลดไฟล์", "ใช้ URL"))

image = None
if option == "อัปโหลดไฟล์":
    uploaded_file = st.file_uploader("เลือกไฟล์ภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
else:
    url = st.text_input("ป้อน URL ของภาพ:")
    if url:
        image = load_image_from_url(url)

# แสดงภาพและตรวจจับวัตถุ
if image is not None:
    st.image(image, caption="ภาพที่โหลด", use_column_width=True)
    if st.button("ตรวจจับวัตถุ"):
        with st.spinner("กำลังตรวจจับวัตถุ..."):
            objects = detect_objects(image)
            if objects:
                st.success("ตรวจพบวัตถุต่อไปนี้:")
                for obj in objects:
                    st.write(f"- {obj}")
            else:
                st.warning("ไม่พบวัตถุในภาพหรือเกิดข้อผิดพลาด")
else:
    st.info("กรุณาอัปโหลดภาพหรือป้อน URL เพื่อเริ่มต้น")
