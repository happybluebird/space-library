# ============================================================
# pages/1_explore.py  v6.0 — 사이드바 제거, 상단 navbar + 인라인 컨트롤
# ============================================================

import html
import streamlit as st
from datetime import date, datetime

from modules.styles     import inject_global_css
from modules.components import render_footer, render_navbar
from modules.nasa_handler import fetch_apod, fetch_image_library, get_badges_html, CATEGORY_MAP
from modules.ai_handler import generate_explanation
from modules.keys import get_anthropic_key
from modules.state      import init_session_state
from modules.enums      import SearchMode

st.set_page_config(
    page_title="Archive · Space Library",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_global_css()
init_session_state()

render_navbar()

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div style="padding:16px 0 12px;">
    <div style="font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:700;
                letter-spacing:0.3em; text-transform:uppercase;
                color:rgba(156,240,255,0.45); margin-bottom:8px;">◈ Deep Space Archive</div>
    <div style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700;
                color:#e3e0f1; letter-spacing:-0.02em;">우주 탐색</div>
</div>
""", unsafe_allow_html=True)

# ── 인라인 검색 컨트롤 ────────────────────────────────────────
ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns([1.2, 1.8, 1, 1.2])

with ctrl_col1:
    search_mode: SearchMode = st.radio(
        "탐색 모드",
        list(SearchMode),
        format_func=lambda m: m.value,
        horizontal=False,
        label_visibility="collapsed",
    )

with ctrl_col2:
    if search_mode == SearchMode.APOD:
        selected_date = st.date_input(
            "날짜 선택",
            value=date.today(),
            min_value=date(1995, 6, 16),
            max_value=date.today(),
        )
        selected_keyword = None
    else:
        cat = st.selectbox("카테고리", list(CATEGORY_MAP.keys()))
        selected_keyword = CATEGORY_MAP[cat]
        selected_date = None

with ctrl_col3:
    expert_mode = st.toggle("🔬 Expert Mode", value=False)

with ctrl_col4:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("✦ 분석 시작", width='stretch')

st.markdown("---")

# ── 탐색 실행 ────────────────────────────────────────────────
if run:
    with st.spinner("📡 NASA 아카이브 연결 중..."):
        if search_mode == SearchMode.APOD:
            fr = fetch_apod(selected_date)
        else:
            fr = fetch_image_library(selected_keyword)

        if fr.error:
            st.error(fr.error)
            st.stop()

    anthropic_key = get_anthropic_key()
    with st.spinner("🤖 AI 해설 생성 중..."):
        if not anthropic_key:
            ai_text = "AI 해설을 불러오기 위해 Claude API 키가 필요합니다. 설정을 확인해주세요."
            st.warning("❌ Claude API 키가 설정되지 않았습니다. 환경변수 ANTHROPIC_KEY 또는 Streamlit secrets에 값을 추가해주세요.")
        else:
            ai_text, ai_err = generate_explanation(
                fr.data.title, fr.data.description, anthropic_key, expert_mode
            )
            if ai_err:
                st.warning(ai_err)
                ai_text = "AI 해설을 불러오지 못했습니다."

    st.session_state.explore_count += 1
    st.session_state.history.append({
        "title":     fr.data.title,
        "date":      datetime.now().strftime("%m/%d %H:%M"),
        "source_id": fr.data.source_id,
    })
    st.session_state.explore_result = fr.data
    st.session_state.ai_text = ai_text

# ── 결과 표시 ─────────────────────────────────────────────────
if st.session_state.explore_result:
    result = st.session_state.explore_result
    st.markdown("<br>", unsafe_allow_html=True)

    col_img, col_info = st.columns([1.6, 1])

    with col_img:
        if result.media_type == "video":
            st.video(result.img_url)
        else:
            st.image(result.img_url, width='stretch')

        badges = get_badges_html(result.title + " " + result.description)
        st.markdown(f"<div style='margin:8px 0;'>{badges}</div>", unsafe_allow_html=True)

    with col_info:
        st.markdown(f"""
        <div style="padding:4px 0 14px;">
            <span class="r-tag">ARCHIVE · {html.escape(result.source_id)}</span>
            <div class="r-title">{html.escape(result.title)}</div>
            <div class="r-id">NASA Image &amp; Video Library · Source Verified</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.ai_text and st.session_state.ai_text != "AI 해설을 불러오지 못했습니다.":
            with st.expander("◈ AI 해설 보기", expanded=True):
                st.write(st.session_state.ai_text)
        else:
            st.info(st.session_state.ai_text)

        st.markdown("""
        <div class="info-card">
            <strong>Source</strong>NASA Image &amp; Video Library
        </div>
        """, unsafe_allow_html=True)

        st.link_button("↗ 원본 고해상도 보기", result.img_url, width='stretch')

render_footer()
