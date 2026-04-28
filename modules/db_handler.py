# ============================================================
# modules/db_handler.py
# 역할: Supabase 연결, 인증(로그인/회원가입), 북마크 CRUD
# 수정 포인트: Supabase URL/KEY는 .streamlit/secrets.toml에서 관리
# ============================================================

import streamlit as st
from supabase import create_client, Client
from typing import Optional


# ----------------------------------------------------------
# [내부] Supabase 클라이언트 생성 (캐싱으로 중복 연결 방지)
# ----------------------------------------------------------
@st.cache_resource
def _get_client() -> Client:
    """Supabase 클라이언트를 한 번만 생성하고 재사용합니다."""
    url  = st.secrets["SUPABASE_URL"]
    key  = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


# ----------------------------------------------------------
# [인증] 회원가입
# 반환: (성공 여부: bool, 메시지: str)
# ----------------------------------------------------------
def sign_up(email: str, password: str) -> tuple[bool, str]:
    try:
        client = _get_client()
        client.auth.sign_up({"email": email, "password": password})
        return True, "✅ 가입 완료! 이메일을 확인해 인증 후 로그인하세요."
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg:
            return False, "⚠️ 이미 가입된 이메일입니다."
        return False, f"❌ 가입 오류: {error_msg}"


# ----------------------------------------------------------
# [인증] 로그인
# 반환: (user 객체 or None, 메시지: str)
# ----------------------------------------------------------
def sign_in(email: str, password: str):
    try:
        client = _get_client()
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        return res.user, "✅ 로그인 성공!"
    except Exception as e:
        error_msg = str(e)
        if "Invalid login" in error_msg:
            return None, "❌ 이메일 또는 비밀번호가 틀렸습니다."
        return None, f"❌ 로그인 오류: {error_msg}"


# ----------------------------------------------------------
# [인증] 로그아웃
# ----------------------------------------------------------
def sign_out() -> None:
    try:
        _get_client().auth.sign_out()
    except Exception:
        pass  # 로그아웃 실패는 무시 (세션 초기화로 처리)


# ----------------------------------------------------------
# [북마크] 저장
# 반환: (성공 여부: bool, 메시지: str)
# ----------------------------------------------------------
def save_bookmark(
    user_id: str,
    title: str,
    img_url: str,
    description: str,
    ai_summary: str,
    collection_name: str = "기본 컬렉션",
    source_type: str = "",
    source_id: str = "",
) -> tuple[bool, str]:
    try:
        client = _get_client()

        # 중복 저장 방지: 같은 유저 + 같은 제목 + 같은 컬렉션
        existing = (
            client.table("bookmarks")
            .select("id")
            .eq("user_id", user_id)
            .eq("title", title)
            .eq("collection_name", collection_name)
            .execute()
        )
        if existing.data:
            return False, "⚠️ 이미 같은 컬렉션에 저장된 항목입니다."

        client.table("bookmarks").insert({
            "user_id": user_id,
            "title": title,
            "img_url": img_url,
            "description": description,
            "ai_summary": ai_summary,
            "collection_name": collection_name,
            "source_type": source_type,
            "source_id": source_id,
        }).execute()

        return True, f"✅ '{collection_name}' 컬렉션에 저장되었습니다!"
    except Exception as e:
        return False, f"❌ 저장 오류: {str(e)}"


# ----------------------------------------------------------
# [북마크] 특정 컬렉션 또는 전체 조회
# 반환: (리스트 or None, 메시지: str)
# ----------------------------------------------------------
def get_bookmarks(user_id: str, collection_name: Optional[str] = None):
    try:
        client = _get_client()
        query = (
            client.table("bookmarks")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
        )
        if collection_name:
            query = query.eq("collection_name", collection_name)

        res = query.execute()
        return res.data, None
    except Exception as e:
        return None, f"❌ 조회 오류: {str(e)}"


# ----------------------------------------------------------
# [북마크] 컬렉션 이름 목록 조회
# 반환: (컬렉션 이름 리스트, 에러 메시지 or None)
# ----------------------------------------------------------
def get_collections(user_id: str):
    try:
        client = _get_client()
        res = (
            client.table("bookmarks")
            .select("collection_name")
            .eq("user_id", user_id)
            .execute()
        )
        collections = sorted(set(item["collection_name"] for item in res.data))
        return collections, None
    except Exception as e:
        return [], f"❌ 컬렉션 조회 오류: {str(e)}"


# ----------------------------------------------------------
# [북마크] 삭제
# 반환: (성공 여부: bool, 메시지: str)
# ----------------------------------------------------------
def delete_bookmark(bookmark_id: str, user_id: str) -> tuple[bool, str]:
    try:
        _get_client().table("bookmarks").delete().eq("id", bookmark_id).eq("user_id", user_id).execute()
        return True, "🗑️ 삭제되었습니다."
    except Exception as e:
        return False, f"❌ 삭제 오류: {str(e)}"


# ----------------------------------------------------------
# [추천] URL ?ref= 파라미터 파싱 → Supabase referrals 저장
# 반환: (성공 여부: bool, ref_code: str | None)
# ----------------------------------------------------------
def track_referral(ref_code: str, visitor_user_id: str = "guest") -> tuple[bool, str]:
    """
    ?ref=CODE 파라미터를 받아 referrals 테이블에 기록합니다.
    중복 방문은 무시(upsert)합니다.
    """
    if not ref_code or not ref_code.strip():
        return False, "ref_code가 비어있습니다."
    try:
        _get_client().table("referrals").upsert({
            "ref_code":   ref_code.strip()[:64],
            "visitor_id": visitor_user_id,
        }, on_conflict="ref_code,visitor_id").execute()
        return True, ref_code
    except Exception as e:
        return False, f"❌ referral 저장 오류: {str(e)}"
