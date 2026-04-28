# ============================================================
# app.py  v8.0 — components.v1.html() 로 완전 재구현
# ============================================================

import datetime
import random
import requests
import streamlit as st
import streamlit.components.v1 as components
from modules.state      import init_session_state
from modules.db_handler import track_referral

st.set_page_config(
    page_title="우주도서관 · Space Library",
    page_icon="🏛",
    layout="wide",
    initial_sidebar_state="collapsed",
)

init_session_state()

_params = st.query_params
if "ref" in _params and not st.session_state.get("_ref_tracked"):
    track_referral(_params["ref"], st.session_state.user.get("id", "guest"))
    st.session_state["_ref_tracked"] = True

# ── Streamlit 기본 UI 숨김 (이것만 st.markdown 사용) ────────────
st.markdown("""
<style>
#MainMenu,header[data-testid="stHeader"],footer,
[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"],.stDeployButton{display:none!important}
.stApp,[data-testid="stAppViewContainer"]{background:#12121d!important}
.main .block-container,[data-testid="stMainBlockContainer"]{
  padding:0!important;max-width:100%!important;margin:0!important}
[data-testid="stVerticalBlock"],[data-testid="stVerticalBlockBorderWrapper"]{
  gap:0!important;padding:0!important}
.element-container{margin:0!important;padding:0!important}
iframe{display:block;border:none!important}
</style>
""", unsafe_allow_html=True)


# ── NASA 이미지 fetch ─────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def _get_img(keyword: str) -> str:
    try:
        r = requests.get(
            "https://images-api.nasa.gov/search",
            params={"q": keyword, "media_type": "image"},
            timeout=8,
        )
        items = r.json().get("collection", {}).get("items", [])
        if items:
            chosen = random.choice(items[:20])
            return chosen.get("links", [{}])[0].get("href", "")
    except Exception:
        pass
    return ""


IMG_PLANET = _get_img("planet solar system") or \
    "https://images-assets.nasa.gov/image/PIA11800/PIA11800~medium.jpg"
IMG_NEBULA = _get_img("nebula") or \
    "https://images-assets.nasa.gov/image/PIA03606/PIA03606~medium.jpg"

# ── 활동 로그 타임스탬프 ──────────────────────────────────────
_now = datetime.datetime.now()
T1 = (_now - datetime.timedelta(minutes=random.randint(5,  30))).strftime("%H:%M:%S")
T2 = (_now - datetime.timedelta(minutes=random.randint(60, 120))).strftime("%H:%M:%S")
T3 = (_now - datetime.timedelta(hours=random.randint(3,   8))).strftime("%H:%M:%S")

# ── 별빛 파티클 (30개) ────────────────────────────────────────
_rng = random.Random(42)
STARS = "".join(
    '<div style="position:absolute;left:{x}%;top:{y}%;width:{w}px;height:{w}px;'
    'background:#fff;border-radius:50%;opacity:{o};'
    'animation:twinkle {d}s {dl}s infinite linear;"></div>'.format(
        x=round(_rng.uniform(0, 100), 1),
        y=round(_rng.uniform(0, 100), 1),
        w=_rng.choice([1, 1, 2]),
        o=round(_rng.uniform(0.15, 0.9), 2),
        d=round(_rng.uniform(2, 7), 1),
        dl=round(_rng.uniform(0, 5), 1),
    )
    for _ in range(30)
)

# ── 전체 HTML 페이지 ──────────────────────────────────────────
_HTML = """<!DOCTYPE html>
<html class="dark" lang="ko">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<script>
window.tailwind={config:{
  darkMode:"class",
  theme:{extend:{
    colors:{
      "secondary-fixed":"#9cf0ff","surface-container-low":"#1b1a26",
      "on-primary-container":"#9674f8","surface-container-lowest":"#0d0d18",
      "on-background":"#e3e0f1","surface-container-high":"#292935",
      "tertiary":"#e9c400","surface":"#12121d","surface-container":"#1f1e2a",
      "outline-variant":"#4a454e","surface-variant":"#343440",
      "background":"#12121d","primary":"#cebdff","primary-container":"#2b0074",
      "on-primary":"#390094","on-surface":"#e3e0f1","primary-fixed-dim":"#cebdff",
      "on-surface-variant":"#ccc4cf","surface-bright":"#383845",
      "secondary":"#bdf4ff","surface-container-highest":"#343440",
      "error":"#ffb4ab","outline":"#958e99","primary-fixed":"#e8ddff",
      "secondary-container":"#00e3fd"
    },
    fontFamily:{"headline":["Space Grotesk"],"body":["Manrope"],"label":["Inter"]},
    borderRadius:{"DEFAULT":"0.125rem","lg":"0.25rem","xl":"0.5rem","full":"0.75rem"}
  }}
}};
</script>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Manrope:wght@200;300;400;500;600;700&family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet"/>
<style>
.material-symbols-outlined{
  font-family:'Material Symbols Outlined';
  font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 24;
  font-style:normal;line-height:1;display:inline-block;
}
body{background:#12121d;color:#e3e0f1;font-family:'Manrope',sans-serif;
     overflow-x:hidden;margin:0;padding:0;}
.nebula-glow{
  background:radial-gradient(circle at 50% 50%,#2b0074 0%,#12121d 70%);
}
@keyframes twinkle{
  0%,100%{opacity:0.1} 50%{opacity:1}
}
@keyframes status-pulse{
  0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(.85)}
}
.status-dot{animation:status-pulse 2s cubic-bezier(.4,0,.6,1) infinite;}
a{text-decoration:none;}
</style>
</head>
<body class="dark selection:bg-primary/30 selection:text-primary">

<!-- ── 네비게이션 ─────────────────────────────────────────── -->
<nav class="sticky top-0 z-50 flex justify-between items-center w-full px-8 py-4
            bg-[#1b1a26]/60 backdrop-blur-xl font-['Space_Grotesk'] tracking-tight"
     style="border-bottom:1px solid rgba(74,69,78,.12);">
  <div class="text-2xl font-bold tracking-tighter text-[#cebdff]">우주도서관</div>
  <div class="flex items-center gap-8">
    <a class="text-[#cebdff] border-b-2 border-[#cebdff] pb-1 font-bold"
       href="/" target="_parent">Lobby</a>
    <a class="text-[#bdf4ff]/70 hover:text-[#cebdff] transition-colors"
       href="/1_explore" target="_parent">Archive</a>
    <a class="text-[#bdf4ff]/70 hover:text-[#cebdff] transition-colors"
       href="/2_collection" target="_parent">My Star System</a>
  </div>
  <div class="flex items-center gap-6">
    <div class="relative hidden lg:block">
      <input class="bg-[#0d0d18] border border-[#4a454e]/30 text-[#cebdff]
                    placeholder:text-[#cebdff]/30 rounded-lg px-4 py-1.5 w-64
                    focus:outline-none focus:ring-1 focus:ring-[#cebdff]
                    font-['Space_Grotesk'] text-sm"
             placeholder="Search the void..." type="text"/>
      <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2
                   text-[#cebdff]/50" style="font-size:16px;">search</span>
    </div>
    <button class="hover:bg-[#292935]/50 transition-all p-2 rounded-full
                   border-none bg-transparent cursor-pointer">
      <span class="material-symbols-outlined text-[#cebdff]">account_circle</span>
    </button>
  </div>
</nav>

<!-- ── 히어로 ─────────────────────────────────────────────── -->
<section class="nebula-glow relative flex items-center justify-center
                overflow-hidden px-8" style="min-height:921px;">
  <!-- 글로우 블롭 -->
  <div class="absolute inset-0 z-0 pointer-events-none">
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px]
                bg-primary/10 rounded-full blur-[120px]"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[400px] h-[400px]
                bg-secondary/10 rounded-full blur-[100px]"></div>
  </div>
  <!-- 별빛 파티클 -->
  <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
    PLACEHOLDER_STARS
  </div>
  <!-- 콘텐츠 -->
  <div class="relative z-10 text-center max-w-5xl mx-auto">
    <div class="inline-flex items-center gap-2 mb-6 px-3 py-1
                bg-[#292935]/50 border border-[#4a454e]/15 rounded-full">
      <span class="status-dot inline-block w-2 h-2 rounded-full bg-[#bdf4ff]"></span>
      <span class="font-['Inter'] text-[10px] uppercase tracking-[.2em] text-[#9cf0ff]">
        System Status: Active
      </span>
    </div>
    <h1 class="font-['Space_Grotesk'] font-bold tracking-tighter
               text-[#e3e0f1] mb-8 leading-[1.1]"
        style="font-size:clamp(2.5rem,6.5vw,5rem);">
      우주도서관:
      <span class="text-transparent bg-clip-text
                   bg-gradient-to-r from-[#cebdff] via-[#bdf4ff] to-[#e8ddff]">
        나만의 우주 정보 도서관
      </span>
    </h1>
    <p class="font-['Manrope'] text-lg text-[#ccc4cf] max-w-2xl mx-auto mb-12
              font-light tracking-wide opacity-80">
      심우주의 지식을 탐험하고 보관하는 중앙 아카이브.<br/>
      고대 성단부터 붕괴하는 블랙홀까지, 우주의 모든 기록이 이곳에서 시작됩니다.
    </p>
    <div class="flex flex-wrap justify-center gap-4">
      <a href="/1_explore" target="_parent"
         class="px-8 py-4 bg-gradient-to-r from-[#cebdff] to-[#9674f8]
                text-[#390094] font-bold rounded-md hover:opacity-90
                transition-all flex items-center gap-2 font-['Space_Grotesk']">
        <span class="material-symbols-outlined" style="font-size:20px;font-variation-settings:'FILL' 1,'wght' 400,'GRAD' 0,'opsz' 24;">auto_awesome</span>
        ✦ 탐사 시작하기
      </a>
      <a href="/2_collection" target="_parent"
         class="px-8 py-4 border border-[#4a454e]/30 text-[#cebdff] font-bold
                rounded-md hover:bg-[#383845]/20 transition-all font-['Space_Grotesk']">
        내 세계 확인
      </a>
    </div>
  </div>
  <!-- 좌측 하단 좌표 -->
  <div class="absolute bottom-12 left-12 hidden lg:block font-['Inter']
              text-[10px] text-[#cebdff]/40 leading-relaxed uppercase tracking-[.15em]">
    COORD: 48.1516 / 23.42<br/>
    REF-SYS: ARCHIVE-DELTA-V<br/>
    SIGNAL: STABLE
  </div>
</section>

<!-- ── 카테고리 벤토 그리드 ────────────────────────────────── -->
<section class="py-24 px-8 max-w-7xl mx-auto">
  <div class="flex flex-col md:flex-row justify-between items-end mb-16 gap-6">
    <div>
      <h2 class="font-['Space_Grotesk'] text-4xl font-bold text-[#e3e0f1] mb-4">
        주요 보관 카테고리
      </h2>
      <p class="font-['Manrope'] text-[#ccc4cf] max-w-md leading-relaxed">
        아카이브의 방대한 데이터가 실시간으로 동기화되고 있습니다.
        탐사할 대상을 선택하십시오.
      </p>
    </div>
    <a href="/1_explore" target="_parent"
       class="font-['Inter'] text-[11px] text-[#bdf4ff] tracking-widest
              border-b border-[#bdf4ff]/30 pb-1 hover:text-[#cebdff] transition-colors">
      전체 보관소 탐색하기 →
    </a>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-4 gap-6"
       style="grid-template-rows:340px 340px;">

    <!-- 행성 (2×2) -->
    <div class="md:col-span-2 md:row-span-2 group relative overflow-hidden
                rounded-xl bg-[#1b1a26] p-8 flex flex-col justify-end cursor-pointer">
      <img src="PLACEHOLDER_PLANET" alt="Planets"
           class="absolute inset-0 w-full h-full object-cover opacity-50
                  group-hover:scale-105 transition-transform duration-700"/>
      <div class="absolute inset-0 bg-gradient-to-t from-[#0d0d18]
                  via-[#1b1a26]/40 to-transparent"></div>
      <div class="relative z-10">
        <span class="font-['Inter'] text-[10px] text-[#bdf4ff] tracking-[.2em]
                     uppercase block mb-2">CATEGORY: CATALOG-01</span>
        <h3 class="font-['Space_Grotesk'] text-3xl font-bold text-[#e3e0f1] mb-4">
          행성 (Planets)
        </h3>
        <p class="font-['Manrope'] text-sm text-[#ccc4cf] max-w-xs mb-6 leading-relaxed">
          암석 행성부터 가스 거인까지, 은하계 전역의 행성 환경 데이터베이스.
        </p>
        <div class="flex gap-2 flex-wrap">
          <span class="px-2 py-1 bg-[#00e3fd]/20 text-[#9cf0ff]
                       font-['Inter'] text-[10px] rounded-sm">1,402 ENTRIES</span>
          <span class="px-2 py-1 bg-[#343440]/40 text-[#ccc4cf]
                       font-['Inter'] text-[10px] rounded-sm">UPDATED 2H AGO</span>
        </div>
      </div>
    </div>

    <!-- 성운 (2×1) -->
    <div class="md:col-span-2 md:row-span-1 group relative overflow-hidden
                rounded-xl bg-[#1b1a26] p-8 flex items-center cursor-pointer">
      <img src="PLACEHOLDER_NEBULA" alt="Nebula"
           class="absolute inset-0 w-full h-full object-cover opacity-40
                  group-hover:scale-105 transition-transform duration-700"/>
      <div class="absolute inset-0 bg-gradient-to-r from-[#0d0d18]/80
                  to-transparent"></div>
      <div class="relative z-10">
        <h3 class="font-['Space_Grotesk'] text-2xl font-bold text-[#e3e0f1] mb-2">
          성운 (Nebulae)
        </h3>
        <p class="font-['Manrope'] text-xs text-[#ccc4cf] max-w-xs leading-relaxed">
          별이 탄생하는 요람, 이온화된 가스 구름의 장관을 기록합니다.
        </p>
      </div>
      <span class="material-symbols-outlined absolute right-8 bottom-8
                   text-[#cebdff]/30 group-hover:text-[#cebdff] transition-colors"
            style="font-size:3rem;">cloud</span>
    </div>

    <!-- 블랙홀 (1×1) -->
    <div class="md:col-span-1 md:row-span-1 group relative overflow-hidden
                rounded-xl bg-[#1b1a26] p-6 flex flex-col justify-between cursor-pointer">
      <div class="absolute inset-0 bg-gradient-to-br from-[#2b0074]/20
                  to-[#12121d]"></div>
      <div class="relative z-10">
        <h3 class="font-['Space_Grotesk'] text-xl font-bold text-[#e3e0f1] mb-1">
          블랙홀
        </h3>
        <span class="font-['Inter'] text-[9px] text-[#ffb4ab]/60
                     uppercase tracking-tight">DENSITY HAZARD: HIGH</span>
      </div>
      <div class="relative z-10 mt-8">
        <div class="w-full h-1 bg-[#343440] rounded-full overflow-hidden">
          <div class="h-full w-3/4 bg-[#e9c400] rounded-full"
               style="box-shadow:0 0 8px #e9c400;"></div>
        </div>
        <span class="font-['Inter'] text-[9px] text-[#ccc4cf] block mt-2 uppercase">
          DENSITY THRESHOLD
        </span>
      </div>
    </div>

    <!-- 항성 (1×1) -->
    <div class="md:col-span-1 md:row-span-1 group relative overflow-hidden
                rounded-xl bg-[#1b1a26] p-6 flex flex-col justify-between
                border border-[#4a454e]/10 cursor-pointer">
      <div class="relative z-10">
        <h3 class="font-['Space_Grotesk'] text-xl font-bold text-[#e3e0f1] mb-1">
          항성 (Stars)
        </h3>
        <p class="font-['Manrope'] text-[10px] text-[#ccc4cf] leading-tight">
          분광형별 항성 아카이브
        </p>
      </div>
      <div class="flex flex-wrap gap-1 mt-4">
        <span class="w-6 h-6 rounded-full bg-[#93c5fd] blur-[2px] opacity-80
                     inline-block"></span>
        <span class="w-6 h-6 rounded-full bg-white blur-[2px] opacity-80
                     inline-block"></span>
        <span class="w-6 h-6 rounded-full bg-yellow-200 blur-[2px] opacity-80
                     inline-block"></span>
        <span class="w-6 h-6 rounded-full bg-orange-400 blur-[2px] opacity-80
                     inline-block"></span>
        <span class="w-6 h-6 rounded-full bg-red-500 blur-[2px] opacity-75
                     inline-block"></span>
      </div>
    </div>
  </div>
</section>

<!-- ── 실시간 아카이브 상태 ───────────────────────────────── -->
<section class="py-24 bg-[#1b1a26]/30">
  <div class="max-w-7xl mx-auto px-8 grid grid-cols-1 lg:grid-cols-3
              gap-12 items-center">
    <div class="lg:col-span-1">
      <h4 class="font-['Inter'] text-[10px] text-[#9cf0ff] tracking-[.3em]
                 uppercase mb-4">Instrumentation</h4>
      <h2 class="font-['Space_Grotesk'] text-3xl font-bold text-[#e3e0f1] mb-6">
        실시간 아카이브 상태
      </h2>
      <p class="font-['Manrope'] text-[#ccc4cf] text-sm leading-relaxed mb-8">
        우주도서관은 전 은하계의 센서 어레이로부터 데이터를 수신합니다.
        현재 데이터 처리율은 99.8%로 최적의 상태를 유지하고 있습니다.
      </p>
      <div class="space-y-4">
        <div class="flex justify-between items-center text-[10px] font-['Inter']
                    text-[#ccc4cf] uppercase tracking-widest
                    border-b border-[#4a454e]/10 pb-2">
          <span>Deep Space Signal</span>
          <span class="text-[#bdf4ff]">OPTIMAL</span>
        </div>
        <div class="flex justify-between items-center text-[10px] font-['Inter']
                    text-[#ccc4cf] uppercase tracking-widest
                    border-b border-[#4a454e]/10 pb-2">
          <span>Relay Latency</span>
          <span class="text-[#cebdff]">12MS</span>
        </div>
        <div class="flex justify-between items-center text-[10px] font-['Inter']
                    text-[#ccc4cf] uppercase tracking-widest
                    border-b border-[#4a454e]/10 pb-2">
          <span>Buffer Load</span>
          <span class="text-[#e9c400]">5.03%</span>
        </div>
      </div>
    </div>

    <div class="lg:col-span-2 relative">
      <div class="bg-[#343440] rounded-xl p-8 border border-[#4a454e]/15
                  flex flex-col justify-between overflow-hidden relative">
        <span class="material-symbols-outlined absolute top-0 right-0 p-8
                     opacity-[0.07] pointer-events-none"
              style="font-size:7rem;">analytics</span>
        <div class="flex justify-between items-start z-10 mb-8">
          <div>
            <span class="font-['Inter'] text-[10px] text-[#cebdff] uppercase
                         tracking-[.1em]">Activity Monitor</span>
            <h3 class="font-['Space_Grotesk'] text-xl font-medium text-[#e3e0f1] mt-1">
              최근 발견 로그
            </h3>
          </div>
          <div class="flex gap-2">
            <span class="w-2 h-2 rounded-full bg-[#bdf4ff] inline-block"></span>
            <span class="w-2 h-2 rounded-full bg-[#bdf4ff]/30 inline-block"></span>
            <span class="w-2 h-2 rounded-full bg-[#bdf4ff]/30 inline-block"></span>
          </div>
        </div>
        <div class="space-y-3 z-10">
          <div class="p-3 bg-[#1b1a26] rounded-lg flex items-center justify-between
                      border-l-2 border-[#bdf4ff]">
            <div class="flex items-center gap-4">
              <span class="font-['Inter'] text-[10px] text-[#ccc4cf]">PLACEHOLDER_T1</span>
              <span class="font-['Manrope'] text-xs text-[#e3e0f1]">
                안드로메다 소성단 내 신규 적색왜성 포착
              </span>
            </div>
            <span class="material-symbols-outlined text-[#bdf4ff]"
                  style="font-size:1rem;">visibility</span>
          </div>
          <div class="p-3 bg-[#1b1a26] rounded-lg flex items-center justify-between">
            <div class="flex items-center gap-4">
              <span class="font-['Inter'] text-[10px] text-[#ccc4cf]">PLACEHOLDER_T2</span>
              <span class="font-['Manrope'] text-xs text-[#e3e0f1]">
                오리온 성운 데이터 코어 백업 완료
              </span>
            </div>
            <span class="material-symbols-outlined text-[#cebdff]"
                  style="font-size:1rem;">check_circle</span>
          </div>
          <div class="p-3 bg-[#1b1a26] rounded-lg flex items-center justify-between">
            <div class="flex items-center gap-4">
              <span class="font-['Inter'] text-[10px] text-[#ccc4cf]">PLACEHOLDER_T3</span>
              <span class="font-['Manrope'] text-xs text-[#e3e0f1]">
                아카이브 델타 보안 프로토콜 갱신
              </span>
            </div>
            <span class="material-symbols-outlined text-[#ccc4cf]"
                  style="font-size:1rem;">lock</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ── 푸터 CTA ──────────────────────────────────────────── -->
<section class="py-32 px-8 text-center relative overflow-hidden">
  <div class="absolute inset-0 bg-gradient-to-b from-transparent
              via-[#cebdff]/5 to-transparent pointer-events-none"></div>
  <div class="relative z-10 max-w-2xl mx-auto">
    <h2 class="font-['Space_Grotesk'] text-4xl font-bold text-[#e3e0f1] mb-6">
      지식의 끝에서 새로운 탐험을.
    </h2>
    <p class="font-['Manrope'] text-[#ccc4cf] mb-12 leading-relaxed">
      개인용 마스터 시스템을 구축하고 발견한 모든 데이터를
      자신만의 아카이브에 영구 저장하세요.
    </p>
    <a href="/4_pricing" target="_parent"
       class="px-10 py-5 bg-[#383845] text-[#cebdff] border border-[#cebdff]/20
              hover:border-[#cebdff] transition-all font-['Space_Grotesk'] font-bold
              tracking-widest rounded-sm uppercase text-xs inline-flex items-center gap-3">
      마스터 시스템 연결 →
      <span class="material-symbols-outlined" style="font-size:1rem;">sensors</span>
    </a>
  </div>
</section>

<!-- ── 푸터 ─────────────────────────────────────────────── -->
<footer class="bg-[#12121d] w-full py-12 border-t border-[#4a454e]/15
               flex flex-col md:flex-row justify-between items-center px-12 gap-4">
  <div class="font-['Inter'] uppercase text-[10px] tracking-[.1em] text-[#9cf0ff]">
    © 2142 THE CELESTIAL ARCHIVE | COSMIC STATUS: STABLE
  </div>
  <div class="flex gap-10">
    <a class="font-['Inter'] uppercase text-[10px] tracking-[.1em]
              text-[#bdf4ff]/40 hover:text-[#cebdff] transition-colors" href="#">
      Protocol</a>
    <a class="font-['Inter'] uppercase text-[10px] tracking-[.1em]
              text-[#bdf4ff]/40 hover:text-[#cebdff] transition-colors" href="#">
      Coordinates</a>
    <a class="font-['Inter'] uppercase text-[10px] tracking-[.1em]
              text-[#bdf4ff]/40 hover:text-[#cebdff] transition-colors" href="#">
      Signal</a>
  </div>
  <div class="flex items-center gap-4">
    <span class="w-1 h-1 rounded-full bg-[#bdf4ff] inline-block"></span>
    <span class="font-['Inter'] uppercase text-[10px] tracking-[.1em]
                 text-[#bdf4ff]/40">KOR-01 SECTOR</span>
  </div>
</footer>

</body>
</html>"""

# 플레이스홀더 치환
_page = (_HTML
    .replace("PLACEHOLDER_PLANET", IMG_PLANET)
    .replace("PLACEHOLDER_NEBULA", IMG_NEBULA)
    .replace("PLACEHOLDER_STARS",  STARS)
    .replace("PLACEHOLDER_T1",     T1)
    .replace("PLACEHOLDER_T2",     T2)
    .replace("PLACEHOLDER_T3",     T3)
)

# st.components.v1.html() 로 렌더 — script/CSS 모두 실행됨
components.html(_page, height=3600, scrolling=False)
