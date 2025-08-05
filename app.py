
import streamlit as st

# openai 라이브러리 임포트 (openai==1.52.2 필요)
from openai import OpenAI

# Upstage Solar Pro2 API 키와 엔드포인트 설정
client = OpenAI(
    api_key= st.secrets['OPENAI_API_KEY'],
    base_url="https://api.upstage.ai/v1"
)

st.title("🧑‍🎓 학생 심리상담 챗봇 (Solar Pro2)")

st.write(
    """
    이 챗봇은 학생들의 심리상담을 돕기 위해 만들어졌어요.<br>
    고민, 감정, 힘든 점을 자유롭게 이야기해 주세요.<br>
    <span style='color:gray; font-size:0.9em;'>* 실제 전문 상담이 필요한 경우, 학교 상담센터에 문의해 주세요.</span>
    """,
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 저는 심리상담 챗봇입니다. 어떤 고민이 있으신가요?"}
    ]

# 이전 대화 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("마음 속 이야기를 자유롭게 입력해 주세요."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Upstage Solar Pro2로 메시지 전송
    with st.chat_message("assistant"):
        with st.spinner("상담사가 답변을 작성 중입니다..."):
            # 메시지 포맷 변환
            upstage_messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            # 스트리밍 응답 받기
            response_text = ""
            stream = client.chat.completions.create(
                model="solar-pro2",
                messages=upstage_messages,
                stream=True,
            )
            response_container = st.empty()
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content
                    response_container.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})


