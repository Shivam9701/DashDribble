from pathlib import Path
import streamlit as st

# Inject custom CSS
def inject_css(css_file: str):
    css_path = Path(css_file)
    with open(css_path, "r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Load HTML template
def load_template(template_file: str):
    template_path = Path(template_file)
    with open(template_path, "r") as f:
        return f.read()
