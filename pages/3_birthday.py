# ============================================================
# pages/3_birthday.py  v1.0
# 내 생일의 우주 — 생년월일 NASA APOD + AI 감성 메시지
# ============================================================

import html
import streamlit as st
import requests
from datetime import date
from modules.keys import get_anthropic_key
from modules.styles     import inject_global_css
from modules.components import render_footer, render_navbar
from modules.nasa_handler import fetch_apod, get_badges_html
from modules.state      import init_session_state

APOD_START = date(1995, 6, 16)   # APOD 서비스 시작일

st.set_page_config(page_title="내 생일의 우주 · Space Library", page_icon="🎂", layout="wide", initial_sidebar_state="collapsed")
inject_global_css()

# ── 추가 CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    /* 생일 카드 래퍼 */
    .bday-card {
        background: linear-gradient(
            145deg,
            rgba(27,22,48,0.85) 0%,
            rgba(18,12,38,0.92) 100%
        );
        border: 1px solid rgba(206,189,255,0.15);
        border-radius: 6px;
        overflow: hidden;
        box-shadow:
            0 0 60px rgba(150,116,248,0.08),
            inset 0 0 40px rgba(43,0,116,0.08);
    }

    /* 카드 상단 배너 */
    .bday-banner {
        background: linear-gradient(135deg,
            rgba(43,0,116,0.6) 0%,
            rgba(80,20,160,0.4) 50%,
            rgba(20,8,60,0.6) 100%);
        border-bottom: 1px solid rgba(206,189,255,0.1);
        padding: 22px 28px 18px;
        text-align: center;
    }
    .bday-banner-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.35em;
        text-transform: uppercase;
        color: rgba(156,240,255,0.5);
        margin-bottom: 8px;
    }
    .bday-banner-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #e3e0f1 0%, #cebdff 50%, #bdf4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 4px;
    }
    .bday-banner-date {
        font-family: 'Inter', sans-serif;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: rgba(206,189,255,0.4);
    }

    /* 카드 이미지 */
    .bday-img-wrap {
        padding: 20px 24px 0;
        position: relative;
    }

    /* 카드 바디 */
    .bday-body {
        padding: 20px 28px 28px;
    }
    .bday-celestial-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
        font-weight: 600;
        color: #e3e0f1;
        letter-spacing: -0.01em;
        margin-bottom: 4px;
    }
    .bday-celestial-meta {
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: rgba(156,240,255,0.35);
        margin-bottom: 16px;
    }

    /* AI 메시지 박스 */
    .bday-message {
        background: rgba(43,0,116,0.15);
        border: 1px solid rgba(150,116,248,0.15);
        border-left: 2px solid rgba(150,116,248,0.45);
        border-radius: 0 4px 4px 0;
        padding: 18px 20px;
        font-family: 'Manrope', sans-serif;
        font-size: 0.88rem;
        font-weight: 300;
        color: rgba(227,224,241,0.82);
        line-height: 1.9;
        margin: 14px 0 0;
        white-space: pre-wrap;
    }
    .bday-message-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: rgba(150,116,248,0.55);
        margin-bottom: 6px;
    }

    /* 별자리 구분선 */
    .star-divider {
        text-align: center;
        color: rgba(206,189,255,0.12);
        font-size: 0.7rem;
        letter-spacing: 0.6em;
        margin: 18px 0;
        user-select: none;
    }

    /* 카드 푸터 */
    .bday-card-footer {
        border-top: 1px solid rgba(75,68,82,0.12);
        padding: 12px 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: rgba(75,68,82,0.7);
    }

    /* 입력 폼 카드 */
    .form-card {
        background: rgba(18,15,32,0.6);
        border: 1px solid rgba(75,68,82,0.12);
        border-radius: 4px;
        padding: 32px 36px;
    }
</style>
""", unsafe_allow_html=True)

init_session_state()


def generate_birthday_message(birth_date: date, title: str, description: str, api_key: str) -> tuple[str | None, str | None]:
    prompt = f"""당신은 우주도서관의 감성적인 AI 도슨트입니다.

사용자의 생일: {birth_date.strftime('%Y년 %m월 %d일')}
그날 우주에서 포착된 천체: {title}
NASA 설명: {description[:800]}

아래 두 파트로 한국어 메시지를 작성해주세요:

[파트 1 — 생일 메시지] (3~4문장)
이 천체와 사용자의 생일을 연결하는 감성적이고 따뜻한 생일 메시지.
"당신이 태어난 날, 우주는..." 식의 서정적인 문체로 시작하세요.

[파트 2 — 천체 해설] (3~4문장)
이 천체가 무엇인지, 왜 특별한지를 쉽고 흥미롭게 설명하세요.
독자가 이 사진을 처음 보는 것처럼 설레게 써주세요.

두 파트를 빈 줄로 구분해서 작성하세요. 파트 레이블([파트 1], [파트 2])은 포함하지 마세요."""

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            json={
                "model":      "claude-haiku-4-5-20251001",
                "max_tokens": 700,
                "messages":   [{"role": "user", "content": prompt}],
            },
            headers={
                "x-api-key":                                 api_key,
                "anthropic-version":                         "2023-06-01",
                "anthropic-dangerous-direct-browser-access": "true",
            },
            timeout=20,
        )
        if resp.status_code == 401:
            return None, "❌ API 키 오류."
        if resp.status_code == 429:
            return None, "⏳ API 한도 초과. 잠시 후 다시 시도해주세요."
        if resp.status_code != 200:
            return None, f"❌ API 오류 {resp.status_code}"

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


render_navbar()

# ── 헤더 ──────────────────────────────────────────────────────
st.markdown("""
<div style="padding:28px 0 20px;">
    <div style="font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:700;
                letter-spacing:0.3em; text-transform:uppercase;
                color:rgba(156,240,255,0.45); margin-bottom:10px;">
        ◈ Personal Archive · Birthday Universe
    </div>
    <div style="font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700;
                color:#e3e0f1; letter-spacing:-0.02em; margin-bottom:4px;">
        내 생일의 우주
    </div>
    <div style="font-family:'Manrope',sans-serif; font-size:0.85rem; font-weight:300;
                color:rgba(227,224,241,0.4);">
        당신이 태어난 그날, 우주는 무엇을 보여주고 있었을까요?
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── 입력 폼 ───────────────────────────────────────────────────
col_form, col_gap = st.columns([1, 1.6])

with col_form:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Inter',sans-serif; font-size:0.58rem; font-weight:700;
                letter-spacing:0.25em; text-transform:uppercase;
                color:rgba(156,240,255,0.45); margin-bottom:16px;">
        생년월일 입력
    </div>
    """, unsafe_allow_html=True)

    birth_date = st.date_input(
        "생년월일",
        value=date(1995, 6, 16),
        min_value=APOD_START,
        max_value=date.today(),
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✦ 내 생일의 우주 열기", width='stretch'):
        if birth_date < APOD_START:
            st.error(f"APOD 서비스는 1995년 6월 16일부터 시작됐습니다.")
        else:
            with st.spinner("📡 NASA 아카이브에서 그날의 기록을 찾는 중..."):
                fr = fetch_apod(birth_date)

            if fr.error:
                st.error(fr.error)
            else:
                with st.spinner("✦ AI 도슨트가 특별한 메시지를 작성 중..."):
                    anthropic_key = get_anthropic_key()
                    if not anthropic_key:
                        msg, msg_err = None, "❌ Claude API 키가 설정되지 않았습니다. 환경변수 ANTHROPIC_KEY 또는 Streamlit secrets를 확인해주세요."
                    else:
                        msg, msg_err = generate_birthday_message(
                            birth_date, fr.data.title, fr.data.description, anthropic_key
                        )

                st.session_state.bday_result  = fr.data
                st.session_state.bday_date    = birth_date
                st.session_state.bday_message = msg if not msg_err else None

                if msg_err:
                    st.warning(msg_err)

                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ── 결과 카드 ─────────────────────────────────────────────────
if st.session_state.bday_result:
    result    = st.session_state.bday_result
    bday      = st.session_state.bday_date
    ai_msg    = st.session_state.bday_message
    bday_str  = bday.strftime("%Y년 %m월 %d일")

    st.markdown("<br>", unsafe_allow_html=True)

    _, card_col, _ = st.columns([0.05, 1, 0.05])

    with card_col:
        # ── 카드 시작 ──
        st.markdown('<div class="bday-card">', unsafe_allow_html=True)

        # 배너
        st.markdown(f"""
        <div class="bday-banner">
            <div class="bday-banner-eyebrow">
                <span style="width:5px;height:5px;border-radius:50%;background:#bdf4ff;
                             box-shadow:0 0 6px rgba(189,244,255,0.6);display:inline-block;
                             margin-right:6px;"></span>
                NASA Astronomy Picture of the Day
            </div>
            <div class="bday-banner-title">내 생일의 우주</div>
            <div class="bday-banner-date">{html.escape(bday_str)}</div>
        </div>
        """, unsafe_allow_html=True)

        # 이미지 + 정보
        img_col, info_col = st.columns([1.2, 1], gap="medium")

        with img_col:
            st.markdown('<div style="padding:20px 12px 0 24px;">', unsafe_allow_html=True)
            if result.media_type == "video":
                st.video(result.img_url)
            else:
                st.image(result.img_url, width='stretch')
            st.markdown('</div>', unsafe_allow_html=True)

        with info_col:
            badges = get_badges_html(result.title + " " + result.description)
            st.markdown(f"""
            <div style="padding:24px 24px 0 8px;">
                <div style="margin-bottom:10px;">{badges}</div>
                <div class="bday-celestial-name">{html.escape(result.title)}</div>
                <div class="bday-celestial-meta">NASA APOD · {html.escape(bday_str)}</div>
                <div class="star-divider">· · · · · · · · · ·</div>
            """, unsafe_allow_html=True)

            if ai_msg:
                parts = ai_msg.split("\n\n", 1)
                birthday_part  = parts[0].strip() if len(parts) > 0 else ""
                celestial_part = parts[1].strip() if len(parts) > 1 else ""

                st.markdown(f"""
                <div class="bday-message-label">✦ 생일 메시지</div>
                <div class="bday-message">{html.escape(birthday_part)}</div>
                """, unsafe_allow_html=True)

                if celestial_part:
                    st.markdown(f"""
                    <div class="bday-message-label" style="margin-top:14px;">◈ 천체 해설</div>
                    <div class="bday-message">{html.escape(celestial_part)}</div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bday-message">{html.escape(result.description[:400])}...</div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # 카드 푸터
        st.markdown(f"""
        <div class="bday-card-footer">
            <span>우주도서관 · Space Library</span>
            <span>NASA Open Archive · {bday.year}</span>
            <span style="display:flex;align-items:center;gap:5px;">
                <span style="width:4px;height:4px;border-radius:50%;background:#bdf4ff;
                             box-shadow:0 0 5px rgba(189,244,255,0.5);display:inline-block;"></span>
                Verified · APOD
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)   # .bday-card 닫기

        # ── 공유 버튼 + 원본 링크 ──────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        share_col, link_col = st.columns([1, 1], gap="small")

        share_text = f"내가 태어난 날 NASA가 이걸 찍었어 🌌 ({bday_str} · {result.title}) → {result.img_url}"

        with share_col:
            # JS 클립보드 복사 버튼
            import streamlit.components.v1 as components
            components.html(f"""
            <style>
                button.share-btn {{
                    width: 100%;
                    background: linear-gradient(135deg, rgba(206,189,255,0.12), rgba(43,0,116,0.25));
                    color: #cebdff;
                    border: 1px solid rgba(206,189,255,0.22);
                    padding: 10px 16px;
                    font-family: 'Space Grotesk', sans-serif;
                    font-size: 0.75rem;
                    font-weight: 700;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                    border-radius: 3px;
                    cursor: pointer;
                    transition: all 0.25s ease;
                }}
                button.share-btn:hover {{
                    background: linear-gradient(135deg, rgba(206,189,255,0.22), rgba(43,0,116,0.45));
                    border-color: rgba(206,189,255,0.45);
                    color: #e8ddff;
                }}
                button.share-btn.copied {{
                    border-color: rgba(156,240,255,0.45);
                    color: #9cf0ff;
                }}
            </style>
            <button class="share-btn" onclick="
                navigator.clipboard.writeText({repr(share_text)}).then(() => {{
                    this.textContent = '✓ 복사됨';
                    this.classList.add('copied');
                    setTimeout(() => {{
                        this.textContent = '◈ 공유 문구 복사';
                        this.classList.remove('copied');
                    }}, 2000);
                }});
            ">◈ 공유 문구 복사</button>
            """, height=48)

        with link_col:
            if result.img_url and result.media_type != "video":
                st.link_button("↗ 원본 고해상도 이미지 보기", result.img_url, width='stretch')

render_footer()
