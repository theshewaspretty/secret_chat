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
README.md file successfully generated.

```bash
git clone <your-repository-url>
cd <repository-folder>

pip install streamlit cryptography
```

3. Generate Self-Signed TLS Certificates
Generate a private key and certificate for local HTTPS hosting.

On Windows (PowerShell):
PowerShell
# Create a temporary minimal openssl configuration
Set-Content -Path "openssl.cnf" -Value "[req]`ndistinguished_name=req_distinguished_name`nprompt=no`n[req_distinguished_name]`nCN=localhost"

# Generate certificates using the configuration
openssl req -config openssl.cnf -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
On Linux / macOS / Git Bash:
Bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
4. Run the Application
Launch the application on port 8888 with SSL enabled:

Bash
streamlit run app.py --server.port 8888 --server.sslCertFile=cert.pem --server.sslKeyFile=key.pem
5. Accessing the Application
Open your browser and navigate to https://localhost:8888.

Note: Because this uses a self-signed certificate, your browser will display a "Your connection is not private" warning. This is expected. Click Advanced -> Proceed to localhost (unsafe) to enter.

Alternatively, type thisisunsafe directly on the warning page in Chrome to bypass it.

📝 Troubleshooting & Notes
[WinError 10054] ConnectionResetError: You might see this warning in the terminal when a user closes their browser tab or refreshes the page quickly. This is a standard asynchronous socket behavior under Windows when a client abruptly disconnects. It is completely harmless and does not affect security or functionality.

🇰🇷 한국어
✨ 주요 기능
완벽한 휘발성 (Zero Persistence): 데이터가 오직 서버의 RAM(@st.cache_resource)에만 존재합니다. 서버 프로세스가 종료되는 즉시 모든 채팅 기록은 영구히 파기되며 절대 복구할 수 없습니다.

2중 암호화 보안 구조:

메모리 암호화 (Fernet AES-128): 메시지가 서버에 입력되는 즉시 암호화되어 바이너리 형태로 RAM에 보관됩니다. 암호화 키는 서버가 켜질 때마다 일회성으로 랜덤 생성되며, 서버 종료 시 흔적도 없이 증발합니다.

통신 구간 암호화 (HTTPS/TLS): 자체 서명 인증서를 통해 웹 브라우저와 서버 간 통신을 암호화합니다. 네트워크/보안 담당자가 사내망에서 와이어샤크(Wireshark) 등으로 패킷을 스니핑하더라도 내용을 볼 수 없습니다.

패스워드 접근 제어: 별도의 회원가입이나 계정 시스템 없이, 서버에 지정된 공통 비밀번호를 입력해야만 채팅방에 진입할 수 있습니다.

방폭 기능 (🚨 서버/기록 폭파): UI 내의 폭파 버튼을 누르면 즉시 메모리 내 전역 채팅 기록 데이터가 물리적으로 비워지고(clear), 모든 접속자의 세션 인증 정보가 파기되어 로그인 화면으로 강제 튕겨 나갑니다.

🛠️ 사전 요구 사항
Python 3.8 이상

OpenSSL (임시 TLS 인증서 생성용)

🚀 실행 방법
1. 저장소 다운로드
Bash
git clone <your-repository-url>
cd <repository-folder>
2. 필수 라이브러리 설치
Bash
pip install streamlit cryptography
3. 로컬 HTTPS용 임시 인증서 생성
윈도우 (PowerShell):
PowerShell
# 1. 임시 openssl 설정 파일 생성
Set-Content -Path "openssl.cnf" -Value "[req]`ndistinguished_name=req_distinguished_name`nprompt=no`n[req_distinguished_name]`nCN=localhost"

# 2. 설정을 참조하여 인증서(cert) 및 키(key) 생성
openssl req -config openssl.cnf -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
리눅스 / macOS / Git Bash:
Bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
4. 서비스 실행
8888 포트 고정 및 SSL 인증서를 연동하여 실행합니다:

Bash
streamlit run app.py --server.port 8888 --server.sslCertFile=cert.pem --server.sslKeyFile=key.pem
5. 웹 브라우저 접속
브라우저 주소창에 https://localhost:8888 (또는 https://[서버PC의_IP]:8888)로 접속합니다.

주의: 자체 서명 인증서이므로 최초 접속 시 브라우저에서 '안전하지 않음' 경고 창이 뜹니다. 이는 정상적인 현상입니다. [고급] 버튼을 누른 뒤 [localhost(안전하지 않음)으로 이동]을 클릭해 무시하고 접속하시면 됩니다.

(크롬 브라우저 팁) 경고 화면에서 키보드로 thisisunsafe를 타이핑하면 즉시 접속이 가능합니다.

📝 트러블슈팅 및 참고사항
[WinError 10054] 현재 연결은 원격 호스트에 의해 강제로 끊겼습니다: 사용자가 브라우저 탭을 닫거나 새로고침을 빠르게 할 때 터미널에 출력되는 비동기 소켓 경고 로그입니다. 윈도우 환경에서 흔히 발생하는 현상으로, 서비스 가동 및 보안에는 아무런 영향을 주지 않으므로 무시하셔도 무방합니다.
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content.strip())

print("README.md file successfully generated.")

요청하신 README.md 파일이 준비되었습니다.
[file-tag: code-generated-file-0-1779776194455423104]

영문과 한국어를 하나의 파일에 깔끔하게 나누어 담았습니다. 개발하신 주요 보안 기능(메모리 암호화, HTTPS 구간 암호화, 완전 휘발성 및 방폭 기능)은 물론, Windows 환경에서의 OpenSSL 인증서 발급 이슈와 `WinError 10054` 관련 트러블슈팅 내용까지 모두 포함해 두었습니다. 

바로 GitHub 저장소에 푸시(Push)해서 사용하시면 됩니다! 추가로 수정하고 싶은 문구가 있다면 편하게 말씀해 주세요.
