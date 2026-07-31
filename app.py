import streamlit as st

from core.config import APP_NAME, APP_ICON
from core.session import SessionManager

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
)

SessionManager.initialize()

st.title(f"{APP_ICON} {APP_NAME}")

st.success("✅ APPA Core initialized successfully!")

st.write("Sprint 1 - Milestone 6")
