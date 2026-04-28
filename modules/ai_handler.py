# ============================================================
# modules/ai_handler.py  v5.4
# api_key를 외부에서 주입받는 구조 (st.secrets 의존성 제거)
# ============================================================

import requests


def generate_explanation(title: str, description: str, api_key: str, expert_mode: bool = False):
    if expert_mode:
        prompt = f"""NASA 수석 데이터 분석가로서 한국어로 기술 리포트를 작성하세요.
[천체]: {title}
[데이터]: {description[:800]}
1. 🧪 천체 분류  2. 🔭 관측 장비  3. 📏 물리 데이터(거리/위치)  4. 📝 심층 분석(3문장)
*톤: 수치·팩트 위주*"""
    else:
        prompt = f"""우주도서관 도슨트로서 한국어로 설명해주세요.
[사진]: {title} / {description[:800]}
1. 📰 헤드라인  2. 🛰️ 관측 이야기(망원경+3문장)  3. 🧬 핵심 요약 2가지
*톤: 관람객에게 말걸듯 부드럽게*"""

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            json={
                "model":      "claude-haiku-4-5-20251001",
                "max_tokens": 800,
                "messages":   [{"role": "user", "content": prompt}],
            },
            headers={
                "x-api-key":         api_key,
                "anthropic-version": "2023-06-01",
            },
            timeout=15,
        )

        if resp.status_code == 401:
            return None, "❌ Anthropic API 키 오류. secrets.toml의 ANTHROPIC_KEY를 확인해주세요."
        if resp.status_code == 429:
            return None, "⏳ API 한도 초과. 잠시 후 다시 시도해주세요."
        if resp.status_code != 200:
            return None, f"❌ API 오류 {resp.status_code}: {resp.text[:100]}"

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
