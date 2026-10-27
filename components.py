import streamlit as st
from pathlib import Path

with (Path(__file__).parent / "assets" / "logo.svg").open(encoding="utf-8") as f:
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

scroll_css = """
/* 1. Set up the container */
.scroll-container {
  width: 100%;
  container-type: inline-size;  /* Enables container query units (cqw) */
  overflow: hidden;
  white-space: nowrap;
  box-sizing: border-box;
  background: transparent;
  padding: 0;
  border: 0;
}

/* 2. Format the text element */
.scroll-text {
  display: inline-block;
  white-space: nowrap;
  margin: 0;
  padding: 0.25rem;
  color: var(--st-code-text-color, var(--st-text-color, #31333f));
  font-family: var(--st-code-font, monospace);
  font-size: var(--st-code-font-size, 0.875rem);
  font-weight: var(--st-code-font-weight, 400);
  line-height: 1.6;
  background: var(--st-code-background-color, #f0f2f6);
  border-radius: var(--st-code-radius, 0.25rem);
  animation: bounce-text 6s ease-in-out infinite alternate;
}

/* 3. Pause animation when user hovers over it */
.scroll-container:hover .scroll-text {
  animation-play-state: paused;
}

/* 4. Define keyframes for back-and-forth movement */
@keyframes bounce-text {
  0%, 20% {
    /* Holds text at the start for readability */
    transform: translateX(0);
  }
  80%, 100% {
    /* Moves text until the right edge aligns with the container right edge.
       If text is shorter than container, min(0px, ...) prevents unnecessary movement. */
    transform: translateX(min(0px, calc(100cqw - 100%)));
  }
}

/* 5. Accessibility: Respect user prefers-reduced-motion settings */
@media (prefers-reduced-motion: reduce) {
  .scroll-text {
    animation: none;
  }
  .scroll-container {
    overflow-x: auto;
  }
}
"""

scroll_html = """
<div class="scroll-container">
  <code class="scroll-text"></code>
</div>
"""

scroll_js = """
export default function (component) {
  const { data, parentElement } = component
  const container = parentElement.querySelector(".scroll-container")
  const text = parentElement.querySelector(".scroll-text")

  if (!container || !text) return

  text.textContent = data?.text ?? ""
}
"""

_scroll_component = st.components.v2.component(
    name="scroll",
    html=scroll_html,
    css=scroll_css,
    js=scroll_js,
)


def scroll_component(text: str):
    return _scroll_component(data={"text": text}, width="stretch")
