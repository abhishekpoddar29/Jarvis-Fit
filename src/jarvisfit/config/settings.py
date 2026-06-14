import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# USER CONFIG
# ─────────────────────────────────────────────

USER_NAME = "Abhi"

# ─────────────────────────────────────────────
# LLM CONFIG
# ─────────────────────────────────────────────

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL   = "gemini-2.5-flash-lite"


NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
NEWSDATA_URL     = "https://newsdata.io/api/1/latest?"
# ─────────────────────────────────────────────
# WEATHER CONFIG
# ─────────────────────────────────────────────

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_URL     = "https://api.openweathermap.org/data/2.5/weather"

# ─────────────────────────────────────────────
# LOCATION CONFIG
# ─────────────────────────────────────────────

IPINFO_URL = "https://ipinfo.io/json"

# ─────────────────────────────────────────────
# VOICE TRIGGER PHRASES
# ─────────────────────────────────────────────

WAKE_PHRASES = [
    "Hi jarvis",
    "Jarvis awake",
    "wake up Jarvis",
    "hello jarvis",
    "hey jarvis",
    "jarvis wake up",
]

SHUTDOWN_PHRASES = [
    "jarvis turn off",
    "Bye Jarvis",
    "Jarvis off",
    "Jarvis sleep",
    "Terminate workout"
    "jarvis shutdown",
    "goodbye jarvis",
    "jarvis stop",
]

# ─────────────────────────────────────────────
# SESSION CONFIG
# ─────────────────────────────────────────────

SESSION_RESET_DAY   = "Monday"
FRESH_SESSION_ON_LAUNCH = True

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────

BASE_DIR         = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR         = os.path.join(BASE_DIR, "data")
SESSION_PATH     = os.path.join(DATA_DIR, "session_state.json")
WORKOUT_PLAN_PATH = os.path.join(DATA_DIR, "workout_plan.json")
DIET_RULES_PATH  = os.path.join(DATA_DIR, "diet_rules.json")
OUTPUT_DIR       = os.path.join(os.path.dirname(BASE_DIR), "output")