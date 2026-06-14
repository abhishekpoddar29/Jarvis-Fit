"""
JarvisFit — Enhanced Iron Man-Inspired UI with Speaking State
"""

import json
import os
import time
import threading
import gradio as gr
from datetime import datetime

from src.jarvisfit.config.settings import SESSION_PATH
from src.jarvisfit.state import app_state


# ════════════════════════════════════════════
# STATE READER
# ════════════════════════════════════════════

def read_state() -> dict:
    try:
        with open(SESSION_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}


# ════════════════════════════════════════════
# STATE → UI BUILDERS
# ════════════════════════════════════════════

def build_orb_html(state: dict) -> str:
    """Build the Iron Man-inspired orb with state-specific animations."""
    agent     = state.get("agent_state", {})
    awake     = agent.get("jarvis_awake", False)
    active    = agent.get("active_session", False)
    listening = agent.get("listening_for_command", False)
    speaking  = agent.get("speaking", False)  # NEW: speaking state
    speech_text = state.get("last_speech", "")  # NEW: text being spoken
    status    = state.get("session_status", "not_started")

    # Determine state class and colors
    if not awake:
        state_class  = "orb-sleeping"
        label        = "SLEEPING"
        color_one    = "#1a3a4a"
        color_two    = "#0d2030"
        color_three  = "#1a3a4a80"
        color_four   = "#0d203080"
        color_five   = "#1a3a4a40"
        opacity      = "0.35"
        show_wave    = False
        show_speech  = False
    elif speaking:
        # NEW: Speaking state takes priority over listening
        state_class  = "orb-speaking"
        label        = "SPEAKING"
        color_one    = "#39ff14"
        color_two    = "#2eb80f"
        color_three  = "#39ff1480"
        color_four   = "#2eb80f80"
        color_five   = "#39ff1440"
        opacity      = "1"
        show_wave    = False
        show_speech  = True
    elif active and status == "active":
        state_class  = "orb-active"
        label        = "ACTIVE SESSION"
        color_one    = "#00ffe7"
        color_two    = "#00bfff"
        color_three  = "#00ffe780"
        color_four   = "#00bfff80"
        color_five   = "#00ffe740"
        opacity      = "1"
        show_wave    = False
        show_speech  = False
    elif status == "paused":
        state_class  = "orb-paused"
        label        = "PAUSED"
        color_one    = "#f5a623"
        color_two    = "#c47d0e"
        color_three  = "#f5a62380"
        color_four   = "#c47d0e80"
        color_five   = "#f5a62340"
        opacity      = "1"
        show_wave    = False
        show_speech  = False
    elif listening:
        state_class  = "orb-listening"
        label        = "LISTENING"
        color_one    = "#ffbf48"
        color_two    = "#be4a1d"
        color_three  = "#ffbf4780"
        color_four   = "#bf4a1d80"
        color_five   = "#ffbf4740"
        opacity      = "1"
        show_wave    = True
        show_speech  = False
    else:
        state_class  = "orb-awake"
        label        = "AWAKE"
        color_one    = "#7efff5"
        color_two    = "#00bfff"
        color_three  = "#7efff580"
        color_four   = "#00bfff80"
        color_five   = "#7efff540"
        opacity      = "1"
        show_wave    = False
        show_speech  = False

    return f"""
        <div class="orb-container {state_class}" style="opacity:{opacity};transition:opacity 0.8s ease;">
            <div class="orb-assembly">
                <div class="orb-ring-outer" style="border-color:{color_one};box-shadow:0 0 20px {color_three},inset 0 0 20px {color_three};"></div>
                <div class="orb-ring-mid" style="border-top-color:{color_one};border-bottom-color:{color_two};"></div>
                <div class="orb-hex-pattern">
                    <svg viewBox="0 0 100 100" style="width:100%;height:100%;">
                        <polygon points="50,5 95,27.5 95,72.5 50,95 5,72.5 5,27.5" 
                            fill="none" stroke="{color_one}" stroke-width="0.5" opacity="0.5"/>
                        <polygon points="50,20 80,35 80,65 50,80 20,65 20,35" 
                            fill="none" stroke="{color_two}" stroke-width="0.5" opacity="0.3"/>
                        <polygon points="50,35 65,42.5 65,57.5 50,65 35,57.5 35,42.5" 
                            fill="none" stroke="{color_one}" stroke-width="0.5" opacity="0.2"/>
                    </svg>
                </div>
                <div class="orb-core" style="background:radial-gradient(circle at 20% 20%, {color_one}, {color_two}, {color_four});">
                    <div class="orb-inner-ring"></div>
                </div>
                <div class="orb-particles">
                    <div class="orb-particle" style="top:5%;left:50%;animation-delay:0s;"></div>
                    <div class="orb-particle" style="top:15%;left:85%;animation-delay:0.3s;"></div>
                    <div class="orb-particle" style="top:50%;left:95%;animation-delay:0.6s;"></div>
                    <div class="orb-particle" style="top:85%;left:85%;animation-delay:0.9s;"></div>
                    <div class="orb-particle" style="top:95%;left:50%;animation-delay:1.2s;"></div>
                    <div class="orb-particle" style="top:85%;left:15%;animation-delay:1.5s;"></div>
                    <div class="orb-particle" style="top:50%;left:5%;animation-delay:1.8s;"></div>
                    <div class="orb-particle" style="top:15%;left:15%;animation-delay:2.1s;"></div>
                </div>
            </div>
            <div class="orb-label" style="color:{color_one};text-shadow:0 0 12px {color_three};">
                {label}
            </div>
            <div class="voice-wave {'active' if show_wave else ''}">
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
                <div class="voice-bar"></div>
            </div>
            <div class="speech-display {'active' if show_speech else ''}">
                <div class="speech-label">JARVIS SPEAKING</div>
                <div class="speech-text">{speech_text}</div>
            </div>
        </div>
"""


def build_workout_html(state: dict) -> str:
    """Build the workout panel with animated exercise items."""
    today    = state.get("today_progress", {})
    exs      = today.get("exercises", {})
    day      = state.get("current_day", "—")
    pct      = today.get("completion_percentage", 0)
    status   = state.get("session_status", "not_started")

    if status == "not_started":
        return """
        <div class="workout-empty">
            <div class="empty-icon">⬡</div>
            <div class="empty-text">Workout plan loads on session start</div>
        </div>
        """

    all_exercises = []
    for cat in ["gym", "yoga", "running"]:
        for ex in exs.get(cat, []):
            all_exercises.append((cat, ex))

    if not all_exercises:
        return '<div class="workout-empty"><div class="empty-text">No exercises for today</div></div>'

    items_html = ""
    for i, (cat, ex) in enumerate(all_exercises):
        ex_status = ex.get("status", "pending")
        name      = ex.get("name", "")
        delay     = i * 0.1  # Staggered animation

        if ex_status == "completed":
            icon       = "✓"
            item_class = "ex-completed"
            detail     = ""
        elif ex_status == "skipped":
            icon       = "—"
            item_class = "ex-skipped"
            detail     = ""
        else:
            icon       = "◈"
            item_class = "ex-pending"
            detail     = ""

        if cat == "gym":
            sets = ex.get("sets")
            reps = ex.get("reps")
            dur  = ex.get("duration_seconds")
            dmin = ex.get("duration_minutes")
            if sets and reps:
                detail = f"{sets} × {reps} reps"
            elif sets and dur:
                detail = f"{sets} × {dur}s"
            elif dmin:
                detail = f"{dmin} min"
        elif cat == "yoga":
            dmin = ex.get("duration_minutes")
            if dmin:
                detail = f"{dmin} min"
        elif cat == "running":
            dmin = ex.get("duration_minutes")
            if dmin:
                detail = f"{dmin} min"

        cat_badge = f'<span class="cat-badge cat-{cat}">{cat.upper()}</span>'

        items_html += f"""
        <div class="ex-item {item_class}" style="animation-delay:{delay}s;">
            <div class="ex-icon">{icon}</div>
            <div class="ex-info">
                <div class="ex-name">{name}</div>
                <div class="ex-detail">{detail}</div>
            </div>
            {cat_badge}
        </div>
        """

    bar_color = "#00ffe7" if pct == 100 else "#00bfff"

    return f"""
    <div class="workout-panel">
        <div class="workout-header">
            <div class="workout-day">{day.upper()}</div>
            <div class="workout-pct" style="color:{bar_color};">{pct}%</div>
        </div>
        <div class="progress-track">
            <div class="progress-fill" style="width:{pct}%;background:{bar_color};box-shadow:0 0 10px {bar_color}88;"></div>
        </div>
        <div class="ex-list">
            {items_html}
        </div>
    </div>
    """


def build_weather_html(state: dict) -> str:
    """Build the session info card with animated border."""
    if not state.get("agent_state", {}).get("jarvis_awake"):
        return '<div class="weather-empty">—</div>'

    day  = state.get("current_day", "—")
    now  = datetime.now()
    hour = now.hour
    tod  = "Morning" if hour < 12 else "Afternoon" if hour < 17 else "Evening"
    time_str = now.strftime("%I:%M %p").lstrip("0")

    return f"""
    <div class="weather-card">
        <div class="weather-tod">{tod}</div>
        <div class="weather-day">{day}</div>
        <div class="weather-time">{time_str}</div>
    </div>
    """


def build_log_html(state: dict) -> str:
    """Build the weekly log with animated entries."""
    logs     = state.get("daily_logs", {})
    streak   = state.get("streak_days", 0)
    done     = state.get("completed_days", [])
    days_ord = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    rows = ""
    for i, d in enumerate(days_ord):
        log       = logs.get(d, {})
        gym_done  = log.get("gym_completed", False)
        yoga_done = log.get("yoga_completed", False)
        run_done  = log.get("running_completed", False)
        is_today  = d == state.get("current_day", "")
        is_done   = d in done
        delay     = i * 0.05

        day_class  = "log-today" if is_today else "log-done" if is_done else "log-pending"
        gym_icon   = "✓" if gym_done  else "·"
        yoga_icon  = "✓" if yoga_done else "·"
        run_icon   = "✓" if run_done  else "·"

        rows += f"""
        <div class="log-row {day_class}" style="animation-delay:{delay}s;">
            <div class="log-day">{d[:3].upper()}</div>
            <div class="log-icons">
                <span title="Gym">{gym_icon}</span>
                <span title="Yoga">{yoga_icon}</span>
                <span title="Run">{run_icon}</span>
            </div>
        </div>
        """

    return f"""
    <div class="log-panel">
        <div class="log-streak">🔥 {streak} day streak</div>
        <div class="log-grid">{rows}</div>
    </div>
    """


def build_summary_html(state: dict) -> str:
    """Build the session summary with animated stat chips."""
    if not state.get("diet_summary_given"):
        return '<div class="summary-empty">Post-workout summary appears here after session</div>'

    today    = state.get("today_progress", {})
    exs      = today.get("exercises", {})
    day      = state.get("current_day", "today")
    gym_done = sum(1 for e in exs.get("gym",     []) if e["status"] == "completed")
    yog_done = sum(1 for e in exs.get("yoga",    []) if e["status"] == "completed")
    run_done = sum(1 for e in exs.get("running", []) if e["status"] == "completed")
    total    = gym_done + yog_done + run_done

    return f"""
    <div class="summary-panel">
        <div class="summary-title">SESSION COMPLETE — {day.upper()}</div>
        <div class="summary-stats">
            <div class="stat-chip" style="animation-delay:0s;">💪 {gym_done} Gym</div>
            <div class="stat-chip" style="animation-delay:0.1s;">🧘 {yog_done} Yoga</div>
            <div class="stat-chip" style="animation-delay:0.2s;">🏃 {run_done} Run</div>
            <div class="stat-chip total-chip" style="animation-delay:0.3s;">⚡ {total} Total</div>
        </div>
        <div class="summary-note">Nutrition summary delivered. Great work today.</div>
    </div>
    """
def build_news_html() -> str:
    """Build the news headlines panel from shared state."""
    headlines = app_state.headlines

    if not headlines:
        return """
        <div class="news-section">
            <div class="news-header">
                <span class="news-indicator">◆</span>
                <span>HEADLINES</span>
            </div>
            <div class="news-empty">Say "Hey Jarvis" to fetch headlines</div>
        </div>
        """

    rank_colors = ['#00d4ff', '#00b8d4', '#0097a7']
    time_str = app_state.last_update or "now"

    cards_html = ""
    for i, headline in enumerate(headlines[:3]):
        color = rank_colors[i] if i < 3 else rank_colors[2]
        rank = str(i + 1).zfill(2)

        cards_html += f"""
        <div class="news-card">
            <div class="news-rank" style="color: {color}">{rank}</div>
            <div class="news-content">
                <div class="news-headline">{headline}</div>
                <div class="news-meta">
                    <span class="news-source">NEWSDATA</span>
                    <span class="news-dot">•</span>
                    <span class="news-time">{time_str}</span>
                </div>
            </div>
            <div class="news-glow" style="background: {color}"></div>
        </div>
        """

    return f"""
    <div class="news-section">
        <div class="news-header">
            <span class="news-indicator">◆</span>
            <span>HEADLINES</span>
        </div>
        <div class="news-cards-container">
            {cards_html}
        </div>
    </div>
    """

# ════════════════════════════════════════════
# ENHANCED CSS — Iron Man Theme with Speaking State
# ════════════════════════════════════════════

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&display=swap');

:root {
    --bg-deep:    #020c14;
    --bg-panel:   #040f1c;
    --bg-card:    #071828;
    --border:     #0d3352;
    --border-hi:  #0e5a8a;
    --cyan:       #00ffe7;
    --blue:       #00bfff;
    --gold:       #f5a623;
    --red:        #ff3860;
    --green:      #39ff14;
    --text-hi:    #e8f4ff;
    --text-mid:   #7ab3cc;
    --text-lo:    #2d5a7a;
    --font-disp:  'Rajdhani', sans-serif;
    --font-mono:  'Share Tech Mono', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body, .gradio-container {
    background: var(--bg-deep) !important;
    font-family: var(--font-disp) !important;
    color: var(--text-hi) !important;
    min-height: 100vh;
}

/* ════════════════════════════════════════════
   AMBIENT BACKGROUND — Animated Grid
   ════════════════════════════════════════════ */
.gradio-container {
    position: relative !important;
}

.gradio-container::after {
    content: '';
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background: 
        radial-gradient(ellipse at 50% 50%, #0a1f3a11 0%, transparent 70%),
        linear-gradient(0deg, transparent 24%, #00bfff08 25%, #00bfff08 26%, transparent 27%, transparent 74%, #00bfff08 75%, #00bfff08 76%, transparent 77%, transparent),
        linear-gradient(90deg, transparent 24%, #00bfff08 25%, #00bfff08 26%, transparent 27%, transparent 74%, #00bfff08 75%, #00bfff08 76%, transparent 77%, transparent);
    background-size: 100% 100%, 60px 60px, 60px 60px;
    animation: gridPulse 8s ease-in-out infinite;
}

@keyframes gridPulse {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.6; }
}

/* ════════════════════════════════════════════
   SCANLINE OVERLAY — Enhanced
   ════════════════════════════════════════════ */
.gradio-container::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,191,255,0.03) 2px,
        rgba(0,191,255,0.03) 4px
    );
    pointer-events: none;
    z-index: 9999;
    animation: scanlineFlicker 0.1s linear infinite;
}

@keyframes scanlineFlicker {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.98; }
}

/* ════════════════════════════════════════════
   HEADER — Enhanced with glitch effect
   ════════════════════════════════════════════ */
.fj-header {
    text-align: center;
    padding: 2rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
    position: relative;
    z-index: 10;
}

.fj-title {
    font-family: var(--font-disp);
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: 0.4em;
    color: var(--cyan);
    text-shadow: 0 0 30px #00ffe799, 0 0 60px #00ffe744;
    text-transform: uppercase;
    position: relative;
    animation: titlePulse 3s ease-in-out infinite;
}

.fj-title::before,
.fj-title::after {
    content: 'JarvisFit';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    opacity: 0.8;
}

.fj-title::before {
    color: #ff00ff;
    animation: glitch1 2s infinite linear alternate-reverse;
    clip-path: polygon(0 0, 100% 0, 100% 35%, 0 35%);
}

.fj-title::after {
    color: #00ffff;
    animation: glitch2 3s infinite linear alternate-reverse;
    clip-path: polygon(0 65%, 100% 65%, 100% 100%, 0 100%);
}

@keyframes titlePulse {
    0%, 100% { text-shadow: 0 0 30px #00ffe799, 0 0 60px #00ffe744; }
    50% { text-shadow: 0 0 40px #00ffe7cc, 0 0 80px #00ffe766, 0 0 120px #00ffe733; }
}

@keyframes glitch1 {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}

@keyframes glitch2 {
    0% { transform: translate(0); }
    20% { transform: translate(2px, -2px); }
    40% { transform: translate(2px, 2px); }
    60% { transform: translate(-2px, -2px); }
    80% { transform: translate(-2px, 2px); }
    100% { transform: translate(0); }
}

.fj-subtitle {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    color: var(--text-mid);
    margin-top: 0.5rem;
    animation: subtitleBlink 4s ease-in-out infinite;
}

@keyframes subtitleBlink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}


/* ════════════════════════════════════════════
   ORB ASSEMBLY — FIXED: All rings merged into one unit
   ════════════════════════════════════════════ */

.orb-assembly {
    position: relative;
    width: 280px;
    height: 280px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

/* All decorative elements locked to center via translate */
.orb-ring-outer,
.orb-ring-mid,
.orb-hex-pattern,
.orb-particles,
.orb-core {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* Outer ring — largest, behind everything */
.orb-ring-outer {
    width: 260px;
    height: 260px;
    border-radius: 50%;
    border: 1px solid var(--cyan);
    opacity: 0.3;
    animation: ringSpin 20s linear infinite, ringPulse 3s ease-in-out infinite;
    box-shadow: 0 0 20px var(--cyan), inset 0 0 20px var(--cyan);
    transition: all 0.8s ease;
    z-index: 1;
}

.orb-ring-outer::before {
    content: '';
    position: absolute;
    inset: -5px;
    border-radius: 50%;
    border: 1px dashed var(--cyan);
    opacity: 0.2;
    animation: ringSpin 30s linear infinite reverse;
}

/* Middle ring */
.orb-ring-mid {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border: 2px solid transparent;
    border-top-color: var(--cyan);
    border-bottom-color: var(--cyan);
    opacity: 0.5;
    animation: ringSpin 8s linear infinite reverse;
    transition: all 0.8s ease;
    z-index: 2;
}

.orb-ring-mid::before {
    content: '';
    position: absolute;
    inset: 10px;
    border-radius: 50%;
    border: 1px solid var(--blue);
    opacity: 0.4;
    animation: ringSpin 12s linear infinite;
}

/* Hex pattern */
.orb-hex-pattern {
    width: 150px;
    height: 150px;
    animation: ringSpin 15s linear infinite;
    opacity: 0.3;
    transition: all 0.8s ease;
    z-index: 3;
}

.orb-hex-pattern svg {
    width: 100%;
    height: 100%;
}

/* THE CORE — dead center, on top of rings */
.orb-core {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle at 20% 20%, var(--cyan), var(--blue), #0077be);
    box-shadow: 
        0 0 30px var(--cyan),
        0 0 60px var(--blue),
        0 0 100px var(--cyan),
        inset 0 0 30px rgba(255,255,255,0.3);
    animation: corePulse 2s ease-in-out infinite, coreBreathe 4s ease-in-out infinite;
    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 4;
    display: flex;
    align-items: center;
    justify-content: center;
}

.orb-core::before {
    content: '';
    position: absolute;
    inset: -5px;
    border-radius: 50%;
    border: 2px solid var(--cyan);
    opacity: 0.5;
    animation: corePulse 2s ease-in-out infinite reverse;
}

.orb-core::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: radial-gradient(circle at 40% 40%, rgba(255,255,255,0.4), transparent 60%);
}

/* Inner ring inside core */
.orb-inner-ring {
    position: relative;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    border: 1px solid rgba(0,255,231,0.3);
    animation: ringSpin 6s linear infinite;
    flex-shrink: 0;
}

.orb-inner-ring::before {
    content: '';
    position: absolute;
    width: 8px;
    height: 8px;
    background: var(--cyan);
    border-radius: 50%;
    top: -4px;
    left: 50%;
    transform: translateX(-50%);
    box-shadow: 0 0 10px var(--cyan);
}

/* Particles — centered container, particles orbit around */
.orb-particles {
    width: 260px;
    height: 260px;
    z-index: 5;
    pointer-events: none;
}

.orb-particle {
    position: absolute;
    width: 3px;
    height: 3px;
    background: var(--cyan);
    border-radius: 50%;
    box-shadow: 0 0 6px var(--cyan);
    animation: orbParticleFloat 3s ease-in-out infinite;
}

/* Particles positioned in orbit around center */
.orb-particle:nth-child(1) { top: 5%; left: 50%; animation-delay: 0s; }
.orb-particle:nth-child(2) { top: 15%; left: 85%; animation-delay: 0.3s; }
.orb-particle:nth-child(3) { top: 50%; left: 95%; animation-delay: 0.6s; }
.orb-particle:nth-child(4) { top: 85%; left: 85%; animation-delay: 0.9s; }
.orb-particle:nth-child(5) { top: 95%; left: 50%; animation-delay: 1.2s; }
.orb-particle:nth-child(6) { top: 85%; left: 15%; animation-delay: 1.5s; }
.orb-particle:nth-child(7) { top: 50%; left: 5%; animation-delay: 1.8s; }
.orb-particle:nth-child(8) { top: 15%; left: 15%; animation-delay: 2.1s; }

@keyframes orbParticleFloat {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.6; }
    25% { transform: translate(10px, -15px) scale(1.2); opacity: 1; }
    50% { transform: translate(-5px, -25px) scale(0.8); opacity: 0.4; }
    75% { transform: translate(-15px, -10px) scale(1.1); opacity: 0.8; }
}

/* ════════════════════════════════════════════
   ORB CONTAINER — holds assembly + label + wave + speech
   ════════════════════════════════════════════ */

.orb-container {
    position: relative;
    height: auto;
    width: 280px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    perspective: 1000px;
    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.orb-label {
    margin-top: 1.5rem;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--cyan);
    text-shadow: 0 0 10px var(--cyan);
    animation: labelPulse 2s ease-in-out infinite;
    transition: all 0.5s ease;
    text-align: center;
    width: 100%;
}

@keyframes labelPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.voice-wave {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3px;
    height: 30px;
    margin-top: 1rem;
    opacity: 0;
    transition: opacity 0.3s ease;
    width: 100%;
}

.voice-wave.active {
    opacity: 1;
}

.voice-bar {
    width: 3px;
    background: var(--cyan);
    border-radius: 2px;
    box-shadow: 0 0 6px var(--cyan);
    animation: voiceWave 0.5s ease-in-out infinite alternate;
}

.voice-bar:nth-child(1) { height: 8px; animation-delay: 0s; }
.voice-bar:nth-child(2) { height: 15px; animation-delay: 0.1s; }
.voice-bar:nth-child(3) { height: 22px; animation-delay: 0.2s; }
.voice-bar:nth-child(4) { height: 18px; animation-delay: 0.15s; }
.voice-bar:nth-child(5) { height: 12px; animation-delay: 0.05s; }
.voice-bar:nth-child(6) { height: 20px; animation-delay: 0.25s; }
.voice-bar:nth-child(7) { height: 14px; animation-delay: 0.1s; }
.voice-bar:nth-child(8) { height: 10px; animation-delay: 0.3s; }
.voice-bar:nth-child(9) { height: 16px; animation-delay: 0.2s; }
.voice-bar:nth-child(10) { height: 8px; animation-delay: 0.35s; }

@keyframes voiceWave {
    0% { transform: scaleY(0.3); opacity: 0.5; }
    100% { transform: scaleY(1); opacity: 1; }
}

.speech-display {
    margin-top: 1rem;
    padding: 0.8rem 1rem;
    background: rgba(57,255,20,0.05);
    border: 1px solid rgba(57,255,20,0.2);
    border-radius: 4px;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: #39ff14;
    text-shadow: 0 0 5px rgba(57,255,20,0.5);
    line-height: 1.5;
    max-width: 260px;
    text-align: center;
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    width: 100%;
}

.speech-display.active {
    opacity: 1;
    transform: translateY(0);
}

.speech-display::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #39ff14, transparent);
    animation: speechScan 2s linear infinite;
}

@keyframes speechScan {
    0% { left: -100%; }
    100% { left: 100%; }
}

.speech-label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: rgba(57,255,20,0.6);
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

.speech-text {
    min-height: 1.2em;
}


/* ════════════════════════════════════════════
   VOICE WAVE VISUALIZATION
   ════════════════════════════════════════════ */
.voice-wave {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3px;
    height: 30px;
    margin-top: 1rem;
    opacity: 0;
    transition: opacity 0.3s ease;
    width: 100%;
}

.voice-wave.active {
    opacity: 1;
}

.voice-bar {
    width: 3px;
    background: var(--cyan);
    border-radius: 2px;
    box-shadow: 0 0 6px var(--cyan);
    animation: voiceWave 0.5s ease-in-out infinite alternate;
}

.voice-bar:nth-child(1) { height: 8px; animation-delay: 0s; }
.voice-bar:nth-child(2) { height: 15px; animation-delay: 0.1s; }
.voice-bar:nth-child(3) { height: 22px; animation-delay: 0.2s; }
.voice-bar:nth-child(4) { height: 18px; animation-delay: 0.15s; }
.voice-bar:nth-child(5) { height: 12px; animation-delay: 0.05s; }
.voice-bar:nth-child(6) { height: 20px; animation-delay: 0.25s; }
.voice-bar:nth-child(7) { height: 14px; animation-delay: 0.1s; }
.voice-bar:nth-child(8) { height: 10px; animation-delay: 0.3s; }
.voice-bar:nth-child(9) { height: 16px; animation-delay: 0.2s; }
.voice-bar:nth-child(10) { height: 8px; animation-delay: 0.35s; }

@keyframes voiceWave {
    0% { transform: scaleY(0.3); opacity: 0.5; }
    100% { transform: scaleY(1); opacity: 1; }
}

/* ════════════════════════════════════════════
   SPEECH TEXT DISPLAY — NEW
   ════════════════════════════════════════════ */
.speech-display {
    margin-top: 1rem;
    padding: 0.8rem 1rem;
    background: rgba(57,255,20,0.05);
    border: 1px solid rgba(57,255,20,0.2);
    border-radius: 4px;
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: #39ff14;
    text-shadow: 0 0 5px rgba(57,255,20,0.5);
    line-height: 1.5;
    max-width: 260px;
    text-align: center;
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    width: 100%;
}

.speech-display.active {
    opacity: 1;
    transform: translateY(0);
}

.speech-display::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #39ff14, transparent);
    animation: speechScan 2s linear infinite;
}

@keyframes speechScan {
    0% { left: -100%; }
    100% { left: 100%; }
}

.speech-label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: rgba(57,255,20,0.6);
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

.speech-text {
    min-height: 1.2em;
}

/* ════════════════════════════════════════════
   PANEL BASE — Enhanced
   ════════════════════════════════════════════ */
.panel {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.2rem;
    height: 100%;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    animation: panelEntry 0.6s ease-out;
}

.panel::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.5;
    animation: panelScan 3s linear infinite;
}

.panel:hover {
    border-color: var(--border-hi);
    box-shadow: 0 0 20px rgba(0,255,231,0.05);
}

@keyframes panelEntry {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes panelScan {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.panel-title {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--text-lo);
    text-transform: uppercase;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.panel-title::before {
    content: '▸';
    color: var(--cyan);
    animation: blink 1s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ════════════════════════════════════════════
   WORKOUT PANEL — Enhanced
   ════════════════════════════════════════════ */
.workout-panel { height: 100%; }

.workout-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
}

.workout-day {
    font-family: var(--font-disp);
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: var(--text-hi);
}

.workout-pct {
    font-family: var(--font-mono);
    font-size: 1.4rem;
    font-weight: 700;
    animation: pctGlow 2s ease-in-out infinite;
}

@keyframes pctGlow {
    0%, 100% { text-shadow: 0 0 10px currentColor; }
    50% { text-shadow: 0 0 20px currentColor, 0 0 40px currentColor; }
}

.progress-track {
    height: 4px;
    background: var(--border);
    border-radius: 2px;
    margin-bottom: 1rem;
    overflow: hidden;
    position: relative;
}

.progress-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    animation: progressGlow 2s ease-in-out infinite;
}

.progress-fill::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 20px;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3));
    animation: progressShine 2s ease-in-out infinite;
}

@keyframes progressGlow {
    0%, 100% { box-shadow: 0 0 5px currentColor; }
    50% { box-shadow: 0 0 15px currentColor, 0 0 30px currentColor; }
}

@keyframes progressShine {
    0% { transform: translateX(0); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateX(20px); opacity: 0; }
}

.ex-list { 
    display: flex; 
    flex-direction: column; 
    gap: 0.5rem; 
    max-height: 420px; 
    overflow-y: auto; 
}

.ex-list::-webkit-scrollbar { width: 3px; }
.ex-list::-webkit-scrollbar-thumb { background: var(--border-hi); }
.ex-list::-webkit-scrollbar-track { background: transparent; }

.ex-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0.75rem;
    border-radius: 3px;
    border: 1px solid var(--border);
    background: var(--bg-card);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    animation: itemEntry 0.4s ease-out both;
}

.ex-item::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--cyan);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.ex-item:hover::before { opacity: 1; }
.ex-item:hover {
    border-color: var(--border-hi);
    transform: translateX(4px);
    box-shadow: -4px 0 15px rgba(0,255,231,0.1);
}

@keyframes itemEntry {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

.ex-pending  { border-color: var(--border); }
.ex-completed {
    border-color: #00ffe744;
    background: #00ffe708;
    opacity: 0.75;
    animation: completedPulse 2s ease-in-out infinite;
}
@keyframes completedPulse {
    0%, 100% { box-shadow: 0 0 5px #00ffe722; }
    50% { box-shadow: 0 0 15px #00ffe744; }
}
.ex-skipped {
    border-color: #ffffff11;
    opacity: 0.4;
}

.ex-icon {
    font-family: var(--font-mono);
    font-size: 0.9rem;
    width: 18px;
    text-align: center;
    color: var(--cyan);
    flex-shrink: 0;
    transition: all 0.3s ease;
}
.ex-item:hover .ex-icon { transform: scale(1.2); }
.ex-completed .ex-icon { color: #00ffe7; }
.ex-skipped   .ex-icon { color: var(--text-lo); }

.ex-info { flex: 1; min-width: 0; }
.ex-name {
    font-family: var(--font-disp);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-hi);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: all 0.3s ease;
}
.ex-completed .ex-name { text-decoration: line-through; color: var(--text-mid); }
.ex-skipped   .ex-name { text-decoration: line-through; color: var(--text-lo);  }
.ex-detail {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-lo);
    margin-top: 1px;
}

.cat-badge {
    font-family: var(--font-mono);
    font-size: 0.55rem;
    letter-spacing: 0.1em;
    padding: 2px 6px;
    border-radius: 2px;
    flex-shrink: 0;
    transition: all 0.3s ease;
}
.ex-item:hover .cat-badge { transform: scale(1.05); }

.cat-gym     { background: #003a5c; color: #00bfff; border: 1px solid #00bfff44; }
.cat-yoga    { background: #1a0a2e; color: #bf7fff; border: 1px solid #bf7fff44; }
.cat-running { background: #1a2600; color: #7fff00; border: 1px solid #7fff0044; }

.workout-empty, .weather-empty, .summary-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    min-height: 80px;
    gap: 0.5rem;
    color: var(--text-lo);
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    animation: emptyPulse 3s ease-in-out infinite;
}
@keyframes emptyPulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 0.8; }
}
.empty-icon { font-size: 1.5rem; opacity: 0.3; animation: iconFloat 3s ease-in-out infinite; }
@keyframes iconFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

/* ════════════════════════════════════════════
   WEATHER CARD — Enhanced
   ════════════════════════════════════════════ */
.weather-card {
    text-align: center;
    padding: 0.5rem;
    position: relative;
}
.weather-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border: 1px solid var(--border);
    border-radius: 4px;
    opacity: 0.3;
    animation: weatherBorder 4s ease-in-out infinite;
}
@keyframes weatherBorder {
    0%, 100% { border-color: var(--border); }
    50% { border-color: var(--cyan); }
}
.weather-tod {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--text-lo);
    text-transform: uppercase;
    animation: todFade 3s ease-in-out infinite;
}
@keyframes todFade {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}
.weather-day {
    font-family: var(--font-disp);
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--cyan);
    letter-spacing: 0.1em;
    text-shadow: 0 0 15px #00ffe766;
    animation: dayGlow 3s ease-in-out infinite;
}
@keyframes dayGlow {
    0%, 100% { text-shadow: 0 0 15px #00ffe766; }
    50% { text-shadow: 0 0 25px #00ffe7aa, 0 0 50px #00ffe744; }
}
.weather-time {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    color: var(--text-mid);
    margin-top: 0.2rem;
    animation: timeTick 1s ease-in-out infinite;
}
@keyframes timeTick {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* ════════════════════════════════════════════
   WEEKLY LOG — Enhanced
   ════════════════════════════════════════════ */
.log-panel { height: 100%; }
.log-streak {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--gold);
    margin-bottom: 0.8rem;
    letter-spacing: 0.05em;
    animation: streakGlow 2s ease-in-out infinite;
}
@keyframes streakGlow {
    0%, 100% { text-shadow: 0 0 5px #f5a62344; }
    50% { text-shadow: 0 0 15px #f5a62388; }
}
.log-grid { display: flex; flex-direction: column; gap: 0.3rem; }
.log-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.35rem 0.5rem;
    border-radius: 3px;
    border: 1px solid var(--border);
    background: var(--bg-card);
    transition: all 0.3s ease;
    animation: logEntry 0.3s ease-out both;
}
.log-row:hover {
    border-color: var(--border-hi);
    transform: translateX(3px);
}
@keyframes logEntry {
    from { opacity: 0; transform: translateX(-10px); }
    to { opacity: 1; transform: translateX(0); }
}
.log-today  { 
    border-color: var(--cyan); 
    background: #00ffe710; 
    animation: todayPulse 2s ease-in-out infinite;
}
@keyframes todayPulse {
    0%, 100% { box-shadow: 0 0 5px #00ffe722; }
    50% { box-shadow: 0 0 15px #00ffe744; }
}
.log-done   { border-color: #00ffe733; opacity: 0.7; }
.log-pending { opacity: 0.4; }
.log-day {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: var(--text-mid);
    width: 32px;
}
.log-today .log-day { color: var(--cyan); }
.log-icons {
    display: flex;
    gap: 0.6rem;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-lo);
}
.log-done .log-icons { color: #00ffe7aa; }

/* ════════════════════════════════════════════
   SESSION SUMMARY — Enhanced
   ════════════════════════════════════════════ */
.summary-panel {
    padding: 0.5rem;
    text-align: center;
    position: relative;
}
.summary-panel::before {
    content: '';
    position: absolute;
    inset: 0;
    border: 1px solid var(--cyan);
    border-radius: 4px;
    opacity: 0.2;
    animation: summaryBorder 3s ease-in-out infinite;
}
@keyframes summaryBorder {
    0%, 100% { opacity: 0.2; }
    50% { opacity: 0.4; }
}
.summary-title {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    color: var(--cyan);
    margin-bottom: 1rem;
    animation: titleGlow 2s ease-in-out infinite;
}
@keyframes titleGlow {
    0%, 100% { text-shadow: 0 0 5px #00ffe744; }
    50% { text-shadow: 0 0 15px #00ffe788; }
}
.summary-stats {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    margin-bottom: 0.8rem;
}
.stat-chip {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    padding: 4px 10px;
    border-radius: 2px;
    background: var(--bg-card);
    border: 1px solid var(--border-hi);
    color: var(--text-mid);
    transition: all 0.3s ease;
    animation: chipEntry 0.4s ease-out both;
}
.stat-chip:hover {
    border-color: var(--cyan);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,255,231,0.1);
}
@keyframes chipEntry {
    from { opacity: 0; transform: scale(0.8); }
    to { opacity: 1; transform: scale(1); }
}
.total-chip { 
    border-color: var(--cyan); 
    color: var(--cyan); 
    animation: totalPulse 2s ease-in-out infinite;
}
@keyframes totalPulse {
    0%, 100% { box-shadow: 0 0 5px #00ffe722; }
    50% { box-shadow: 0 0 15px #00ffe744; }
}
.summary-note {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-lo);
    letter-spacing: 0.05em;
    animation: noteFade 4s ease-in-out infinite;
}
@keyframes noteFade {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}

/* ════════════════════════════════════════════
   VOICE COMMANDS — Enhanced
   ════════════════════════════════════════════ */
.commands-panel {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-lo);
    line-height: 2;
    letter-spacing: 0.05em;
}
.command-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.2rem 0;
    transition: all 0.3s ease;
    cursor: default;
}
.command-item:hover {
    color: var(--cyan);
    transform: translateX(5px);
}
.command-item::before {
    content: '>';
    color: var(--cyan);
    opacity: 0;
    transition: opacity 0.3s ease;
}
.command-item:hover::before { opacity: 1; }
.command-quote {
    color: var(--text-mid);
    transition: color 0.3s ease;
}
.command-item:hover .command-quote {
    color: var(--cyan);
    text-shadow: 0 0 5px var(--cyan);
}

/* ════════════════════════════════════════════
   NEWS HEADLINES — NEW
   ════════════════════════════════════════════ */
.news-section {
    margin-top: 16px;
    padding: 0 2px;
}

.news-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 3px;
    color: var(--text-lo);
    text-transform: uppercase;
    margin-bottom: 12px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(0, 255, 231, 0.08);
}

.news-indicator {
    color: var(--cyan);
    font-size: 7px;
    animation: newsPulse 2s ease-in-out infinite;
}

@keyframes newsPulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.news-loading, .news-empty {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-lo);
    padding: 14px 0;
    text-align: center;
    letter-spacing: 1px;
}

.news-cards-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.news-card {
    position: relative;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 12px;
    background: var(--bg-card);
    border: 1px solid rgba(0, 255, 231, 0.06);
    border-radius: 6px;
    overflow: hidden;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: default;
}

.news-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 2px;
    height: 100%;
    background: linear-gradient(180deg, var(--cyan) 0%, var(--text-lo) 100%);
    opacity: 0;
    transition: opacity 0.25s ease;
}

.news-card:hover {
    background: rgba(0, 255, 231, 0.04);
    border-color: rgba(0, 255, 231, 0.12);
    transform: translateX(3px);
}

.news-card:hover::before {
    opacity: 1;
}

.news-rank {
    font-family: var(--font-mono);
    font-size: 16px;
    font-weight: 700;
    line-height: 1;
    opacity: 0.7;
    min-width: 22px;
    text-align: center;
    margin-top: 2px;
    flex-shrink: 0;
}

.news-content {
    flex: 1;
    min-width: 0;
}

.news-headline {
    font-family: var(--font-disp);
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-mid);
    line-height: 1.5;
    margin: 0 0 4px 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    transition: color 0.25s ease;
}

.news-card:hover .news-headline {
    color: var(--text-hi);
}

.news-meta {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: var(--font-mono);
    font-size: 0.55rem;
    letter-spacing: 0.5px;
}

.news-source {
    color: var(--cyan);
    font-weight: 500;
    text-transform: uppercase;
}

.news-dot {
    color: var(--text-lo);
    font-size: 6px;
}

.news-time {
    color: var(--text-lo);
}

.news-glow {
    position: absolute;
    top: -50%;
    right: -15px;
    width: 60px;
    height: 200%;
    opacity: 0;
    filter: blur(30px);
    transition: opacity 0.3s ease;
    pointer-events: none;
}

.news-card:hover .news-glow {
    opacity: 0.05;
}

/* ════════════════════════════════════════════
   GRADIO OVERRIDES
   ════════════════════════════════════════════ */
.gradio-container .prose  { color: var(--text-hi) !important; }
footer                    { display: none !important; }
.gr-button                { display: none !important; }
#component-0              { background: var(--bg-deep) !important; }
.svelte-1gfkn6j           { background: var(--bg-deep) !important; }

/* Ensure panels stack correctly in Gradio */
.gradio-container .panel {
    margin-bottom: 1rem;
}
"""


# ════════════════════════════════════════════
# GRADIO UI BUILDER
# ════════════════════════════════════════════

def launch_ui(controller=None):

    def refresh():
        state    = read_state()
        orb      = build_orb_html(state)
        workout  = build_workout_html(state)
        weather  = build_weather_html(state)
        log      = build_log_html(state)
        summary  = build_summary_html(state)
        news     = build_news_html()
        return orb, workout, weather, log, summary, news

    with gr.Blocks(title="JarvisFit", css=CSS) as app:

        # ── header ──────────────────────────
        gr.HTML("""
        <div class="fj-header">
            <div class="fj-title">JarvisFit</div>
            <div class="fj-subtitle">VOICE · ACTIVATED · FITNESS · INTELLIGENCE</div>
        </div>
        """)

        # ── main layout ─────────────────────
        with gr.Row():

            # LEFT — orb + weather + log
            with gr.Column(scale=1, min_width=280):

                gr.HTML('<div class="panel-title">SYSTEM STATUS</div>')
                orb_html = gr.HTML(
                    value=build_orb_html(read_state()),
                    elem_id="orb-display",
                )

                gr.HTML('<div style="height:1rem;"></div>')

                gr.HTML('<div class="panel-title">SESSION INFO</div>')
                weather_html = gr.HTML(
                    value=build_weather_html(read_state()),
                    elem_id="weather-display",
                )

                gr.HTML('<div style="height:1rem;"></div>')

                gr.HTML('<div class="panel-title">WEEKLY LOG</div>')
                log_html = gr.HTML(
                    value=build_log_html(read_state()),
                    elem_id="log-display",
                )

            # CENTER — workout list
            with gr.Column(scale=2, min_width=340):

                gr.HTML('<div class="panel-title">TODAY\'S WORKOUT</div>')
                workout_html = gr.HTML(
                    value=build_workout_html(read_state()),
                    elem_id="workout-display",
                )

            # RIGHT — session summary + commands
            with gr.Column(scale=1, min_width=280):

                gr.HTML('<div class="panel-title">SESSION SUMMARY</div>')
                summary_html = gr.HTML(
                    value=build_summary_html(read_state()),
                    elem_id="summary-display",
                )

                gr.HTML('<div style="height:1rem;"></div>')

                gr.HTML('<div class="panel-title">VOICE COMMANDS</div>')
                gr.HTML("""
                <div class="commands-panel">
                    <div class="command-item">
                        <span class="command-quote">"Hello Jarvis"</span> — Wake
                    </div>
                    <div class="command-item">
                        <span class="command-quote">"Let's start"</span> — Begin
                    </div>
                    <div class="command-item">
                        <span class="command-quote">"Push ups done"</span> — Complete
                    </div>
                    <div class="command-item">
                        <span class="command-quote">"Skip bench"</span> — Skip
                    </div>
                    <div class="command-item">
                        <span class="command-quote">"What's next"</span> — Next
                    </div>
                    <div class="command-item">
                        <span class="command-quote">"How am I doing"</span> — Progress
                    </div>
                    <div class="command-item">
                        <span class="command-quote">"Jarvis pause"</span> — Pause
                    </div>
                    <div class="command-item">
                        <span class="command-quote">"Let's continue"</span> — Resume
                    </div>
                    <div class="command-item">
                        <span class="command-quote">"Jarvis off"</span> — Sleep
                    </div>
                </div>
                """)
                gr.HTML('<div style="height:1rem;"></div>')

                gr.HTML('<div class="panel-title">HEADLINES</div>')
                news_html = gr.HTML(
                    value=build_news_html(),
                    elem_id="news-display",
                )

        # ── auto refresh every 2 seconds ────
        refresh_timer = gr.Timer(value=2)
        refresh_timer.tick(
            fn=refresh,
            outputs=[orb_html, workout_html, weather_html, log_html, summary_html, news_html],
        )

    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        quiet=False,
        prevent_thread_lock=False,
        theme=gr.themes.Base(
            primary_hue="cyan",
            neutral_hue="slate",
        )
    )
