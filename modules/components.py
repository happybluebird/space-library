# ============================================================
# modules/components.py
# 재사용 UI 컴포넌트 (ui_components.py에서 분리)
# ============================================================

import streamlit as st
from datetime import date


def render_navbar() -> None:
    """모든 페이지 상단에 렌더링되는 네비게이션 바"""
    logo_col, nav_col = st.columns([1, 4])

    with logo_col:
        st.markdown(
            '<div class="nav-logo">🏛 우주도서관</div>',
            unsafe_allow_html=True,
        )

    with nav_col:
        c1, c2, c3, c4, c5, c6, _ = st.columns([1, 1, 1, 1, 1, 1, 0.5])
        with c1:
            st.page_link("app.py",               label="홈",        icon="🏠")
        with c2:
            st.page_link("pages/1_explore.py",   label="탐색",        icon="🔭")
        with c3:
            st.page_link("pages/2_collection.py", label="나의 항성계", icon="🪐")
        with c4:
            st.page_link("pages/3_birthday.py",  label="생일의 우주", icon="🎂")
        with c5:
            st.page_link("pages/3_chat.py",      label="AI 도슨트",   icon="💬")
        with c6:
            st.page_link("pages/5_stars.py",     label="별 아카이브", icon="⭐")
        with c6:
            st.page_link("pages/4_pricing.py",   label="구독 플랜",  icon="🪐")

    st.markdown(
        '<hr style="margin:0 0 8px; border-color:rgba(75,68,82,0.15);">',
        unsafe_allow_html=True,
    )


def render_solar_monitor() -> None:
    st.markdown('<div class="section-label">☀ Solar Monitor</div>', unsafe_allow_html=True)
    sdo_urls = [
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_512_0193.jpg",
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0193.jpg",
    ]
    loaded = False
    for url in sdo_urls:
        try:
            st.image(url, width='stretch')
            st.markdown(
                f'<p style="font-family:Inter,sans-serif; font-size:0.58rem; font-weight:700;'
                f' letter-spacing:0.15em; text-transform:uppercase; color:rgba(75,68,82,0.8);'
                f' text-align:center; margin-top:4px;">NASA SDO · {date.today()} · Live Feed</p>',
                unsafe_allow_html=True,
            )
            loaded = True
            break
        except Exception:
            continue
    if not loaded:
        st.markdown("""
        <div style="background:#0d0d18; border:1px solid rgba(75,68,82,0.12); border-radius:2px;
                    padding:14px; text-align:center; font-family:'Inter',sans-serif;">
            <span style="font-size:0.6rem; font-weight:700; letter-spacing:0.15em;
                         text-transform:uppercase; color:rgba(75,68,82,0.7);">
                Feed Offline<br>
                <a href="https://sdo.gsfc.nasa.gov" target="_blank"
                   style="color:rgba(206,189,255,0.35); text-decoration:none;">
                   ↗ sdo.gsfc.nasa.gov
                </a>
            </span>
        </div>
        """, unsafe_allow_html=True)


def render_footer() -> None:
    st.markdown("""
    <div style="margin-top:80px; padding:22px 0;
                border-top: 1px solid rgba(75,68,82,0.1);
                display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;
                font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:700;
                letter-spacing:0.15em; text-transform:uppercase;
                color:rgba(156,240,255,0.25);">
        <span>© 2026 우주도서관 · Space Library · v5.0</span>
        <span>NASA Open API · Claude AI · Free Tier</span>
        <span style="display:flex; align-items:center; gap:5px;">
            <span style="width:4px;height:4px;border-radius:50%;background:#bdf4ff;
                         box-shadow:0 0 5px rgba(189,244,255,0.5);display:inline-block;"></span>
            Cosmic Status: Stable
        </span>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(icon: str, title: str, subtitle: str = "") -> None:
    st.markdown(f"""
    <div style="text-align:center; padding:80px 20px;">
        <div style="font-size:1.8rem; margin-bottom:20px; opacity:0.2;">{icon}</div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:0.95rem;
                    font-weight:600; color:rgba(206,189,255,0.25); margin-bottom:8px;">{title}</div>
        <div style="font-family:'Inter',sans-serif; font-size:0.6rem;
                    font-weight:700; letter-spacing:0.15em; text-transform:uppercase;
                    color:rgba(75,68,82,0.7);">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
