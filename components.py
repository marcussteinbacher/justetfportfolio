import streamlit as st

with open("assets/logo.svg", "r") as f:
    svg = f.read()

logo_css = """
.logo {
    width: 100%;
    max-width: 360px;
}

@media (min-width: 576px) {
    .logo {
        max-width: 360px;
    }
}

@media (min-width: 768px) {
    .logo {
        max-width: 360px;
    }
}

@media (min-width: 992px) {
    .logo {
        max-width: 360px;
    }
}

@media (min-width: 1200px) {
    .logo {
        max-width: 360px;
    }
}

@media (min-width: 1400px) {
    .logo {
        max-width: 360px;
    }
}
"""

logo_component = st.components.v2.component(
    name="logo",
    html=f'<div class="logo">{svg.replace("#1e293b","var(--st-text-color)")}</div>',
    css=logo_css,
)
