# ============================================================
# modules/styles.py
# 전역 CSS 주입 (ui_components.py에서 분리)
# ============================================================

import streamlit as st


def inject_global_css() -> None:
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Manrope:wght@200;300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── 전체 배경 ── */
    .stApp {
        background-color: #0a0814;
        background-image:
            radial-gradient(circle at 50% 30%, rgba(80,50,120,0.35) 0%, transparent 55%),
            radial-gradient(circle at 15% 20%, rgba(43,0,116,0.25) 0%, transparent 45%),
            radial-gradient(circle at 85% 80%, rgba(20,8,60,0.35) 0%, transparent 50%);
        background-attachment: fixed;
        color: #e3e0f1;
        font-family: 'Manrope', sans-serif;
    }

    /* 별 레이어 */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(1.2px 1.2px at 8%  12%, rgba(255,255,255,0.8) 0%, transparent 100%),
            radial-gradient(1px   1px   at 22% 8%,  rgba(200,190,255,0.6) 0%, transparent 100%),
            radial-gradient(1.3px 1.3px at 45% 5%,  rgba(255,255,255,0.9) 0%, transparent 100%),
            radial-gradient(0.9px 0.9px at 67% 15%, rgba(255,240,200,0.7) 0%, transparent 100%),
            radial-gradient(1px   1px   at 88% 8%,  rgba(255,255,255,0.6) 0%, transparent 100%),
            radial-gradient(1px   1px   at 12% 35%, rgba(200,210,255,0.5) 0%, transparent 100%),
            radial-gradient(1.1px 1.1px at 35% 28%, rgba(255,255,255,0.7) 0%, transparent 100%),
            radial-gradient(0.8px 0.8px at 72% 42%, rgba(255,255,255,0.5) 0%, transparent 100%),
            radial-gradient(1px   1px   at 92% 35%, rgba(200,190,255,0.6) 0%, transparent 100%),
            radial-gradient(0.9px 0.9px at 5%  58%, rgba(255,255,255,0.4) 0%, transparent 100%),
            radial-gradient(1px   1px   at 28% 62%, rgba(255,240,200,0.6) 0%, transparent 100%),
            radial-gradient(0.8px 0.8px at 55% 55%, rgba(255,255,255,0.5) 0%, transparent 100%),
            radial-gradient(1.2px 1.2px at 78% 68%, rgba(200,210,255,0.7) 0%, transparent 100%),
            radial-gradient(1px   1px   at 18% 80%, rgba(255,255,255,0.6) 0%, transparent 100%),
            radial-gradient(0.8px 0.8px at 42% 85%, rgba(200,190,255,0.5) 0%, transparent 100%),
            radial-gradient(1px   1px   at 65% 78%, rgba(255,255,255,0.7) 0%, transparent 100%),
            radial-gradient(0.9px 0.9px at 85% 90%, rgba(255,240,200,0.5) 0%, transparent 100%),
            radial-gradient(1.1px 1.1px at 30% 45%, rgba(255,255,255,0.4) 0%, transparent 100%),
            radial-gradient(0.8px 0.8px at 58% 32%, rgba(200,190,255,0.5) 0%, transparent 100%),
            radial-gradient(1px   1px   at 95% 72%, rgba(255,255,255,0.4) 0%, transparent 100%);
        pointer-events: none;
        z-index: 0;
    }

    /* ── Streamlit 기본 UI 정리 ── */
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
    [data-testid="stDecoration"] { display: none; }
    /* 사이드바 토글 버튼 숨김 (상단 navbar 사용) */
    [data-testid="collapsedControl"] { display: none; }
    [data-testid="stSidebarCollapsedControl"] { display: none; }

    /* ── 사이드바 ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,
            rgba(8,5,20,0.98) 0%,
            rgba(12,8,28,0.98) 100%) !important;
        border-right: 1px solid rgba(75,68,82,0.12) !important;
    }
    [data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── 버튼 ── */
    div.stButton > button {
        background: linear-gradient(135deg,
            rgba(206,189,255,0.12) 0%,
            rgba(43,0,116,0.25) 100%) !important;
        color: #cebdff !important;
        border: 1px solid rgba(206,189,255,0.22) !important;
        padding: 12px 24px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        transition: all 0.25s ease !important;
        border-radius: 3px !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg,
            rgba(206,189,255,0.22) 0%,
            rgba(43,0,116,0.45) 100%) !important;
        border-color: rgba(206,189,255,0.45) !important;
        color: #e8ddff !important;
        box-shadow: 0 0 24px rgba(150,80,255,0.12) !important;
        transform: translateY(-1px) !important;
    }

    /* ── 정보 카드 ── */
    .info-card {
        background: rgba(27,26,38,0.5);
        border: 1px solid rgba(75,68,82,0.12);
        border-left: 2px solid rgba(150,116,248,0.35);
        border-radius: 2px;
        padding: 16px 20px;
        margin: 10px 0;
        font-family: 'Inter', monospace;
        font-size: 0.78rem;
        line-height: 1.8;
        color: #ccc4cf;
    }
    .info-card strong {
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #9cf0ff;
        display: block;
        margin-bottom: 4px;
    }

    /* ── 히어로 ── */
    .hero-section {
        padding: 48px 0 40px;
        border-bottom: 1px solid rgba(75,68,82,0.1);
        margin-bottom: 48px;
    }
    .hero-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        color: rgba(156,240,255,0.55);
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .status-pulse {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #bdf4ff;
        display: inline-block;
        box-shadow: 0 0 8px rgba(189,244,255,0.6);
        animation: blink 2s ease-in-out infinite;
    }
    @keyframes blink {
        0%,100% { opacity: 1; }
        50%      { opacity: 0.25; }
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.8rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 1.05;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #e3e0f1 0%, #cebdff 40%, #bdf4ff 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-sub {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.82rem;
        font-weight: 400;
        color: rgba(189,244,255,0.4);
        letter-spacing: 0.25em;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .hero-desc {
        font-family: 'Manrope', sans-serif;
        font-size: 0.92rem;
        font-weight: 300;
        color: rgba(227,224,241,0.55);
        line-height: 1.85;
        max-width: 540px;
    }

    /* ── 섹션 레이블 ── */
    .section-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: rgba(156,240,255,0.45);
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(75,68,82,0.1);
    }

    /* ── 벤토 카드 ── */
    .bento-card {
        background: rgba(27,26,38,0.55);
        border: 1px solid rgba(75,68,82,0.1);
        border-radius: 3px;
        padding: 22px 24px;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        height: 100%;
    }
    .bento-card:hover {
        background: rgba(41,41,53,0.65);
        border-color: rgba(206,189,255,0.18);
        transform: translateY(-2px);
    }
    .bento-num {
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        color: rgba(150,116,248,0.45);
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .bento-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: #e3e0f1;
        margin-bottom: 8px;
        letter-spacing: -0.01em;
    }
    .bento-desc {
        font-family: 'Manrope', sans-serif;
        font-size: 0.76rem;
        font-weight: 300;
        color: rgba(204,196,207,0.5);
        line-height: 1.7;
    }

    /* ── 상태 바 ── */
    .status-bar {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        padding: 14px 0;
        margin-top: 28px;
        border-top: 1px solid rgba(75,68,82,0.1);
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: rgba(75,68,82,0.85);
    }
    .s-dot {
        width: 5px; height: 5px; border-radius: 50%;
        background: #bdf4ff;
        box-shadow: 0 0 6px rgba(189,244,255,0.5);
        display: inline-block;
        margin-right: 5px;
        animation: blink 2s ease-in-out infinite;
    }

    /* ── 카운터 ── */
    .counter-wrap { display:flex; gap:20px; padding:10px 0; }
    .c-num {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: #cebdff;
        letter-spacing: -0.03em;
        line-height: 1;
        text-shadow: 0 0 20px rgba(206,189,255,0.25);
    }
    .c-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.55rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: rgba(75,68,82,0.85);
        margin-top: 4px;
    }

    /* ── 히스토리 ── */
    .h-item {
        padding: 8px 0;
        border-bottom: 1px solid rgba(75,68,82,0.1);
    }
    .h-item:last-child { border-bottom: none; }
    .h-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem;
        font-weight: 500;
        color: rgba(206,189,255,0.55);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 195px;
    }
    .h-meta {
        font-family: 'Inter', sans-serif;
        font-size: 0.56rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(75,68,82,0.8);
        margin-top: 2px;
    }

    /* ── 결과 카드 ── */
    .r-tag {
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #9cf0ff;
        background: rgba(156,240,255,0.08);
        border: 1px solid rgba(156,240,255,0.18);
        padding: 2px 8px;
        border-radius: 2px;
        display: inline-block;
        margin-right: 4px;
        margin-bottom: 8px;
    }
    .r-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #e3e0f1;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    .r-id {
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: rgba(156,240,255,0.35);
        margin-bottom: 14px;
    }

    /* ── 뱃지 ── */
    .badge-hubble  { background:rgba(58,110,165,0.15);  color:#9cf0ff;  padding:2px 8px; border-radius:2px; font-size:0.62em; border:1px solid rgba(58,110,165,0.22);  margin-right:4px; font-family:'Inter',monospace; letter-spacing:0.06em; }
    .badge-webb    { background:rgba(212,175,55,0.1);   color:#ffe16d;  padding:2px 8px; border-radius:2px; font-size:0.62em; border:1px solid rgba(212,175,55,0.18);  margin-right:4px; font-family:'Inter',monospace; letter-spacing:0.06em; }
    .badge-chandra { background:rgba(150,116,248,0.15); color:#cebdff;  padding:2px 8px; border-radius:2px; font-size:0.62em; border:1px solid rgba(150,116,248,0.22); margin-right:4px; font-family:'Inter',monospace; letter-spacing:0.06em; }
    .badge-solar   { background:rgba(233,196,0,0.1);    color:#e9c400;  padding:2px 8px; border-radius:2px; font-size:0.62em; border:1px solid rgba(233,196,0,0.18);   margin-right:4px; font-family:'Inter',monospace; letter-spacing:0.06em; }
    .badge-mars    { background:rgba(230,126,34,0.1);   color:#ff9966;  padding:2px 8px; border-radius:2px; font-size:0.62em; border:1px solid rgba(230,126,34,0.18);  margin-right:4px; font-family:'Inter',monospace; letter-spacing:0.06em; }
    .badge-deep    { background:rgba(43,0,116,0.3);     color:#9674f8;  padding:2px 8px; border-radius:2px; font-size:0.62em; border:1px solid rgba(43,0,116,0.38);    margin-right:4px; font-family:'Inter',monospace; letter-spacing:0.06em; }
    .badge-generic { background:rgba(52,52,64,0.45);    color:rgba(204,196,207,0.55); padding:2px 8px; border-radius:2px; font-size:0.62em; border:1px solid rgba(74,69,78,0.25); margin-right:4px; font-family:'Inter',monospace; letter-spacing:0.06em; }

    /* ── 상단 네비게이션 바 ── */
    .top-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 8px 12px;
        border-bottom: 1px solid rgba(75,68,82,0.15);
        margin-bottom: 28px;
        background: rgba(8,5,20,0.6);
        backdrop-filter: blur(12px);
        border-radius: 4px;
    }
    .nav-logo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #cebdff;
        letter-spacing: -0.02em;
        white-space: nowrap;
    }
    /* page_link 버튼 오버라이드 */
    [data-testid="stPageLink"] a {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: rgba(189,244,255,0.45) !important;
        text-decoration: none !important;
        padding: 5px 10px !important;
        border-radius: 3px !important;
        transition: all 0.2s ease !important;
        border: 1px solid transparent !important;
    }
    [data-testid="stPageLink"] a:hover {
        color: #cebdff !important;
        border-color: rgba(206,189,255,0.2) !important;
        background: rgba(206,189,255,0.06) !important;
    }
    [data-testid="stPageLink-active"] a {
        color: #cebdff !important;
        border-color: rgba(206,189,255,0.25) !important;
        background: rgba(206,189,255,0.08) !important;
    }

    /* ── 기타 ── */
    hr { border-color: rgba(75,68,82,0.1) !important; }
    .stTextInput input { background:rgba(13,13,24,0.8) !important; border:1px solid rgba(75,68,82,0.15) !important; color:#e3e0f1 !important; font-family:'Space Grotesk',sans-serif !important; border-radius:2px !important; }
    .stTextInput input:focus { border-color:rgba(206,189,255,0.35) !important; box-shadow:none !important; }
    .stTextInput input::placeholder { color:rgba(150,141,153,0.35) !important; }
    .stRadio label { font-family:'Inter',sans-serif !important; font-size:0.78rem !important; color:rgba(204,196,207,0.65) !important; }
    .stSelectbox label { font-family:'Inter',sans-serif !important; font-size:0.6rem !important; font-weight:700 !important; letter-spacing:0.15em !important; text-transform:uppercase !important; color:rgba(156,240,255,0.45) !important; }
    .stToggle label { font-family:'Inter',sans-serif !important; font-size:0.78rem !important; color:rgba(204,196,207,0.65) !important; }
    .stCaption p { font-family:'Inter',sans-serif !important; font-size:0.62rem !important; font-weight:700 !important; letter-spacing:0.12em !important; text-transform:uppercase !important; color:rgba(75,68,82,0.85) !important; }
    .stMarkdown p { font-family:'Manrope',sans-serif; color:rgba(227,224,241,0.75); line-height:1.75; }
    h1 { font-family:'Space Grotesk',sans-serif !important; font-weight:700 !important; color:#e3e0f1 !important; letter-spacing:-0.02em !important; }
    h2 { font-family:'Space Grotesk',sans-serif !important; font-weight:600 !important; color:#cebdff !important; }
    h3 { font-family:'Space Grotesk',sans-serif !important; font-weight:500 !important; color:rgba(206,189,255,0.8) !important; }
</style>
""", unsafe_allow_html=True)
