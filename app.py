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

# 페이지 제목 설정
st.title("Gemini AI 챗봇")
st.write("Gemini API를 사용한 대화 기억 기능이 있는 챗봇입니다. 질문을 입력해보세요!")

# 생성 설정
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "chat_session" not in st.session_state:
    # 대화 세션 초기화 - 수정된 방식으로 생성 설정 적용
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        generation_config=generation_config
    )
    st.session_state.chat_session = model.start_chat(history=[])

# 사이드바에 대화 초기화 버튼 추가
if st.sidebar.button("대화 초기화"):
    st.session_state.messages = []
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        generation_config=generation_config
    )
    st.session_state.chat_session = model.start_chat(history=[])
    st.sidebar.success("대화가 초기화되었습니다!")

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
            # 대화 세션을 통해 응답 생성 (이전 대화 기억)
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text
            
            # 응답 표시
            message_placeholder.markdown(full_response)
            
            # 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        except Exception as e:
            error_message = f"오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# 대화 기록 정보 표시
st.sidebar.subheader("대화 정보")
message_count = len(st.session_state.messages)
st.sidebar.info(f"현재 대화에 {message_count}개의 메시지가 있습니다.")
st.sidebar.caption("'대화 초기화' 버튼을 클릭하면 새로운 대화를 시작할 수 있습니다.")
