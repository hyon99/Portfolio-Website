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
    layout="wide",
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


AVATAR_PATH = ASSETS / "avatar_idle.png"
AVATAR_B64 = _b64(AVATAR_PATH) if AVATAR_PATH.exists() else ""  # lobby scene only
HOME_AVATAR_PATH = ASSETS / "avatar.jpg"
HOME_AVATAR_B64 = _b64(HOME_AVATAR_PATH) if HOME_AVATAR_PATH.exists() else ""


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
# Game-like intro / loading lobby
# --------------------------------------------------------------------------
PAGES = ["Home", "About Me", "Experience", "Projects", "Contact Me", "AI Agent"]
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "entered_lobby" not in st.session_state:
    st.session_state.entered_lobby = False

if not st.session_state.entered_lobby:
    st.markdown('''
    <div class="game-loading-screen">
      <div class="loading-skyline"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
      <div class="loading-topline"><span>SM // DIGITAL UNIVERSE</span><span>BUILD 2026.10 · ONLINE</span></div>
      <div class="loading-center">
        <div class="loading-emblem"><div class="emblem-core">SM</div><div class="emblem-ring ring-a"></div><div class="emblem-ring ring-b"></div></div>
        <div class="loading-kicker">A PERSONAL WORLD, NOT JUST A WEBSITE</div>
        <div class="loading-title">ENTER THE<br><span>PORTFOLIOVERSE</span></div>
        <p class="loading-subtitle">Explore the world. Discover the work.</p>
        <div class="loading-progress"><span></span></div>
        <div class="loading-status"><span>WORLD SYSTEMS READY</span><span>100%</span></div>
      </div>
      <div class="loading-avatars"><div class="npc npc-red"><b></b><i></i><small>BUILDER</small></div><div class="npc npc-cyan"><b></b><i></i><small>EXPLORER</small></div><div class="npc npc-violet"><b></b><i></i><small>CREATOR</small></div><div class="npc npc-gold"><b></b><i></i><small>ALLY</small></div><div class="npc npc-green"><b></b><i></i><small>SCOUT</small></div></div>
      <div class="loading-footer">WASD NOT REQUIRED · YOUR CURIOSITY IS THE CONTROLLER</div>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶  ENTER WORLD", key="enter_lobby", type="primary", use_container_width=True):
        st.session_state.entered_lobby = True
        st.rerun()
    st.stop()


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

# Persistent game-lobby HUD: the player avatar changes pose for each destination.
pose_map = {
    "Home": ("HERO / IDLE", "pose-idle", "Welcome to my world"),
    "About Me": ("HERO / THINKING", "pose-think", "Origin story unlocked"),
    "Experience": ("HERO / READY", "pose-ready", "Missions & experience"),
    "Projects": ("HERO / ACTION", "pose-action", "Projects unlocked"),
    "Contact Me": ("HERO / WAVE", "pose-wave", "Open a new connection"),
    "AI Agent": ("HERO / POWER-UP", "pose-power", "AI companion online"),
}
pose_label, pose_class, world_caption = pose_map.get(st.session_state.page, pose_map["Home"])
main_avatar = (f'<img class="player-model" src="data:image/png;base64,{AVATAR_B64}" alt="3D-style player avatar" />' if AVATAR_B64 else '<span class="avatar-initials">SM</span>')
st.markdown(f'''<div class="lobby-hud">
  <div class="lobby-scene">
    <div class="scene-scanlines"></div><div class="scene-sun"></div><div class="scene-city city-back"></div><div class="scene-city city-front"></div>
    <div class="scene-label label-left"><span class="live-dot"></span> WORLD INSTANCE: ACTIVE<br><small>SECTOR 01 · PORTFOLIO DISTRICT</small></div>
    <div class="scene-label label-right">{pose_label}<br><small>PLAYER 01 · SUDIPON</small></div>
    <div class="player-avatar {pose_class}">{main_avatar}<div class="player-aura"></div></div>
    <div class="player-shadow"></div>
    <div class="npc-lobby npc-lobby-one"><div class="npc-body"><b></b><i></i></div><small>AI GUIDE</small></div>
    <div class="npc-lobby npc-lobby-two"><div class="npc-body"><b></b><i></i></div><small>BUILDER</small></div>
    <div class="npc-lobby npc-lobby-three"><div class="npc-body"><b></b><i></i></div><small>SCOUT</small></div>
    <div class="scene-ground"></div><div class="scene-caption"><span class="scroll-unlock">SCROLL DOWN TO UNLOCK MORE INFORMATION <b>↓</b></span></div>
  </div>
  
</div>''', unsafe_allow_html=True)

st.markdown('<div class="eyebrow">PORTFOLIOVERSE / DESTINATION TERMINAL</div>', unsafe_allow_html=True)
st.markdown(typewriter(TAGLINE, tag="div", css_class="tagline", speed=0.028), unsafe_allow_html=True)

# --------------------------------------------------------------------------
# HOME
# --------------------------------------------------------------------------
if st.session_state.page == "Home":
    avatar_img = (
        f'<img src="data:image/jpeg;base64,{HOME_AVATAR_B64}" alt="{NAME} avatar"/>'
        if HOME_AVATAR_B64 else '<div class="avatar-placeholder"><span>SM</span><small>AVATAR CORE</small></div>'
    )
    st.markdown(f'''
    <div class="hero-card">
      <div class="hero-grid">
        <div class="metaverse-stage" aria-label="Metaverse avatar display">
          <div class="stage-grid"></div>
          <div class="orbit orbit-one"></div>
          <div class="orbit orbit-two"></div>
          <div class="orbit orbit-three"></div>
          <div class="avatar-platform"></div>
          <div class="avatar-ring">{avatar_img}</div>
          <div class="stage-tag tag-top">IDENTITY // 01</div>
          <div class="stage-tag tag-bottom"><span class="live-dot"></span> DIGITAL TWIN ONLINE</div>
          <div class="floating-node node-left">AI / ML</div>
          <div class="floating-node node-right">IOT</div>
        </div>
        <div class="hero-copy">
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
    st.markdown('<div class="game-screen ai-screen">', unsafe_allow_html=True)
    left, right = st.columns([0.82, 1.45], gap="large")
    with left:
        st.markdown("""
        <div class="mission-panel">
          <div class="hud-kicker">PORTFOLIOVERSE // COMMS LINK</div>
          <div class="mission-title">AI<br>ASSISTANT</div>
          <div class="mission-rule"></div>
          <div class="mission-status"><span class="status-dot"></span> CONNECTION ESTABLISHED</div>
          <p class="mission-copy">Your interactive intelligence interface. Ask about projects, engineering experience, skills, or the story behind the build.</p>
          <div class="mission-label">AVAILABLE INTEL</div>
          <div class="intel-row"><span>01</span> PROJECT ARCHIVE</div>
          <div class="intel-row"><span>02</span> EXPERIENCE LOG</div>
          <div class="intel-row"><span>03</span> SKILL MATRIX</div>
          <div class="intel-row"><span>04</span> BACKGROUND FILE</div>
          <div class="operator-card"><div class="operator-orb">AI</div><div><b>PORTFOLIO INTELLIGENCE</b><small>Response system · Online</small></div></div>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="comms-header">
          <div><div class="hud-kicker">SECURE CHANNEL / 04</div><div class="comms-title">COMMUNICATIONS</div></div>
          <div class="live-pill"><span class="status-dot"></span> LIVE</div>
        </div>
        <div class="comms-subtitle">Talk to the portfolio assistant</div>
        """, unsafe_allow_html=True)
        if "messages" not in st.session_state:
            st.session_state.messages = []
        chat_area = st.container(height=430, border=False)
        with chat_area:
            if not st.session_state.messages:
                st.markdown("""
                <div class="welcome-transmission">
                  <div class="bot-emblem">AI</div>
                  <div class="transmission-tag">INCOMING TRANSMISSION</div>
                  <h3>Channel ready.</h3>
                  <p>Ask me something about Sudipon's work. I can walk you through projects, tools, experience, and technical decisions.</p>
                </div>
                """, unsafe_allow_html=True)
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
                    st.markdown(msg["content"])
                    for img_bytes in msg.get("images", []):
                        st.image(img_bytes, use_container_width=True)
        prompt = st.chat_input("Transmit a message…")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Establishing response…"):
                try:
                    result = ask_agent(prompt)
                except Exception as e:
                    result = {"text": f"Sorry, something went wrong while generating a response: {e}", "images": []}
            answer_text = result.get("text") or "Sorry, I couldn't generate a response — please try again."
            images = result.get("images", [])
            st.session_state.messages.append({"role": "assistant", "content": answer_text, "images": images})
            st.rerun()
        st.markdown('<div class="comms-footer">ENTER TO TRANSMIT <span>•</span> AI-POWERED RESPONSE</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    microcopy("AI Agent")
