# ============================================================
# pages/4_pricing.py  v1.0
# 구독 플랜 페이지 — Explorer / Astronomer / Pioneer
# 연간 할인 토글 포함
# ============================================================

import streamlit as st
from modules.styles     import inject_global_css
from modules.components import render_footer, render_navbar
from modules.state      import init_session_state

st.set_page_config(page_title="Pricing · Space Library", page_icon="🪐", layout="wide", initial_sidebar_state="collapsed")
inject_global_css()
init_session_state()
render_navbar()

# ── 추가 CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    /* 플랜 카드 */
    .plan-card {
        background: rgba(18,15,32,0.7);
        border: 1px solid rgba(75,68,82,0.15);
        border-radius: 6px;
        padding: 32px 28px 28px;
        height: 100%;
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
    }
    .plan-card:hover {
        border-color: rgba(206,189,255,0.22);
        box-shadow: 0 0 40px rgba(150,116,248,0.06);
        transform: translateY(-2px);
    }
    .plan-card.featured {
        background: linear-gradient(145deg,
            rgba(43,0,116,0.35) 0%,
            rgba(27,22,48,0.85) 100%);
        border-color: rgba(150,116,248,0.35);
        box-shadow: 0 0 60px rgba(150,116,248,0.1);
    }

    /* 플랜 헤더 */
    .plan-badge {
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 2px;
        display: inline-block;
        margin-bottom: 16px;
    }
    .plan-badge.free    { color: rgba(156,240,255,0.7);  background: rgba(156,240,255,0.08);  border: 1px solid rgba(156,240,255,0.18); }
    .plan-badge.popular { color: #cebdff; background: rgba(150,116,248,0.15); border: 1px solid rgba(150,116,248,0.3); }
    .plan-badge.pro     { color: #ffe16d; background: rgba(212,175,55,0.1);   border: 1px solid rgba(212,175,55,0.22); }

    .plan-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #e3e0f1;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }
    .plan-tagline {
        font-family: 'Manrope', sans-serif;
        font-size: 0.78rem;
        font-weight: 300;
        color: rgba(204,196,207,0.5);
        margin-bottom: 22px;
        line-height: 1.6;
    }

    /* 가격 */
    .plan-price {
        display: flex;
        align-items: baseline;
        gap: 4px;
        margin-bottom: 6px;
    }
    .plan-price-amount {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #e3e0f1;
    }
    .plan-price-unit {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: rgba(204,196,207,0.4);
    }
    .plan-price-note {
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(156,240,255,0.4);
        margin-bottom: 24px;
    }

    /* 기능 목록 */
    .plan-divider {
        border: none;
        border-top: 1px solid rgba(75,68,82,0.1);
        margin: 0 0 18px;
    }
    .plan-feature {
        font-family: 'Manrope', sans-serif;
        font-size: 0.8rem;
        font-weight: 400;
        color: rgba(227,224,241,0.65);
        padding: 5px 0;
        display: flex;
        align-items: center;
        gap: 8px;
        line-height: 1.5;
    }
    .plan-feature.inactive {
        color: rgba(75,68,82,0.6);
        text-decoration: line-through;
    }
    .feat-icon { font-size: 0.75rem; flex-shrink: 0; }

    /* 절감 배지 */
    .save-badge {
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #9cf0ff;
        background: rgba(156,240,255,0.08);
        border: 1px solid rgba(156,240,255,0.18);
        padding: 2px 8px;
        border-radius: 2px;
        margin-left: 8px;
        vertical-align: middle;
    }

    /* FAQ */
    .faq-item {
        border-bottom: 1px solid rgba(75,68,82,0.1);
        padding: 18px 0;
    }
    .faq-q {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        color: rgba(206,189,255,0.75);
        margin-bottom: 8px;
    }
    .faq-a {
        font-family: 'Manrope', sans-serif;
        font-size: 0.8rem;
        font-weight: 300;
        color: rgba(204,196,207,0.5);
        line-height: 1.75;
    }
</style>
""", unsafe_allow_html=True)

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div style="padding:40px 0 32px; text-align:center;">
    <div style="font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:700;
                letter-spacing:0.35em; text-transform:uppercase;
                color:rgba(156,240,255,0.45); margin-bottom:14px;">
        ◈ Subscription Plans
    </div>
    <div style="font-family:'Space Grotesk',sans-serif; font-size:2.4rem; font-weight:700;
                letter-spacing:-0.03em; color:#e3e0f1; margin-bottom:10px;">
        우주를 탐험할 준비가 됐나요?
    </div>
    <div style="font-family:'Manrope',sans-serif; font-size:0.9rem; font-weight:300;
                color:rgba(227,224,241,0.4); max-width:480px; margin:0 auto; line-height:1.8;">
        무료로 시작하고, 더 깊은 우주로 나아가세요.<br>
        언제든지 업그레이드하거나 취소할 수 있습니다.
    </div>
</div>
""", unsafe_allow_html=True)

# ── 연간/월간 토글 ─────────────────────────────────────────────
_, toggle_col, _ = st.columns([1, 1, 1])
with toggle_col:
    annual = st.toggle("연간 결제 (2개월 무료)", value=False)

DISCOUNT = 0.167   # 연간 결제 시 약 17% 할인 (= 2개월 무료)

PLANS = [
    {
        "badge_class": "free",
        "badge_label": "무료",
        "name":        "Explorer",
        "tagline":     "우주 탐험을 시작하는 분들을 위한 기본 플랜",
        "monthly":     0,
        "features": [
            (True,  "NASA APOD 일일 탐색"),
            (True,  "AI 해설 (일 5회)"),
            (True,  "내 생일의 우주"),
            (True,  "기본 컬렉션 1개"),
            (False, "무제한 AI 해설"),
            (False, "키워드 탐색"),
            (False, "AI 챗봇 도슨트"),
            (False, "컬렉션 무제한"),
        ],
        "cta":         "무료로 시작",
        "featured":    False,
    },
    {
        "badge_class": "popular",
        "badge_label": "가장 인기",
        "name":        "Astronomer",
        "tagline":     "더 깊은 우주 탐험을 원하는 열정적인 탐험가",
        "monthly":     9900,
        "features": [
            (True,  "NASA APOD + 키워드 탐색"),
            (True,  "무제한 AI 해설"),
            (True,  "AI 챗봇 도슨트"),
            (True,  "컬렉션 무제한"),
            (True,  "내 생일의 우주"),
            (True,  "우선 응답 속도"),
            (False, "팀 공유 컬렉션"),
            (False, "교사용 수업 패키지"),
        ],
        "cta":         "Astronomer 시작",
        "featured":    True,
    },
    {
        "badge_class": "pro",
        "badge_label": "Pioneer",
        "name":        "Pioneer",
        "tagline":     "교육·연구·팀 협업을 위한 완전한 우주도서관",
        "monthly":     29900,
        "features": [
            (True,  "Astronomer 전체 포함"),
            (True,  "팀 공유 컬렉션 (최대 10인)"),
            (True,  "교사용 수업 패키지"),
            (True,  "API 접근 (Beta)"),
            (True,  "전용 고객 지원"),
            (True,  "로고 커스터마이징"),
            (True,  "우선 신기능 접근"),
            (True,  "월간 천문 리포트"),
        ],
        "cta":         "Pioneer 시작",
        "featured":    False,
    },
]

# ── 플랜 카드 ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
cols = st.columns(3, gap="medium")

for col, plan in zip(cols, PLANS):
    with col:
        monthly_price = plan["monthly"]
        if annual and monthly_price > 0:
            display_price = int(monthly_price * (1 - DISCOUNT))
            billed_note   = f"연간 {display_price * 12:,}원 청구 · 2개월 무료"
        else:
            display_price = monthly_price
            billed_note   = "매월 청구" if monthly_price > 0 else "영구 무료"

        price_str = f"₩{display_price:,}" if display_price > 0 else "₩0"
        featured_cls = "featured" if plan["featured"] else ""

        st.markdown(f"""
        <div class="plan-card {featured_cls}">
            <div>
                <span class="plan-badge {plan['badge_class']}">{plan['badge_label']}</span>
                <div class="plan-name">{plan['name']}</div>
                <div class="plan-tagline">{plan['tagline']}</div>
                <div class="plan-price">
                    <span class="plan-price-amount">{price_str}</span>
                    <span class="plan-price-unit">/ 월</span>
                </div>
                <div class="plan-price-note">{billed_note}</div>
                <hr class="plan-divider">
        """, unsafe_allow_html=True)

        for active, feat in plan["features"]:
            icon = "✦" if active else "—"
            cls  = "" if active else "inactive"
            st.markdown(f"""
                <div class="plan-feature {cls}">
                    <span class="feat-icon">{icon}</span>{feat}
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)   # .plan-card 닫기

        st.markdown("<br>", unsafe_allow_html=True)
        if plan["monthly"] == 0:
            if st.button(plan["cta"], key=f"cta_{plan['name']}", width='stretch'):
                st.switch_page("pages/1_explore.py")
        else:
            st.button(
                plan["cta"] + (" · 연간" if annual else " · 월간"),
                key=f"cta_{plan['name']}",
                width='stretch',
                disabled=True,   # TODO: Stripe 연동 후 활성화
            )
            st.markdown("""
            <div style="font-family:'Inter',sans-serif; font-size:0.58rem; font-weight:700;
                        letter-spacing:0.12em; text-transform:uppercase;
                        color:rgba(75,68,82,0.6); text-align:center; margin-top:4px;">
                결제 준비 중 · Coming Soon
            </div>
            """, unsafe_allow_html=True)

# ── 비교표 요약 ───────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">플랜 비교</div>', unsafe_allow_html=True)

compare_rows = [
    ("NASA APOD 탐색",     "✦", "✦", "✦"),
    ("AI 해설",            "일 5회", "무제한", "무제한"),
    ("키워드 탐색",         "—", "✦", "✦"),
    ("AI 챗봇 도슨트",      "—", "✦", "✦"),
    ("컬렉션",              "1개", "무제한", "무제한"),
    ("팀 공유",             "—", "—", "✦ (10인)"),
    ("교사용 패키지",        "—", "—", "✦"),
    ("API 접근",            "—", "—", "✦ Beta"),
]

header_col, e_col, a_col, p_col = st.columns([2, 1, 1, 1])
for label, text, align, color in [
    ("기능", "Explorer", "Astronomer", "Pioneer"),
]:
    header_col.markdown(f'<div style="font-family:Inter,sans-serif;font-size:0.58rem;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:rgba(156,240,255,0.35);padding:8px 0;">{label}</div>', unsafe_allow_html=True)
    e_col.markdown(f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.75rem;font-weight:600;color:rgba(227,224,241,0.5);padding:8px 0;text-align:center;">{text}</div>', unsafe_allow_html=True)
    a_col.markdown(f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.75rem;font-weight:700;color:#cebdff;padding:8px 0;text-align:center;">{align}</div>', unsafe_allow_html=True)
    p_col.markdown(f'<div style="font-family:Space Grotesk,sans-serif;font-size:0.75rem;font-weight:600;color:rgba(255,225,109,0.7);padding:8px 0;text-align:center;">{color}</div>', unsafe_allow_html=True)

st.markdown('<hr style="border-color:rgba(75,68,82,0.15);">', unsafe_allow_html=True)

for feat, e_val, a_val, p_val in compare_rows:
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    c1.markdown(f'<div style="font-family:Manrope,sans-serif;font-size:0.8rem;color:rgba(204,196,207,0.6);padding:7px 0;">{feat}</div>', unsafe_allow_html=True)
    for col, val, color in [
        (c2, e_val, "rgba(204,196,207,0.45)"),
        (c3, a_val, "#cebdff" if val != "—" else "rgba(75,68,82,0.5)"),
        (c4, p_val, "rgba(255,225,109,0.65)" if val != "—" else "rgba(75,68,82,0.5)"),
    ]:
        col.markdown(f'<div style="font-family:Inter,sans-serif;font-size:0.78rem;font-weight:600;color:{color};padding:7px 0;text-align:center;">{val}</div>', unsafe_allow_html=True)

# ── FAQ ───────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">자주 묻는 질문</div>', unsafe_allow_html=True)

faqs = [
    ("언제든지 취소할 수 있나요?",
     "네. 구독은 언제든지 취소할 수 있으며, 취소 후에도 현재 결제 기간이 끝날 때까지 서비스를 이용할 수 있습니다."),
    ("연간 결제 시 어떻게 절약되나요?",
     "연간 플랜은 월간 플랜 대비 2개월치 비용이 무료입니다. 연간 요금은 한 번에 청구됩니다."),
    ("Explorer 무료 플랜에서 업그레이드하면 기존 데이터는 유지되나요?",
     "네. 업그레이드해도 기존 컬렉션과 북마크는 모두 유지됩니다."),
    ("결제는 어떤 방법을 지원하나요?",
     "카드 결제를 지원할 예정입니다 (Stripe 연동). 현재 결제 기능은 준비 중입니다."),
]

for q, a in faqs:
    st.markdown(f"""
    <div class="faq-item">
        <div class="faq-q">Q. {q}</div>
        <div class="faq-a">{a}</div>
    </div>
    """, unsafe_allow_html=True)

render_footer()
