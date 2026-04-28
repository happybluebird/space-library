# ============================================================
# modules/nasa_handler.py  v5.2
# 반환 타입: (dict, str) 튜플 → FetchResult dataclass
# ============================================================

import datetime
import random
import requests
import streamlit as st

from modules.keys import get_nasa_key
from modules.models import FetchResult, NasaImage

APOD_URL   = "https://api.nasa.gov/planetary/apod"
SEARCH_URL = "https://images-api.nasa.gov/search"

CATEGORY_MAP = {
    "🌌 은하 (Galaxies)":                "galaxy",
    "✨ 성운 (Nebulae)":                 "nebula",
    "🪐 태양계 (Solar System)":          "solar system",
    "🌑 블랙홀 (Black Hole)":            "black hole",
    "🌟 초신성 잔해 (Supernova Remnant)": "supernova remnant",
    "🔭 심우주 관측 (Deep Field)":        "deep field",
    "☄️ 혜성/소행성 (Comets/Asteroids)":  "comet",
}

_ERR = FetchResult(data=None, error="")   # 타입 힌트용 sentinel (실제 사용 안 함)


# ── APOD: 캐시 1시간 ──────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_apod(target_date) -> FetchResult:
    try:
        nasa_key = get_nasa_key()
        if not nasa_key:
            return FetchResult(data=None, error="❌ NASA API 키가 설정되지 않았습니다. \n환경변수 NASA_KEY 또는 Streamlit secrets에 값을 추가해주세요.")
        # NASA APOD는 1~2일 지연 업로드되므로, 404/500 시 최대 3일 전까지 폴백
        target = datetime.date.fromisoformat(str(target_date))
        res = raw = None
        used_date = target
        for delta in range(4):
            candidate = target - datetime.timedelta(days=delta)
            res = requests.get(
                APOD_URL,
                params={"api_key": nasa_key, "date": str(candidate)},
                timeout=8,
            )
            if res.status_code == 200:
                used_date = candidate
                break
        res.raise_for_status()
        raw = res.json()

        if "url" not in raw:
            return FetchResult(data=None, error="해당 날짜의 관측 데이터가 없습니다.")

        return FetchResult(
            data=NasaImage(
                title=raw.get("title", "Untitled"),
                img_url=raw.get("hdurl") or raw.get("url", ""),
                description=raw.get("explanation", ""),
                media_type=raw.get("media_type", "image"),
                date=str(used_date),
                source_type="apod",
                source_id=str(used_date),
            ),
            error=None,
        )

    except requests.exceptions.Timeout:
        return FetchResult(data=None, error="⏳ NASA 서버 응답 시간 초과. 다시 시도해주세요.")
    except requests.exceptions.ConnectionError:
        return FetchResult(data=None, error="🔌 네트워크 연결을 확인해주세요.")
    except Exception as e:
        return FetchResult(data=None, error=f"❌ APOD 오류: {str(e)[:100]}")


# ── Image Library: 캐시 10분 ──────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def _fetch_items(keyword: str) -> list:
    res = requests.get(
        SEARCH_URL,
        params={"q": keyword, "media_type": "image"},
        timeout=8,
    )
    res.raise_for_status()
    return res.json().get("collection", {}).get("items", [])


def fetch_image_library(keyword: str) -> FetchResult:
    try:
        items = _fetch_items(keyword)
        if not items:
            return FetchResult(
                data=None,
                error=f"'{keyword}' 키워드로 일치하는 천체를 찾지 못했습니다.",
            )

        selected  = random.choice(items[:50])
        data_core = selected.get("data", [{}])[0]
        link_core = selected.get("links", [{}])[0]

        return FetchResult(
            data=NasaImage(
                title=data_core.get("title", "Untitled"),
                img_url=link_core.get("href", ""),
                description=data_core.get("description", ""),
                media_type="image",
                keyword=keyword,
                source_type="search",
                source_id=keyword,
            ),
            error=None,
        )

    except requests.exceptions.Timeout:
        return FetchResult(data=None, error="⏳ NASA 이미지 서버 응답 시간 초과.")
    except requests.exceptions.ConnectionError:
        return FetchResult(data=None, error="🔌 네트워크 연결을 확인해주세요.")
    except Exception as e:
        return FetchResult(data=None, error=f"❌ Image Library 오류: {str(e)[:100]}")


# ── 뱃지 ─────────────────────────────────────────────────────
BADGE_RULES = [
    (["hubble", "hst"],                           "badge-hubble",  "🔭 Hubble"),
    (["webb", "jwst"],                            "badge-webb",    "🛰 James Webb"),
    (["chandra"],                                 "badge-chandra", "🟣 Chandra"),
    (["spitzer"],                                 "badge-mars",    "🌡 Spitzer"),
    (["cassini"],                                 "badge-deep",    "🪐 Cassini"),
    (["juno"],                                    "badge-deep",    "⚡ Juno"),
    (["voyager"],                                 "badge-deep",    "🌌 Voyager"),
    (["perseverance", "curiosity", "mars rover"], "badge-mars",    "🚙 Mars Rover"),
    (["sdo", "soho", "solar dynamics", "parker"], "badge-solar",   "☀ Solar Mission"),
]


def get_badges_html(text: str) -> str:
    t = text.lower()
    badges = [
        f'<span class="{css}">{label}</span>'
        for keywords, css, label in BADGE_RULES
        if any(k in t for k in keywords)
    ]
    return " ".join(badges) if badges else '<span class="badge-generic">📡 NASA Archive</span>'
