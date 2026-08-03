from pathlib import Path
import streamlit as st


def load_theme():
    css_file = Path(__file__).parent / "main.css"

    css = css_file.read_text()

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )
