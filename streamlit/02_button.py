# =============================================================
# 2026. 7. 16.
# streamlit\02_button.py
# 
# Streamlit 라이브러리 기초 실습
#   - code 삽입
#   - 버튼 삽입
# =============================================================

# 라이브러리 불러오기
import streamlit as st
code1 = 'print("hello, world!")'
code2 = 'printf("Hello, world!")'
code3 = '<a href="https://www.naver.com">네이버</a>'

st.code(code1, language='python')
st.code(code2, language='C')
st.code(code3, language='html')

st.divider() # 구분선

st.button('클릭하시오!! ㅋㅋㅋ', type="primary")

if st.button('Reset', type='primary', key='btn1'):
    st.write('Reset 버튼을 눌렀습니다.!')

if st.button('Cancel', type='secondary', key='btn2'):
    st.write('Cancel 버튼이 눌러졌네요!!!')

if st.button('Ignore', type='tertiary', key='btn3'):
    st.write('Ignore 버튼이 눌러졌네요!!!')

def button_write(): # 버튼에 클릭했을때 함수 정의
    st.title('Sorry!!')

st.button('activate', on_click=button_write)    # 클릭하면 함수 실행