# =============================================================
# 2026. 7. 16.
# streamlit\03_image.py
# 
# Streamlit 라이브러리 기초 실습
#   - image 삽입
# =============================================================
import streamlit as st
from PIL import Image

image = Image.open('image1.png')
image2 = Image.open('image2.png')

st.image(image, caption= "열공하는 은경이")
st.image(image2, caption= "열공하는 은경이: 수채화버전")

st.image(image, caption= "너비를 100으로 수정", width=100)
st.image(image2, caption= "너비를 200으로 수정", width=200)

st.image(image, caption= "전체 너비", width='stretch')
st.image(image2, caption= "원본 너비", width='content')

small_image =image.resize((200, 200)) # 튜플에 담아 리사이즈. 작은 사이즈로 조정

st.image(small_image, caption= "작아진 이미지")