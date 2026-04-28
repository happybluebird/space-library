# ============================================================
# modules/state.py
# 세션 상태 중앙 초기화
# ============================================================

from collections import deque
import streamlit as st

_DEFAULTS: dict = {
    "user":           {"id": "guest", "email": "guest"},
    "explore_count":  0,
    "history":        deque(maxlen=20),
    "explore_result": None,
    "ai_text":        "",
    "chat_messages":  [],
    "bday_result":    None,
    "bday_message":   None,
    "bday_date":      None,
}


def init_session_state() -> None:
    for key, default in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default
