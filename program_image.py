import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

st.title("แสดงภาพจาก URL (3 รูป)")

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

def draw_axes(img):
    draw = ImageDraw.Draw(img)
    w, h = img.size

    # สร้างฟอนต์พื้นฐาน (ถ้าไม่มีฟอนต์จะใช้ default)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()

    # แกน X (เส้นแดง)
    draw.line((0, h-30, w, h-30), fill="red", width=2)
    # แกน Y (เส้นแดง)
    draw.line((30, 0, 30, h), fill="red", width=2)

    # ตีเครื่องหมายที่แกน X ทุก 100 px
    for x in range(0, w, 100):
        draw.line((x, h-30, x, h-25), fill="red", width=2)
        draw.text((x+2, h-22), str(x), fill="red", font=font)

    # ตีเครื่องหมายที่แกน Y ทุก 100 px
    for y in range(0, h, 100):
        draw.line((25, y, 30, y), fill="red", width=2)
        draw.text((2, y-7), str(y), fill="red", font=font)

    return img

cols = st.columns(3)

if 'selected_index' not in st.session_state:
    st.session_state.selected_index = None

if 'img_width' not in st.session_state:
    st.session_state.img_width = 600  # default

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
        img_with_axes = draw_axes(img.copy())
        w_percent = st.session_state.img_width / img_with_axes.width
        h_size = int(img_with_axes.height * w_percent)
        img_resized = img_with_axes.resize((st.session_state.img_width, h_size))
        st.image(img_resized, caption=f"ภาพที่ {st.session_state.selected_index+1} พร้อมแกน X,Y", width=st.session_state.img_width)
    else:
        st.error("ไม่สามารถโหลดภาพที่เลือกได้")
