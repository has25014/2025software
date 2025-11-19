import streamlit as st

st.title(“첫 웹앱 입니다 !”)
name = st.text_input(“이름을 입력해 주세요! : “)
menu = st.selectbox("좋아하는 맛을 선택해 주세요: ",["아몬드봉봉","베리베리스트로베리"]
if st.button("문장 생성"): 
  st.write(name + "님 안녕하세요. 좋아하는 맛은 "+ menu + "이군요!")
