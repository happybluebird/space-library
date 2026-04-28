# ============================================================
# pages/5_stars.py  v1.0
# 별의 스펙트럼 아카이브 — OBAFGKM 분류별 별 카드
# ============================================================

import html as html_lib
import requests
import streamlit as st

from modules.styles     import inject_global_css
from modules.components import render_footer, render_navbar
from modules.state      import init_session_state

st.set_page_config(
    page_title="별 아카이브 · Space Library",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_global_css()
init_session_state()

# ── 스펙트럼 타입 정의 ─────────────────────────────────────────
SPECTRUM_INFO: dict[str, dict] = {
    "O": {"color": "#9bb0ff", "temp_range": "30,000 K+",       "temp_k": 40000, "desc": "가장 뜨겁고 밝은 청색 초거성. 수명이 수백만 년에 불과합니다."},
    "B": {"color": "#aabfff", "temp_range": "10,000~30,000 K", "temp_k": 20000, "desc": "청백색의 거대한 별. 강렬한 자외선을 방출합니다."},
    "A": {"color": "#cad7ff", "temp_range": "7,500~10,000 K",  "temp_k": 8750,  "desc": "밝은 흰색 별. 수소 흡수선이 가장 강하게 나타납니다."},
    "F": {"color": "#f8f7ff", "temp_range": "6,000~7,500 K",   "temp_k": 6750,  "desc": "황백색 별. 태양보다 약간 뜨겁고 밝습니다."},
    "G": {"color": "#fff4e8", "temp_range": "5,200~6,000 K",   "temp_k": 5778,  "desc": "노란색 왜성. 태양이 이 분류에 속합니다."},
    "K": {"color": "#ffd2a1", "temp_range": "3,700~5,200 K",   "temp_k": 4500,  "desc": "주황색 별. 태양보다 차갑고 수명이 더 깁니다."},
    "M": {"color": "#ffcc6f", "temp_range": "2,400~3,700 K",   "temp_k": 3000,  "desc": "적색 왜성. 우주에서 가장 흔한 별입니다."},
}

# ── 폴백 데이터 ───────────────────────────────────────────────
FALLBACK_STARS: dict[str, list] = {
    "O": [
        {"name": "Theta1 Orionis C", "korean": "오리온 θ¹C",    "sp_type": "O6pe", "temp_k": 45000, "distance_ly": 1344, "note": "오리온 성운을 밝히는 가장 뜨거운 별"},
        {"name": "Zeta Puppis",      "korean": "고물자리 ζ",     "sp_type": "O4If", "temp_k": 42000, "distance_ly": 1093, "note": "가장 가까운 O형 초거성 중 하나"},
    ],
    "B": [
        {"name": "Rigel",  "korean": "리겔",   "sp_type": "B8Ia",  "temp_k": 12100, "distance_ly": 860, "note": "오리온자리에서 가장 밝은 별"},
        {"name": "Spica",  "korean": "스피카", "sp_type": "B1III", "temp_k": 25300, "distance_ly": 250, "note": "처녀자리의 1등성, 쌍성계"},
    ],
    "A": [
        {"name": "Sirius", "korean": "시리우스", "sp_type": "A1V",  "temp_k": 9940, "distance_ly": 9,  "note": "밤하늘에서 가장 밝은 별"},
        {"name": "Vega",   "korean": "직녀성",   "sp_type": "A0Va", "temp_k": 9602, "distance_ly": 25, "note": "직녀성, 거문고자리 알파별"},
    ],
    "F": [
        {"name": "Procyon", "korean": "프로키온", "sp_type": "F5IV", "temp_k": 6530, "distance_ly": 11,  "note": "작은개자리 알파별, 태양계 근처"},
        {"name": "Canopus", "korean": "카노푸스", "sp_type": "F0II", "temp_k": 7350, "distance_ly": 310, "note": "남반구에서 가장 밝은 별"},
    ],
    "G": [
        {"name": "Sun",      "korean": "태양",       "sp_type": "G2V", "temp_k": 5778, "distance_ly": 0,  "note": "우리 태양계의 중심별"},
        {"name": "Tau Ceti", "korean": "고래자리 τ", "sp_type": "G8V", "temp_k": 5344, "distance_ly": 12, "note": "지구형 행성 보유 가능성이 높은 별"},
    ],
    "K": [
        {"name": "Arcturus",  "korean": "아크투루스", "sp_type": "K1.5IIIFe", "temp_k": 4286, "distance_ly": 37, "note": "북반구에서 가장 밝은 별"},
        {"name": "Aldebaran", "korean": "알데바란",   "sp_type": "K5III",     "temp_k": 3910, "distance_ly": 65, "note": "황소자리 알파별, 붉은 거성"},
    ],
    "M": [
        {"name": "Proxima Centauri", "korean": "프록시마 센타우리", "sp_type": "M5.5Ve", "temp_k": 3042, "distance_ly": 4,   "note": "태양에서 가장 가까운 별"},
        {"name": "Betelgeuse",       "korean": "베텔게우스",        "sp_type": "M1Ia",   "temp_k": 3500, "distance_ly": 700, "note": "초신성 폭발을 앞둔 오리온자리 어깨별"},
    ],
}


# ── Simbad API (ADQL) ─────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_simbad_stars(sp_type: str) -> list:
    query = (
        f"SELECT TOP 10 main_id, sp_type, fe_h_teff, plx_value, ra, dec "
        f"FROM basic "
        f"WHERE sp_type LIKE '{sp_type}%' "
        f"AND fe_h_teff IS NOT NULL "
        f"AND plx_value IS NOT NULL "
        f"AND plx_value > 0 "
        f"ORDER BY plx_value DESC"
    )
    try:
        resp = requests.get(
            "http://simbad.u-strasbg.fr/simbad/sim-tap/sync",
            params={"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "json", "QUERY": query},
            timeout=10,
        )
        resp.raise_for_status()
        payload = resp.json()
        cols = [c["name"] for c in payload["metadata"]]
        stars = []
        for row in payload["data"]:
            d = dict(zip(cols, row))
            plx = d.get("plx_value")
            dist = round(3261.56 / plx) if plx and plx > 0 else None
            sp = (d.get("sp_type") or "").strip()
            sp_key = sp[0] if sp and sp[0] in SPECTRUM_INFO else sp_type
            teff = d.get("fe_h_teff")
            temp = round(teff) if teff is not None else SPECTRUM_INFO[sp_key]["temp_k"]
            stars.append({
                "name":        (d.get("main_id") or "").lstrip("* ").strip(),
                "korean":      "",
                "sp_type":     sp or sp_type,
                "temp_k":      temp,
                "distance_ly": dist,
                "note":        SPECTRUM_INFO[sp_key]["desc"],
                "ra":          d.get("ra"),
                "dec":         d.get("dec"),
            })
        return stars or FALLBACK_STARS[sp_type]
    except Exception:
        return FALLBACK_STARS[sp_type]


# ── Aladin HiPS 이미지 ────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_aladin_image(ra: float | None, dec: float | None) -> str | None:
    """Aladin HiPS2FITS API로 DSS2 컬러 이미지 URL 조회.
    requests.head()로 유효성 확인 후 반환. 실패 시 None.
    HEAD가 405인 경우 GET(stream) 으로 재시도해 서버 가용성을 확인한다.
    """
    if ra is None or dec is None:
        return None

    url = (
        "https://alasky.cds.unistra.fr/hips-image-services/hips2fits"
        f"?hips=DSS2+color&ra={ra}&dec={dec}"
        "&fov=0.08&width=300&height=300&projection=TAN&format=jpg"
    )
    try:
        head = requests.head(url, timeout=6, allow_redirects=True)
        if head.status_code == 200 and "image" in head.headers.get("content-type", ""):
            return url
        # HEAD를 지원하지 않는 경우(405 등) GET+stream 으로 재확인
        if head.status_code in (405, 501):
            resp = requests.get(url, timeout=8, stream=True)
            ct = resp.headers.get("content-type", "")
            resp.close()
            if resp.status_code == 200 and "image" in ct:
                return url
    except Exception:
        pass
    return None


render_navbar()

# ── 헤더 ─────────────────────────────────────────────────────
st.markdown("""
<div style="padding:16px 0 12px;">
    <div style="font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:700;
                letter-spacing:0.3em; text-transform:uppercase;
                color:rgba(156,240,255,0.45); margin-bottom:8px;">⭐ Stellar Spectrum Archive</div>
    <div style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:700;
                color:#e3e0f1; letter-spacing:-0.02em;">별의 스펙트럼 아카이브</div>
    <div style="font-family:'Manrope',sans-serif; font-size:0.85rem; font-weight:300;
                color:rgba(227,224,241,0.4); margin-top:6px;">
        OBAFGKM — 별의 온도와 색이 만들어내는 우주의 팔레트
    </div>
</div>
""", unsafe_allow_html=True)

# ── 스펙트럼 타입 색상 바 ─────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
bar_cols = st.columns(7, gap="small")
for col, (sp_key, info) in zip(bar_cols, SPECTRUM_INFO.items()):
    c = info["color"]
    with col:
        st.markdown(f"""
        <div style="background:rgba(18,15,32,0.7); border:1px solid {c}33;
                    border-top:2px solid {c}; border-radius:3px;
                    padding:10px 6px; text-align:center;">
            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.15rem;
                        font-weight:700; color:{c}; margin-bottom:3px;">{sp_key}</div>
            <div style="font-family:'Inter',sans-serif; font-size:0.5rem; font-weight:700;
                        letter-spacing:0.08em; color:rgba(204,196,207,0.4);
                        white-space:nowrap;">{info["temp_range"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── 필터 ─────────────────────────────────────────────────────
ALL_TYPES = list(SPECTRUM_INFO.keys())
selected_type: str = st.radio(
    "스펙트럼 필터",
    ["ALL"] + ALL_TYPES,
    horizontal=True,
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)

# ── 데이터 로드 ───────────────────────────────────────────────
display_types = ALL_TYPES if selected_type == "ALL" else [selected_type]

all_stars: list[tuple[str, dict]] = []
with st.spinner("🌟 별 데이터를 불러오는 중..."):
    for sp_type in display_types:
        for star in fetch_simbad_stars(sp_type):
            all_stars.append((sp_type, star))

if not all_stars:
    st.info("별 데이터를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.")
    render_footer()
    st.stop()

# ── 카드 그리드 (3열) ─────────────────────────────────────────
GRID_COLS = 3
grid_cols = None

for i, (sp_type, star) in enumerate(all_stars):
    if i % GRID_COLS == 0:
        grid_cols = st.columns(GRID_COLS, gap="small")

    info = SPECTRUM_INFO[sp_type]
    c    = info["color"]

    with grid_cols[i % GRID_COLS]:
        # 별 이미지 — Aladin HiPS2FITS DSS2 → 스펙트럼 배경 폴백
        ra  = star.get("ra")
        dec = star.get("dec")
        with st.spinner(""):
            img_url = fetch_aladin_image(ra, dec)

        if img_url:
            aladin_href = (
                f"https://aladin.cds.unistra.fr/AladinLite/"
                f"?target={ra}+{dec}&fov=0.1"
            )
            # 출처 표기 (이미지 상단)
            st.markdown(
                '<div style="font-family:\'Inter\',sans-serif; font-size:0.48rem;'
                'font-weight:600; letter-spacing:0.09em; text-transform:uppercase;'
                'color:rgba(156,240,255,0.32); margin-bottom:3px;">'
                'Aladin DSS2 &middot; ESA/CDS</div>',
                unsafe_allow_html=True,
            )
            # 클릭 시 Aladin Lite 연결
            try:
                st.markdown(
                    f'<a href="{aladin_href}" target="_blank" rel="noopener noreferrer"'
                    f' style="display:block; margin-bottom:2px;">'
                    f'<img src="{img_url}" alt="{html_lib.escape(star["name"])}"'
                    f' style="width:100%; border-radius:3px; display:block;'
                    f' border:1px solid {c}22;" /></a>',
                    unsafe_allow_html=True,
                )
                img_url = img_url  # 성공 플래그 유지
            except Exception:
                img_url = None

        if not img_url:
            # 폴백: 스펙트럼 색상 배경 + ★
            st.markdown(
                f'<div style="background:radial-gradient(circle at 50% 50%,'
                f'{c}40 0%, rgba(10,8,20,0.95) 70%);'
                f'border:1px solid {c}44; border-radius:3px;'
                f'height:140px; display:flex; align-items:center;'
                f'justify-content:center; margin-bottom:2px;">'
                f'<span style="font-size:3.5rem; color:{c}; opacity:0.75;'
                f'line-height:1;">&#9733;</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        # 카드 정보
        name_esc   = html_lib.escape(star["name"])
        korean_esc = html_lib.escape(star.get("korean", ""))
        sp_esc     = html_lib.escape(star["sp_type"])
        note_esc   = html_lib.escape(star["note"])
        temp_str   = f"{star['temp_k']:,} K"
        dist_val   = star.get("distance_ly")
        if dist_val is None:
            dist_str = "—"
        elif dist_val == 0:
            dist_str = "0.000016 광년"   # 태양
        else:
            dist_str = f"{dist_val:,} 광년"

        korean_span = (
            f'<span style="color:rgba(156,240,255,0.5); font-size:0.76rem;"> · {korean_esc}</span>'
            if korean_esc else ""
        )

        # 빈 줄 없이 한 HTML 블록으로 구성 — 빈 줄이 있으면 마크다운 파서가
        # HTML 블록을 중간에 종료시켜 내부 태그가 텍스트로 노출되는 버그 발생
        st.markdown(
            f'<div style="background:linear-gradient(160deg, rgba(18,15,32,0.75) 0%, {c}0a 100%);'
            f'border:1px solid {c}28; border-left:2px solid {c}99;'
            f'border-radius:0 4px 4px 0; padding:16px 18px; margin-bottom:20px;">'
            f'<div style="margin-bottom:10px;">'
            f'<span style="font-family:\'Inter\',sans-serif; font-size:0.55rem; font-weight:700;'
            f'letter-spacing:0.2em; text-transform:uppercase;'
            f'color:{c}; background:{c}18; border:1px solid {c}44;'
            f'padding:2px 9px; border-radius:2px; display:inline-block;">'
            f'{sp_type}형 · {sp_esc}</span></div>'
            f'<div style="font-family:\'Space Grotesk\',sans-serif; font-size:0.95rem; font-weight:700;'
            f'color:#e3e0f1; letter-spacing:-0.01em; margin-bottom:5px;">'
            f'{name_esc}{korean_span}</div>'
            f'<div style="font-family:\'Manrope\',sans-serif; font-size:0.78rem; font-weight:300;'
            f'color:rgba(227,224,241,0.5); line-height:1.65; margin-bottom:14px;">'
            f'{note_esc}</div>'
            f'<div style="display:flex; gap:20px; font-family:\'Inter\',sans-serif;'
            f'font-size:0.58rem; font-weight:700; letter-spacing:0.12em;'
            f'text-transform:uppercase; border-top:1px solid {c}1a; padding-top:10px;">'
            f'<span><span style="color:rgba(156,240,255,0.3);">온도&nbsp;</span>'
            f'<span style="color:{c};">{temp_str}</span></span>'
            f'<span><span style="color:rgba(156,240,255,0.3);">거리&nbsp;</span>'
            f'<span style="color:rgba(204,196,207,0.55);">{dist_str}</span></span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

render_footer()
