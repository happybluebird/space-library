# ============================================================
# pages/2_collection.py  v5.2
# user.id → user["id"] 딕셔너리 접근 방식으로 수정
# ============================================================

import html
import streamlit as st
from modules.styles     import inject_global_css
from modules.components import render_footer, render_empty_state, render_navbar
from modules.db_handler import get_bookmarks, get_collections, delete_bookmark
from modules.state      import init_session_state

st.set_page_config(page_title="컬렉션 · Space Library", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")
inject_global_css()
init_session_state()

user    = st.session_state.user
user_id = user["id"] if isinstance(user, dict) else getattr(user, "id", "guest")

render_navbar()

# ── 인라인 컬렉션 필터 ────────────────────────────────────────
filter_col = None
if user_id != "guest":
    collections, _ = get_collections(user_id)
    if collections:
        all_opt = "📋 전체 보기"
        _, fc = st.columns([3, 1])
        with fc:
            selected = st.selectbox("컬렉션 필터", [all_opt] + collections, label_visibility="collapsed")
            filter_col = None if selected == all_opt else selected


# ── 메인 ─────────────────────────────────────────────────────
st.markdown("""
<div style="padding:28px 0 20px;">
    <div style="font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:700;
                letter-spacing:0.3em; text-transform:uppercase;
                color:rgba(156,240,255,0.45); margin-bottom:10px;">◈ My Star System</div>
    <div style="font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700;
                color:#e3e0f1; letter-spacing:-0.02em; margin-bottom:4px;">나의 컬렉션</div>
    <div style="font-family:'Manrope',sans-serif; font-size:0.85rem; font-weight:300;
                color:rgba(227,224,241,0.4);">저장한 우주 기록을 관리하세요.</div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# guest 차단
if user_id == "guest":
    render_empty_state("🔒", "로그인이 필요합니다.", "사이드바에서 로그인 후 이용해주세요.")
    render_footer()
    st.stop()

# 북마크 로드
filter_col = locals().get("filter_col", None)
bookmarks, err = get_bookmarks(user_id, collection_name=filter_col)

if err:
    st.error(err)
    render_footer()
    st.stop()

if not bookmarks:
    render_empty_state("🌌", "저장된 천체가 없습니다.", "탐색 페이지에서 이미지를 저장해보세요.")
    render_footer()
    st.stop()

st.markdown(f"""
<div style="font-family:'Inter',sans-serif; font-size:0.7rem; font-weight:700;
            letter-spacing:0.1em; text-transform:uppercase;
            color:rgba(156,240,255,0.4); margin-bottom:20px;">
    Total <span style="color:#cebdff; font-size:1.1rem;">{len(bookmarks)}</span> Records
</div>
""", unsafe_allow_html=True)

# 그리드 표시
COLS = 3
for i, item in enumerate(bookmarks):
    if i % COLS == 0:
        cols = st.columns(COLS)
    with cols[i % COLS]:
        if item.get("img_url"):
            try:
                st.image(item["img_url"], width='stretch')
            except Exception:
                pass

        st.markdown(f"""
        <div style="background:rgba(27,26,38,0.55); border:1px solid rgba(75,68,82,0.1);
                    border-radius:3px; padding:14px; margin-bottom:4px;">
            <span style="font-family:'Inter',sans-serif; font-size:0.58rem; font-weight:700;
                         letter-spacing:0.18em; text-transform:uppercase; color:#9cf0ff;
                         background:rgba(156,240,255,0.08); border:1px solid rgba(156,240,255,0.18);
                         padding:2px 8px; border-radius:2px; display:inline-block; margin-bottom:8px;">
                📁 {html.escape(item['collection_name'])}
            </span><br>
            <span style="font-family:'Space Grotesk',sans-serif; font-size:0.88rem;
                         font-weight:600; color:#e3e0f1;">{html.escape(item['title'])}</span><br>
            <span style="font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:700;
                         letter-spacing:0.1em; text-transform:uppercase;
                         color:rgba(75,68,82,0.8);">{html.escape(item['created_at'][:10])}</span>
        </div>
        """, unsafe_allow_html=True)

        if item.get("ai_summary"):
            with st.expander("💬 AI 해설"):
                st.write(item["ai_summary"])

        if st.button("🗑️ 삭제", key=f"del_{item['id']}", width='stretch'):
            ok, msg = delete_bookmark(item["id"], user_id)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

render_footer()
