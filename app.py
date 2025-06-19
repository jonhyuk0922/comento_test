import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# API 키 설정
genai.configure(api_key=api_key)

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
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        generation_config=generation_config
    )
    st.session_state.chat_session = model.start_chat(history=[])

# 사이드바 메뉴
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["🤖 챗봇", "📜 대화 기록"])

# 사이드바 기능
if st.sidebar.button("대화 초기화"):
    st.session_state.messages = []
    model = genai.GenerativeModel(
        model_name='gemini-1.5-pro',
        generation_config=generation_config
    )
    st.session_state.chat_session = model.start_chat(history=[])
    st.sidebar.success("대화가 초기화되었습니다!")

# 🤖 챗봇 페이지
if page == "🤖 챗봇":
    st.title("Gemini AI 챗봇")
    st.write("Gemini API를 사용한 대화 기억 기능이 있는 챗봇입니다. 질문을 입력해보세요!")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("무엇이든 물어보세요!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("생각 중...")

            try:
                response = st.session_state.chat_session.send_message(prompt)
                full_response = response.text
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                error_message = f"오류가 발생했습니다: {str(e)}"
                message_placeholder.markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# 📜 대화 기록 페이지
elif page == "📜 대화 기록":
    st.title("📜 대화 기록 보기")
    if st.session_state.messages:
        for i, message in enumerate(st.session_state.messages, 1):
            role = "👤 사용자" if message["role"] == "user" else "🤖 Gemini"
            st.markdown(f"**{i}. {role}**\n\n{message['content']}\n---")
    else:
        st.info("아직 대화 기록이 없습니다.")

# 사이드바 대화 개수 표시
st.sidebar.subheader("대화 정보")
st.sidebar.info(f"현재 대화에 {len(st.session_state.messages)}개의 메시지가 있습니다.")
