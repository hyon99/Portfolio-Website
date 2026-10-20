"""
Sudipon Makal — Portfolio
A single-page Streamlit site with in-app navigation (no new tabs/reloads
feel), a typewriter reveal on headlines, and a fade-up reveal on photos
and content cards.
"""
from adk_chat import ask_agent
import base64
import itertools
from pathlib import Path

import streamlit as st

# --------------------------------------------------------------------------
# Page config
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Sudipon Makal — Portfolio",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ASSETS = Path(__file__).parent / "assets"
CSS_PATH = Path(__file__).parent / "style.css"
_counter = itertools.count()


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def load_css(path: Path) -> None:
    """Read an external CSS file and inject it into the page."""
    with open(path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


AVATAR_B64 = _b64(ASSETS / "avatar.jpg") if (ASSETS / "avatar.jpg").exists() else ""


# --------------------------------------------------------------------------
# Content — edit anything in content.py to update the site
# --------------------------------------------------------------------------
from content import (
    NAME, ROLE_LINE, TAGLINE, INTRO, CURRENT_LINE, QUOTE, CTA_LINE,
    EDUCATION, CGPA, GRAD_YEAR, ABOUT_PARAGRAPHS, JOURNEY, PROJECTS,
    WHAT_I_DO, EXPERIENCE, SKILLS, CERTIFICATIONS, CERTIFICATES_DRIVE_URL,
    GOALS, BEYOND, CONTACT, MICROCOPY, ICONS,
)

# --------------------------------------------------------------------------
# CSS — design tokens + components + animation (now in style.css)
# --------------------------------------------------------------------------
load_css(CSS_PATH)

# --------------------------------------------------------------------------
# Small render helpers
# --------------------------------------------------------------------------

def typewriter(text: str, tag: str = "span", css_class: str = "", delay: float = 0.0,
                speed: float = 0.03) -> str:
    """Return HTML for a left-to-right typewriter reveal of `text`."""
    cls = f"tw{next(_counter)}"
    steps = max(len(text), 1)
    duration = round(min(steps * speed, 2.6), 2)
    return f"""
    <style>
    .{cls} {{
        display:inline-block; clip-path: inset(0 100% 0 0);
        animation: reveal-{cls} {duration}s steps({steps},end) {delay}s forwards;
    }}
    @keyframes reveal-{cls} {{ to {{ clip-path: inset(0 0% 0 0); }} }}
    </style>
    <{tag} class="{css_class} {cls}">{text}</{tag}>
    """


def fade(html: str, delay: float = 0.0, extra_class: str = "") -> str:
    return f'<div class="fade-up {extra_class}" style="animation-delay:{delay}s;">{html}</div>'


def circuit_divider() -> str:
    return """
    <div class="circuit-divider">
      <svg viewBox="0 0 800 26" preserveAspectRatio="none">
        <defs>
          <linearGradient id="cd" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#a855f7" stop-opacity="0"/>
            <stop offset="50%" stop-color="#e94ff5" stop-opacity="1"/>
            <stop offset="100%" stop-color="#38e0e0" stop-opacity="0"/>
          </linearGradient>
        </defs>
        <path d="M0 13 H320 L340 4 H460 L480 13 H800" fill="none" stroke="url(#cd)" stroke-width="1.4"/>
        <circle cx="340" cy="4" r="3" fill="#e94ff5"/>
        <circle cx="480" cy="13" r="3" fill="#38e0e0"/>
      </svg>
    </div>
    """


def microcopy(page: str) -> None:
    st.markdown(f'<div class="microcopy">"{MICROCOPY.get(page, "")}"</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Navigation state
# --------------------------------------------------------------------------
PAGES = ["Home", "About Me", "Experience", "Projects", "Contact Me", "AI Agent"]
if "page" not in st.session_state:
    st.session_state.page = "Home"


def render_nav():
    cols = st.columns([1.5, 1, 1.2, 1, 1.25, 1.15])
    with cols[0]:
        if st.button("Sudipon Makal.", key="nav_home", use_container_width=False):
            st.session_state.page = "Home"
            st.rerun()
    for i, label in enumerate(
        ["About Me", "Experience", "Projects", "Contact Me", "AI Agent"], start=1
    ):
        page_key = label
        with cols[i]:
            is_active = st.session_state.page == page_key
            if st.button(label, key=f"nav_{page_key}", type="primary" if is_active else "secondary",
                         use_container_width=True):
                st.session_state.page = page_key
                st.rerun()

render_nav()

st.markdown('<div class="eyebrow">PORTFOLIO</div>', unsafe_allow_html=True)
st.markdown(typewriter(TAGLINE, tag="div", css_class="tagline", speed=0.028), unsafe_allow_html=True)

# --------------------------------------------------------------------------
# HOME
# --------------------------------------------------------------------------
if st.session_state.page == "Home":
    avatar_img = (
        f'<img src="data:image/png;base64,{AVATAR_B64}" alt="{NAME}"/>'
        if AVATAR_B64 else ""
    )
    st.markdown(f'''
    <div class="hero-card">
      <div style="display:flex; gap:2rem; flex-wrap:wrap; align-items:flex-start;">
        <div class="avatar-ring">{avatar_img}</div>
        <div style="flex:1; min-width:260px;">
          <div class="hero-name">{typewriter(NAME, speed=0.045)}</div>
          <div class="hero-role">{ROLE_LINE}</div>
          <div class="hero-body">
            <p>{INTRO}</p>
            <p>{CURRENT_LINE}</p>
          </div>
          <div class="quote-block">"{QUOTE}"</div>
          <div class="cta-line">{CTA_LINE}</div>
        </div>
      </div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown(fade("", delay=0), unsafe_allow_html=True)  # keeps avatar/card timing consistent
    microcopy("Home")

# --------------------------------------------------------------------------
# ABOUT ME
# --------------------------------------------------------------------------
elif st.session_state.page == "About Me":
    st.markdown(circuit_divider(), unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{typewriter("About Me", speed=0.05)}</div>',
                unsafe_allow_html=True)

    facts = f'''
    <div class="facts-strip">
      <div class="fact-card"><div class="fact-label">Education</div><div class="fact-value">{EDUCATION}</div></div>
      <div class="fact-card"><div class="fact-label">CGPA</div><div class="fact-value">{CGPA}</div></div>
      <div class="fact-card"><div class="fact-label">Expected Graduation</div><div class="fact-value">{GRAD_YEAR}</div></div>
    </div>
    '''
    st.markdown(fade(facts, delay=0.05), unsafe_allow_html=True)

    body = "".join(f"<p>{p}</p>" for p in ABOUT_PARAGRAPHS)
    st.markdown(fade(f'<div class="card">{body}</div>', delay=0.1), unsafe_allow_html=True)

    st.markdown('<h3 style="margin-top:2.2rem;">My Journey</h3>', unsafe_allow_html=True)
    items = ""
    for i, (year, title, text) in enumerate(JOURNEY):
        items += (
            f'<div class="t-item"><div class="t-year">{year}</div>'
            f'<div class="t-title">{title}</div><div class="t-text">{text}</div></div>'
        )
    st.markdown(fade(f'<div class="timeline">{items}</div>', delay=0.15), unsafe_allow_html=True)
    microcopy("About Me")

# --------------------------------------------------------------------------
# EXPERIENCE
# --------------------------------------------------------------------------
elif st.session_state.page == "Experience":
    st.markdown(circuit_divider(), unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{typewriter("Experience", speed=0.05)}</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Hands-on time in both enterprise infrastructure '
                'and embedded hardware, learning how each operates in the real world.</div>',
                unsafe_allow_html=True)

    for i, exp in enumerate(EXPERIENCE):
        chips = "".join(f'<span class="chip">{g}</span>' for g in exp["gained"])
        period_line = exp["period"] + (f" · {exp['location']}" if exp.get("location") else "")
        html = f'''
        <div class="card">
          <div class="exp-head">
            <div><span class="exp-role">{exp["role"]}</span> · <span class="exp-company">{exp["company"]}</span></div>
            <div class="exp-period">{period_line}</div>
          </div>
          <p style="margin-top:.6rem;">{exp["summary"]}</p>
          <div class="chip-row">{chips}</div>
        </div>
        '''
        st.markdown(fade(html, delay=0.1 * (i + 1)), unsafe_allow_html=True)
    microcopy("Experience")

# --------------------------------------------------------------------------
# PROJECTS  (capabilities + skills + certifications)
# --------------------------------------------------------------------------
elif st.session_state.page == "Projects":
    st.markdown(circuit_divider(), unsafe_allow_html=True)
    proj_title = typewriter("Projects", speed=0.05)
    st.markdown(f'<div class="section-title">{proj_title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Proof-of-concept work at the intersection of AI '
                'and embedded systems — each one backed by a GitHub repo.</div>',
                unsafe_allow_html=True)

    for i, p in enumerate(PROJECTS):
        tech_chips = "".join(f'<span class="chip">{t}</span>' for t in p["tech"])
        html = f'''
        <div class="card">
          <div class="proj-title">{p["title"]}</div>
          <p>{p["desc"]}</p>
          <div class="chip-row">{tech_chips}</div>
          <a class="proj-link" href="{p["github"]}" target="_blank">↗ View on GitHub</a>
        </div>
        '''
        st.markdown(fade(html, delay=0.08 * (i + 1)), unsafe_allow_html=True)

    st.markdown('<h3 style="margin-top:2.2rem;">What I Do</h3>', unsafe_allow_html=True)
    cards = "".join(
        f'<div class="card"><div class="do-title">{t}</div><p>{d}</p></div>'
        for t, d in WHAT_I_DO
    )
    st.markdown(fade(f'<div class="do-grid">{cards}</div>', delay=0.1), unsafe_allow_html=True)

    st.markdown('<h3 style="margin-top:2.2rem;">Skills</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color:var(--text-dim); font-size:.9rem; margin-top:-.6rem;">'
                'Instead of listing technologies, I prefer thinking of them as tools that '
                'help me solve different kinds of problems.</p>', unsafe_allow_html=True)
    skill_html = ""
    for i, (cat, items) in enumerate(SKILLS.items()):
        chips = "".join(f'<span class="chip skill">{s}</span>' for s in items)
        skill_html += f'<div class="skill-cat">{cat}</div><div class="chip-row">{chips}</div>'
    st.markdown(fade(skill_html, delay=0.15), unsafe_allow_html=True)

    st.markdown('<h3 style="margin-top:2.2rem;">Certifications</h3>', unsafe_allow_html=True)
    cert_html = "".join(
        f'<div class="cert-item"><div class="cert-dot"></div>{c}</div>' for c in CERTIFICATIONS
    )
    st.markdown(fade(f'<div class="card">{cert_html}'
                      f'<a class="proj-link" href="{CERTIFICATES_DRIVE_URL}" target="_blank" '
                      f'style="margin-top:1rem;">↗ View all certificates</a></div>', delay=0.2),
                unsafe_allow_html=True)
    microcopy("Projects")

# --------------------------------------------------------------------------
# CONTACT ME
# --------------------------------------------------------------------------
elif st.session_state.page == "Contact Me":
    st.markdown(circuit_divider(), unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{typewriter("Ways to contact me:", speed=0.03)}</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Whether you want to discuss technology, '
                'collaborate on an idea, or simply connect, I\'d be happy to hear from you.</div>',
                unsafe_allow_html=True)

    cards = "".join(
        f'<a class="contact-card" href="{href}" target="_blank">'
        f'<div class="contact-icon">{ICONS[label]}</div>'
        f'<div><div class="contact-label">{label}</div>'
        f'<div class="contact-value">{value}</div></div>'
        f'</a>'
        for label, (value, href) in CONTACT.items()
    )
    st.markdown(fade(f'<div class="contact-grid">{cards}</div>', delay=0.1), unsafe_allow_html=True)

    st.markdown('<h3 style="margin-top:2.2rem;">Beyond Engineering</h3>', unsafe_allow_html=True)
    st.markdown(fade(f'<div class="card"><p>{BEYOND}</p></div>', delay=0.15), unsafe_allow_html=True)

    st.markdown('<h3 style="margin-top:2.2rem;">Current Goals</h3>', unsafe_allow_html=True)
    goal_items = "".join(f"<li>{g}</li>" for g in GOALS)
    st.markdown(fade(f'<ul class="goal-list">{goal_items}</ul>', delay=0.2, extra_class="card"),
                unsafe_allow_html=True)
    microcopy("Contact Me")

# --------------------------------------------------------------------------
# AI AGENT
# --------------------------------------------------------------------------
elif st.session_state.page == "AI Agent":
    st.markdown(circuit_divider(), unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{typewriter("AI Agent", speed=0.05)}</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ask me anything about Sudipon — his projects, '
                'experience, skills, or background — and the assistant will answer.</div>',
                unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            for img_bytes in msg.get("images", []):
                st.image(img_bytes)

    prompt = st.chat_input("Ask me anything about Sudipon...")
    if prompt:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            try:
                result = ask_agent(prompt)
            except Exception as e:
                result = {
                    "text": f"Sorry, something went wrong while generating a response: {e}",
                    "images": [],
                }

        # ask_agent returns {"text": str, "images": [bytes, ...]}; images are
        # PNG bytes for any diagrams the agent generated via draw_block_diagram.
        answer_text = result.get("text") or "Sorry, I couldn't generate a response — please try again."
        images = result.get("images", [])

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer_text,
                "images": images,
            }
        )
        with st.chat_message("assistant"):
            st.markdown(answer_text)
            for img_bytes in images:
                st.image(img_bytes)
    microcopy("AI Agent")