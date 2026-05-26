readme_content = """# 🔒 Ephemeral Secure Local Chat (휘발성 보안 로컬 채팅방)

A lightweight, highly secure, and completely ephemeral local chat application built with Streamlit. Designed for temporary, untraceable communication within a local network without any database or persistent logs.

Streamlit으로 구축된 가볍고 안전한 휘발성 로컬 채팅 애플리케이션입니다. 데이터베이스나 로그 기록 없이, 로컬 네트워크 내에서 안전하고 흔적 없는 일시적 소통을 위해 설계되었습니다.

---

## 🌐 Language / 언어 선택
- [English](#-english)
- [한국어](#-한국어)

---

# 🇺🇸 English

## ✨ Features
- **Zero Persistence:** Data exists exclusively in the server's RAM (`@st.cache_resource`). Once the server process is terminated, all chat history is permanently wiped and unrecoverable.
- **Dual-Layer Encryption:**
  - **In-Memory Encryption (Fernet AES-128):** Messages are encrypted immediately upon receipt and stored as encrypted bytes in memory. The encryption key is dynamically generated at startup and completely destroyed when the server stops.
  - **Transit Encryption (HTTPS/TLS):** Encrypts all data in transit using TLS certificates, mitigating network packet sniffing (e.g., Wireshark) by network or security administrators.
- **Password Protection:** Access is restricted via a simple shared password without the need for registration or account creation.
- **Panic Button (Emergency Wipe):** Features a "Server/Record Wipe" button that instantly clears the in-memory array, flushes all active sessions, and forces users back to the login screen.

## 🛠️ Prerequisites
- Python 3.8 or higher
- OpenSSL (for generating self-signed TLS certificates)

## 🚀 Quick Start

### 1. Clone the Repository
