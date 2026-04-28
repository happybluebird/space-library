# ============================================================
# modules/keys.py
# API 키를 환경변수 또는 Streamlit secrets에서 안전하게 로드
# ============================================================

import os
import streamlit as st


def _load_secret(key: str, env_var: str) -> str | None:
    if hasattr(st, "secrets"):
        try:
            value = st.secrets.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        except Exception:
            pass

    env_value = os.environ.get(env_var)
    if isinstance(env_value, str) and env_value.strip():
        return env_value.strip()

    return None


def get_nasa_key() -> str | None:
    return _load_secret("NASA_KEY", "NASA_KEY")


def get_anthropic_key() -> str | None:
    return _load_secret("ANTHROPIC_KEY", "ANTHROPIC_KEY")
