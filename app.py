import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# Gemini API 키 가져오기
api_key = os.getenv("GEMINI_API_KEY")

# API 키 설정
genai.configure(api_key=api_key)

# Gemini 모델 설정
model = genai.GenerativeModel('gemini-1.5-pro')

# 페이지 제목 설정
st.title("Gemini AI 챗봇")
st.write("Gemini API를 사용한 간단한 챗봇입니다. 질문을 입력해보세요!")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("무엇이든 물어보세요!"):
    # 사용자 메시지 추가 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 생성 중 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("생각 중...")
        
        try:
            # Gemini API로 응답 생성
            response = model.generate_content(prompt)
            full_response = response.text
            
            # 응답 표시
            message_placeholder.markdown(full_response)
            
            # 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        except Exception as e:
            error_message = f"오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
