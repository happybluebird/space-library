# ============================================================
# pages/3_chat.py  v1.0
# 우주 사진 AI 도슨트 챗봇
# 탐색 페이지에서 불러온 이미지를 기반으로 Claude와 대화
# ============================================================

import html
import streamlit as st
import requests
from modules.styles     import inject_global_css
from modules.components import render_footer, render_empty_state, render_navbar
from modules.keys import get_anthropic_key
from modules.nasa_handler import get_badges_html
from modules.state      import init_session_state

st.set_page_config(page_title="Chat · Space Library", page_icon="💬", layout="wide", initial_sidebar_state="collapsed")
inject_global_css()

# ── 추가 CSS (챗 전용) ────────────────────────────────────────
st.markdown("""
<style>
    /* 채팅 메시지 — AI */
    .chat-msg-ai {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        align-items: flex-start;
    }
    .chat-avatar-ai {
        width: 28px; height: 28px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(150,116,248,0.35), rgba(43,0,116,0.6));
        border: 1px solid rgba(150,116,248,0.3);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem;
        flex-shrink: 0;
    }
    .chat-bubble-ai {
        background: rgba(27,26,38,0.7);
        border: 1px solid rgba(75,68,82,0.15);
        border-left: 2px solid rgba(150,116,248,0.4);
        border-radius: 0 6px 6px 6px;
        padding: 14px 18px;
        font-family: 'Manrope', sans-serif;
        font-size: 0.85rem;
        font-weight: 300;
        color: rgba(227,224,241,0.85);
        line-height: 1.8;
        flex: 1;
    }

    /* 채팅 메시지 — 사용자 */
    .chat-msg-user {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
        align-items: flex-start;
        flex-direction: row-reverse;
    }
    .chat-avatar-user {
        width: 28px; height: 28px;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(156,240,255,0.2), rgba(43,100,116,0.4));
        border: 1px solid rgba(156,240,255,0.25);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem;
        flex-shrink: 0;
    }
    .chat-bubble-user {
        background: rgba(156,240,255,0.05);
        border: 1px solid rgba(156,240,255,0.12);
        border-right: 2px solid rgba(156,240,255,0.3);
        border-radius: 6px 0 6px 6px;
        padding: 12px 16px;
        font-family: 'Manrope', sans-serif;
        font-size: 0.85rem;
        font-weight: 400;
        color: rgba(189,244,255,0.8);
        line-height: 1.7;
        flex: 1;
        text-align: right;
    }

    /* 이미지 패널 */
    .img-panel {
        background: rgba(13,13,24,0.6);
        border: 1px solid rgba(75,68,82,0.12);
        border-radius: 4px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .img-panel-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #e3e0f1;
        letter-spacing: -0.01em;
        margin: 10px 0 4px;
    }
    .img-panel-meta {
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: rgba(156,240,255,0.35);
    }

    /* 대화 초기화 버튼 */
    div.stButton > button[kind="secondary"] {
        background: transparent !important;
        border: 1px solid rgba(75,68,82,0.25) !important;
        color: rgba(204,196,207,0.45) !important;
        font-size: 0.65rem !important;
        padding: 6px 14px !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: rgba(150,116,248,0.3) !important;
        color: rgba(206,189,255,0.7) !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* 입력창 */
    .stChatInput textarea {
        background: rgba(13,13,24,0.85) !important;
        border: 1px solid rgba(75,68,82,0.2) !important;
        color: #e3e0f1 !important;
        font-family: 'Manrope', sans-serif !important;
        border-radius: 3px !important;
    }
    .stChatInput textarea:focus {
        border-color: rgba(206,189,255,0.35) !important;
    }

    /* 채팅 영역 구분선 */
    .chat-divider {
        border: none;
        border-top: 1px solid rgba(75,68,82,0.1);
        margin: 8px 0 20px;
    }
</style>
""", unsafe_allow_html=True)

init_session_state()
render_navbar()

# 탐색 결과 가져오기
result = st.session_state.get("explore_result", None)


def call_claude(messages: list, api_key: str) -> tuple[str | None, str | None]:
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            json={
                "model":      "claude-haiku-4-5-20251001",
                "max_tokens": 1024,
                "system":     st.session_state._chat_system,
                "messages":   messages,
            },
            headers={
                "x-api-key":                                 api_key,
                "anthropic-version":                         "2023-06-01",
                "anthropic-dangerous-direct-browser-access": "true",
            },
            timeout=20,
        )
        if resp.status_code == 401:
            return None, "❌ API 키 오류. secrets.toml의 ANTHROPIC_KEY를 확인해주세요."
        if resp.status_code == 429:
            return None, "⏳ API 한도 초과. 잠시 후 다시 시도해주세요."
        if resp.status_code != 200:
            return None, f"❌ API 오류 {resp.status_code}: {resp.text[:120]}"

        api_data = resp.json()
        text = ""
        if isinstance(api_data, dict):
            text = api_data.get("content", [{}])[0].get("text", "")
        return text or None, None
    except requests.exceptions.Timeout:
        return None, "⏳ 응답 시간 초과. 다시 시도해주세요."
    except requests.exceptions.ConnectionError:
        return None, "🔌 네트워크 연결을 확인해주세요."
    except Exception as e:
        return None, f"❌ 오류: {str(e)[:100]}"


# ── 헤더 + 대화 초기화 버튼 ───────────────────────────────────
hdr_col, btn_col = st.columns([4, 1])
with hdr_col:
    st.markdown("""
    <div style="padding:10px 0 12px;">
        <div style="font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:700;
                    letter-spacing:0.3em; text-transform:uppercase;
                    color:rgba(156,240,255,0.45); margin-bottom:6px;">◈ AI Docent · Chat Interface</div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700;
                    color:#e3e0f1; letter-spacing:-0.02em;">도슨트와 대화하기</div>
    </div>
    """, unsafe_allow_html=True)
with btn_col:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("◻ 대화 초기화", key="clear_chat"):
        st.session_state.chat_messages = []
        st.rerun()
st.markdown("---")

# ── 이미지 없을 때 ─────────────────────────────────────────────
if not result:
    render_empty_state(
        "🔭",
        "관측 대상이 없습니다",
        "탐색 페이지에서 천체 이미지를 먼저 불러와주세요",
    )
    if st.button("✦ 탐색 페이지로 이동"):
        st.switch_page("pages/1_explore.py")
    render_footer()
    st.stop()

# ── API 키 확인 ─────────────────────────────────────────────
anthropic_key = get_anthropic_key()
if not anthropic_key:
    st.warning("❌ Claude API 키가 설정되지 않았습니다. 환경변수 ANTHROPIC_KEY 또는 Streamlit secrets를 확인해주세요.")
    st.info("AI 챗봇 기능은 Claude API 키가 필요합니다. 설정 후 다시 실행해주세요.")
    render_footer()
    st.stop()

# ── 시스템 프롬프트 구성 (탐색 결과 기반) ─────────────────────
system_prompt = f"""당신은 우주도서관의 전문 도슨트 AI입니다.
현재 사용자가 보고 있는 천체 사진 정보:
- 제목: {result.title}
- 출처: NASA · {result.source_id or 'Archive'}
- 설명: {result.description[:1200]}

이 사진에 대해 사용자의 질문에 한국어로 친절하고 흥미롭게 답변하세요.
전문적인 천문학 지식을 쉽고 생동감 있게 전달하는 것이 목표입니다.
답변은 간결하게 유지하되, 핵심 정보를 놓치지 마세요.
질문이 이 사진과 무관한 경우에도 우주·천문학 맥락에서 성실히 답변하세요."""

st.session_state._chat_system = system_prompt

# ── 이미지 + 초기 해설 패널 ────────────────────────────────────
col_img, col_chat = st.columns([1, 1.4], gap="large")

with col_img:
    st.markdown('<div class="img-panel">', unsafe_allow_html=True)
    if result.media_type == "video":
        st.video(result.img_url)
    else:
        st.image(result.img_url, width='stretch')

    badges = get_badges_html(result.title + " " + result.description)
    st.markdown(f"""
    <div style="margin:10px 0 6px;">{badges}</div>
    <div class="img-panel-title">{html.escape(result.title)}</div>
    <div class="img-panel-meta">NASA · {html.escape(result.source_id or 'Archive')}</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.ai_text and st.session_state.ai_text != "AI 해설을 불러오지 못했습니다.":
        with st.expander("◈ 초기 AI 해설", expanded=False):
            st.write(st.session_state.ai_text)

# ── 채팅 영역 ─────────────────────────────────────────────────
with col_chat:
    # 대화 없을 때 안내
    if not st.session_state.chat_messages:
        st.markdown("""
        <div style="padding:24px 20px; background:rgba(27,26,38,0.4);
                    border:1px solid rgba(75,68,82,0.1); border-radius:4px;
                    margin-bottom:20px;">
            <div style="font-family:'Space Grotesk',sans-serif; font-size:0.8rem;
                        font-weight:600; color:rgba(206,189,255,0.5); margin-bottom:12px;">
                질문 예시
            </div>
            <div style="font-family:'Manrope',sans-serif; font-size:0.8rem; font-weight:300;
                        color:rgba(204,196,207,0.45); line-height:2;">
                · 이 천체까지 거리가 얼마나 되나요?<br>
                · 어떤 망원경으로 촬영했나요?<br>
                · 이 사진에서 가장 흥미로운 점은?<br>
                · 블랙홀이 근처에 있나요?<br>
                · 초보자에게 쉽게 설명해 주세요.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 메시지 렌더링
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-msg-user">
                <div class="chat-avatar-user">👤</div>
                <div class="chat-bubble-user">{html.escape(msg['content'])}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-msg-ai">
                <div class="chat-avatar-ai">✦</div>
                <div class="chat-bubble-ai">{html.escape(msg['content'])}</div>
            </div>
            """, unsafe_allow_html=True)

    # 입력창
    user_input = st.chat_input("이 천체에 대해 무엇이든 물어보세요...")

    if user_input:
        st.session_state.chat_messages.append({"role": "user", "content": user_input})

        with st.spinner("✦ 도슨트가 답변을 준비 중..."):
            reply, err = call_claude(st.session_state.chat_messages, anthropic_key)

        if err:
            st.error(err)
            st.session_state.chat_messages.pop()
        else:
            st.session_state.chat_messages.append({"role": "assistant", "content": reply})
            st.rerun()

render_footer()
