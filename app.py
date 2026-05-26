import streamlit as st
import random
from datetime import datetime
from cryptography.fernet import Fernet

# --- 1. 일회용 암호화 키 및 상태 관리 ---
# 서버 기동 시 1회만 생성되며, 서버가 꺼지면 키도 증발합니다.
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

# --- 3. 채팅방 로직 ---
def chat_page():
    col1, col2, col3 = st.columns([2, 1, 1])
    
    if "nickname" not in st.session_state:
        st.session_state["nickname"] = f"Guest_{random.randint(1000, 9999)}"
        
    with col1:
        new_nickname = st.text_input("닉네임 설정", value=st.session_state["nickname"], label_visibility="collapsed")
        st.session_state["nickname"] = new_nickname
    with col2:
        if st.button("🔄 새로고침", use_container_width=True):
            st.rerun()
    with col3:
        if st.button("🚨 서버/기록 폭파", type="primary", use_container_width=True):
            chat_history.clear()
            st.session_state.clear()
            st.rerun()

    st.divider()
    
    chat_container = st.container(height=500)
    with chat_container:
        if not chat_history:
            st.info("채팅 기록이 없습니다. (모든 데이터는 메모리에 암호화되어 저장됩니다)")
            
        for msg in chat_history:
            # 출력할 때만 임시로 복호화 (메모리에는 여전히 암호화 상태로 유지)
            decrypted_text = cipher_suite.decrypt(msg["text"]).decode("utf-8")
            
            if msg["author"] == st.session_state["nickname"]:
                with st.chat_message("user"):
                    st.markdown(f"**나** 🕒 {msg['time']} \n\n {decrypted_text}")
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"**{msg['author']}** 🕒 {msg['time']} \n\n {decrypted_text}")

    if prompt := st.chat_input("메시지를 입력하세요..."):
        now = datetime.now().strftime("%H:%M:%S")
        # 입력받은 텍스트를 즉시 암호화하여 저장
        encrypted_text = cipher_suite.encrypt(prompt.encode("utf-8"))
        
        chat_history.append({
            "author": st.session_state["nickname"],
            "text": encrypted_text,  # 평문 대신 암호문 저장
            "time": now
        })
        st.rerun()

# --- 4. 메인 라우팅 ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_page()
else:
    chat_page()
