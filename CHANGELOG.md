# 우주도서관 (Space Library) — 작업 이력

## 프로젝트 개요
NASA Open API + Claude AI 기반 우주 기록 보관소.  
Streamlit + Supabase + Anthropic API로 구성된 완전 무료 스택 웹앱.

---

## 작업 목록

### 🔐 보안 수정
- **API 키 노출 제거** (`modules/ai_handler.py`)  
  `st.secrets["sk-ant-api03-..."]` → `st.secrets["ANTHROPIC_KEY"]`로 교체  
  소스코드에 하드코딩된 Anthropic API 키 제거

- **XSS 취약점 수정** (전체 5개 파일)  
  `html.escape()` 19곳 적용  
  대상: `result.title`, `result.source_id`, `item['title']`, `item['collection_name']`, `msg['content']` 등 HTML 삽입 변수 전체

- **secrets.toml 구성**  
  `ANTHROPIC_KEY`, `NASA_KEY`, `GEMINI_KEY`, `SUPABASE_URL`, `SUPABASE_KEY` 키 정리

---

### 🐛 버그 수정
- **SSL 인증서 오류** — `urllib` → `requests` 교체 (`certifi` 자동 처리)
- **`use_container_width` deprecated** 경고 — `width='stretch'` / `width='content'`로 전체 교체 (7곳)
- **`switch_page` 이모지 경로 버그** — 파일명에서 이모지 제거  
  `1_🔭_탐색.py` → `1_탐색.py`, `2_📚_컬렉션.py` → `2_컬렉션.py`
- **사이드바 깜빡임** — `initial_sidebar_state="expanded"` → `"collapsed"` + 상단 navbar로 교체

---

### ✨ 신규 페이지

#### `pages/3_chat.py` — AI 도슨트 챗봇
- 탐색한 천체 사진을 기반으로 Claude와 멀티턴 대화
- 이미지 + 배지 패널 / 채팅 말풍선 UI
- 대화 초기화 버튼

#### `pages/3_birthday.py` — 내 생일의 우주
- 생년월일 입력 → NASA APOD 사진 호출 (1995-06-16 이후)
- Claude AI가 생일 메시지 + 천체 해설 2파트 생성
- SNS 공유용 카드 레이아웃
- 클립보드 복사 공유 버튼 (JS `navigator.clipboard`)

#### `pages/4_pricing.py` — 구독 플랜
- Explorer(무료) / Astronomer(₩9,900) / Pioneer(₩29,900) 3단계
- 연간 결제 토글 (17% 할인, 2개월 무료)
- 플랜 비교표 + FAQ 섹션

---

### 🏗 아키텍처 리팩터링

#### 신규 모듈
| 파일 | 역할 |
|------|------|
| `modules/enums.py` | `SearchMode` Enum — 매직 스트링 분기 제거 |
| `modules/models.py` | `NasaImage`, `FetchResult` dataclass |
| `modules/styles.py` | 전역 CSS (`inject_global_css`) |
| `modules/components.py` | UI 컴포넌트 (`render_navbar`, `render_footer`, `render_empty_state`, `render_solar_monitor`) |
| `modules/state.py` | 세션 상태 중앙 초기화 (`init_session_state`) |

#### 변경된 모듈
- **`modules/ui_components.py`** → `styles.py` + `components.py`로 분리 후 **삭제**
- **`modules/nasa_handler.py`** — 반환 타입 `(dict, str)` 튜플 → `FetchResult` dataclass
- **`modules/ai_handler.py`** — `st.secrets` 의존성 제거, `api_key` 파라미터로 주입
- **`modules/state.py`** — `history` 타입을 `list` → `collections.deque(maxlen=20)` 교체 (수동 `pop(0)` 제거)
- **`modules/db_handler.py`** — `track_referral()` 함수 추가

#### 검색 모드 Enum 적용 (`pages/1_탐색.py`)
```python
# Before
if search_mode == "📅 날짜별 (APOD)":

# After
if search_mode == SearchMode.APOD:
```

---

### 🧭 UI/UX 개선

#### 상단 네비게이션 바 (전체 페이지)
- 사이드바 완전 제거 → 상단 `render_navbar()` 컴포넌트 적용
- 페이지 링크: 홈 · 탐색 · 생일의 우주 · AI 도슨트 · 구독 플랜
- Streamlit 사이드바 토글 버튼 CSS로 숨김

#### `app.py` 홈 화면
- CTA 버튼 3개: 탐사 시작하기 / 내 컬렉션 / 내 생일의 우주
- 최근 탐색 기록 5개 홈 화면 인라인 표시

#### `pages/1_탐색.py`
- 검색 컨트롤(모드 선택, 날짜/키워드, Expert 토글)을 상단 가로 행으로 이동

#### `pages/2_컬렉션.py`
- 컬렉션 필터를 우측 상단 드롭다운으로 이동

---

### 🌐 배포 설정

#### `.streamlit/config.toml` 신규 생성
```toml
[server]
headless = true
enableXsrfProtection = true

[theme]
base = "dark"
backgroundColor = "#0a0814"
primaryColor = "#cebdff"
```

#### `requirements.txt` 최신화
```
streamlit>=1.45.0
anthropic>=0.49.0
requests>=2.32.0
supabase>=2.10.0
```

---

### 📊 추천(Referral) 추적
- `?ref=CODE` URL 파라미터 파싱 → Supabase `referrals` 테이블 저장
- `modules/db_handler.py` — `track_referral()` 추가
- `schema.sql` — `referrals` 테이블 + RLS 정책 + 인덱스 추가
- `app.py` — 첫 방문 시 1회만 기록 (세션 플래그)

---

## 최종 파일 구조

```
space_library/
├── app.py                    ← 홈 + 상단 navbar
├── requirements.txt
├── schema.sql                ← bookmarks + referrals 테이블
├── CHANGELOG.md              ← 이 파일
├── .streamlit/
│   ├── secrets.toml          ← API 키 (Git 제외)
│   └── config.toml           ← 배포 설정
├── modules/
│   ├── enums.py              ← SearchMode Enum
│   ├── models.py             ← NasaImage, FetchResult dataclass
│   ├── styles.py             ← 전역 CSS
│   ├── components.py         ← render_navbar, render_footer 등
│   ├── state.py              ← init_session_state (deque)
│   ├── nasa_handler.py       ← NASA API (FetchResult 반환)
│   ├── ai_handler.py         ← Claude API (api_key 주입)
│   └── db_handler.py         ← Supabase CRUD + track_referral
└── pages/
    ├── 1_탐색.py              ← NASA 탐색 + AI 해설
    ├── 2_컬렉션.py            ← 북마크 관리
    ├── 3_birthday.py         ← 내 생일의 우주
    ├── 3_chat.py             ← AI 도슨트 챗봇
    └── 4_pricing.py          ← 구독 플랜
```

---

## 실행 방법

```bash
# 로컬 실행
python3 -m streamlit run app.py

# secrets.toml 위치
.streamlit/secrets.toml
```

```toml
# .streamlit/secrets.toml
NASA_KEY       = "..."
ANTHROPIC_KEY  = "..."
SUPABASE_URL   = "https://xxxx.supabase.co"
SUPABASE_KEY   = "eyJ..."
```
