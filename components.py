import streamlit as st

with open("assets/logo.svg", "r") as f:
    svg = f.read()
logo_component = st.components.v2.component(
    name="logo",
    html=f'<div style="width:360px">{svg.replace("#1e293b","var(--st-text-color)")}</div>'
)