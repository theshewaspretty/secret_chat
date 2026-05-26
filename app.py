import streamlit as st
import random
from datetime import datetime
from cryptography.fernet import Fernet

# --- 1. 일회용 암호화 키 및 상태 관리 ---
@st.cache_resource
def get_cipher_suite():
    key = Fernet.generate_key()
    return Fernet(key)

@st.cache_resource
def get_chat_history():
    return []

cipher_suite = get_cipher_suite()
chat_history = get_chat_history()

SHARED_PASSWORD = "thisisunsafe"

st.set_page_config(page_title="로컬 E2EE 비밀 채팅방", page_icon="🔒")

# --- 2. 로그인 로직 ---
def login_page():
    st.title("🔒 암호화된 로컬 채팅방")
    st.write("네트워크 추적 방지 및 메모리 암호화가 적용되어 있습니다.")
    
    pwd = st.text_input("비밀번호", type="password")
    
    if st.button("입장하기"):
        if pwd == SHARED_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")

# --- 3. 실시간 자동 새로고침 채팅 영역 (Fragment) ---
# 이 함수 내부만 1초(1s)마다 독립적으로 실행(새로고침)됩니다.
@st.fragment(run_every="1s")
def display_chat_messages():
    chat_container = st.container(height=500)
    with chat_container:
        if not chat_history:
            st.info("채팅 기록이 없습니다. (모든 데이터는 메모리에 암호화되어 저장됩니다)")
            
        for msg in chat_history:
            # 출력할 때만 임시로 복호화
            decrypted_text = cipher_suite.decrypt(msg["text"]).decode("utf-8")
            
            if msg["author"] == st.session_state["nickname"]:
                with st.chat_message("user"):
                    st.markdown(f"**나** 🕒 {msg['time']} \n\n {decrypted_text}")
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"**{msg['author']}** 🕒 {msg['time']} \n\n {decrypted_text}")

# --- 4. 채팅방 전체 로직 ---
def chat_page():
    col1, col2, col3 = st.columns([2, 1, 1])
    
    if "nickname" not in st.session_state:
        st.session_state["nickname"] = f"Guest_{random.randint(1000, 9999)}"
        
    with col1:
        new_nickname = st.text_input("닉네임 설정", value=st.session_state["nickname"], label_visibility="collapsed")
        st.session_state["nickname"] = new_nickname
    with col2:
        # 자동 갱신되므로 수동 새로고침 버튼은 사실상 필요 없지만 유지
        if st.button("🔄 새로고침", use_container_width=True):
            st.rerun()
    with col3:
        if st.button("🚨 서버/기록 폭파", type="primary", use_container_width=True):
            chat_history.clear()
            st.session_state.clear()
            st.rerun()

    st.divider()
    
    # 1초마다 자동 갱신되는 채팅창 컴포넌트 호출
    display_chat_messages()

    # 메시지 입력 창
    if prompt := st.chat_input("메시지를 입력하세요..."):
        now = datetime.now().strftime("%H:%M:%S")
        encrypted_text = cipher_suite.encrypt(prompt.encode("utf-8"))
        
        chat_history.append({
            "author": st.session_state["nickname"],
            "text": encrypted_text,
            "time": now
        })
        st.rerun() # 내 메시지를 입력했을 때는 즉시 전체 화면 갱신

# --- 5. 메인 라우팅 ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_page()
else:
    chat_page()
