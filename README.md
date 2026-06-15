```
     ██╗  █████╗  ██████╗  ██╗   ██╗ ██╗ ███████╗    ███████╗ ██╗ ████████╗
     ██║ ██╔══██╗ ██╔══██╗ ██║   ██║ ██║ ██╔════╝    ██╔════╝ ██║ ╚══██╔══╝
     ██║ ███████║ ██████╔╝ ██║   ██║ ██║ ███████╗    █████╗   ██║    ██║   
██   ██║ ██╔══██║ ██╔══██╗ ╚██╗ ██╔╝ ██║ ╚════██║    ██╔══╝   ██║    ██║   
╚█████╔╝ ██║  ██║ ██║  ██║  ╚████╔╝  ██║ ███████║    ██║      ██║    ██║   
 ╚════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝   ╚═══╝   ╚═╝ ╚══════╝    ╚═╝      ╚═╝    ╚═╝
```

### 🔥 Your Personal Iron Man. But Make It Gains.

*"Hey Jarvis — let's get after it."* 💪

[Python](https://python.org)
[CrewAI](https://crewai.com)
[Gemini](https://ai.google.dev)
[Gradio](https://gradio.app)

---

## 🚀 What Is JarvisFit?

You roll out of bed. Groggy. Unmotivated. Zero interest in counting reps.

You say two words: **"Hey Jarvis."**

And just like that — your AI fitness assistant snaps to life. It checks the weather for you. Reads you this morning's top headlines. Reminds you it's **leg day** (sorry). Walks you through every single exercise, one by one, at your pace. You finish a set, you just say *"squats done"* — Jarvis marks it, tells you what's next, and keeps the momentum going so you never have to think.

When the last rep is done, it doesn't just let you walk away. It hands you a **fully personalized nutrition plan** — exactly how much protein to eat, how much water to drink, what to have for dinner, and even reminds you to take your zinc tonight for deeper sleep and faster recovery.

Then, with the energy of a butler who's extremely proud of you, it says —

> *"Amazing work. Have a great day. Jarvis going to sleep."* 😴

And waits. Quietly. Loyally. Ready to do it all again tomorrow.

**JarvisFit is not a fitness tracker. It is not a workout app. It is the AI training partner you always wished existed** — built with CrewAI multi-agent orchestration, Google Gemini 2.5 Flash, real-time voice I/O, and a living Iron Man–inspired UI that pulses and glows with every command.

No tapping. No scrolling. No excuses.

Just you, your voice, and Jarvis.

> 🦾 *Inspired by J.A.R.V.I.S. from Iron Man. Built for humans who actually show up.*
>
> ⭐ *If this made you want to go work out right now — you already know what to do.*

---

## 🎬 Demo Flow

```
You  →  "Hey Jarvis"
         ↓
Jarvis  →  "Good morning Abhi. Today is Friday, June 13th.
            It is 7:20 AM. In Bengaluru, 26°C with partly cloudy skies.
            Here are your top headlines...
            How would you like to start your day?"
         ↓
You  →  "Let's start the workout"
         ↓
Jarvis  →  "Here is your plan for today, Friday. Focus is Full Body Strength.
            4 gym exercises, 1 yoga pose, 1 running activity.
            Let's get started. Your first exercise is Deadlifts."
         ↓
You  →  "Deadlifts done"
         ↓
Jarvis  →  "Great work on Deadlifts! Next up is Push Ups.
            After that, move on to Goblet Squats."
         ↓
         ... (session continues) ...
         ↓
Jarvis  →  "Amazing work! You've completed all exercises for today.
            Here's your nutrition summary: aim for 140g of protein today,
            drink 4 litres of water. Post-workout meal: chicken rice bowl...
            Take 11mg of zinc 30 minutes before bed for better sleep.
            Have a great day Abhi. Jarvis going to sleep. Goodbye."
```

Demo Video : [https://drive.google.com/file/d/15mfVrOciCaxwIEIxsnBcOC0z_I-AZcZj/view?usp=drive_link](https://drive.google.com/file/d/15mfVrOciCaxwIEIxsnBcOC0z_I-AZcZj/view?usp=drive_link)

---

## 🚀 Features


| Feature                       | Description                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| 🎙️ **Wake Word Detection**   | "Hey Jarvis" / "Hello Jarvis" triggers the full morning sequence                    |
| 🌤️ **Live Weather Briefing** | Auto-detects your city via IP, fetches real-time weather from OpenWeatherMap        |
| 📰 **Morning Headlines**      | Top 3 health, sports, and general news from newsdata.io                             |
| 📅 **Dynamic Daily Plans**    | Loads the right workout for today automatically — no manual selection               |
| ✅ **Voice Exercise Tracking** | Say "Push ups done" — Jarvis marks it, suggests what's next                         |
| ⏭️ **Skip Exercises**         | "Skip bench press today" — skips and moves on                                       |
| 📊 **Live Progress**          | "How am I doing?" — hear your completion percentage in real time                    |
| ⏸️ **Pause & Resume**         | "Jarvis pause" / "Let's continue" — full session control                            |
| 🧠 **Fitness Q&A**            | Ask any fitness question mid-workout — Gemini answers in 2-3 sentences              |
| 🥗 **Nutrition Summary**      | Post-workout protein, water, meal suggestions, vitamins, and zinc intake            |
| 📆 **Day Completion Memory**  | Say "Hey Jarvis" after finishing — it knows you're done and switches to free assist |
| 🔄 **Weekly Auto-Reset**      | Every Monday, all completion flags reset for a fresh week                           |
| 🔥 **Streak Tracking**        | Consecutive day streak tracked and spoken at session end                            |
| 🌑 **Living Gradio UI**       | Animated Iron Man–style orb, real-time workout list, weekly log, session summary    |
| 😴 **Graceful Sleep**         | "Jarvis Turn Off" ends the session cleanly with goodbye                             |


---

## 🏗️ Architecture

JarvisFit uses a **hybrid architecture** — CrewAI for structured reasoning and Python for real-time event loops.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          JARVISFIT ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   MAIN THREAD                                                           │
│   ├── JarvisFitController.kickoff()  →  Thread-1 (daemon)              │
│   └── launch_ui()  →  Gradio at localhost:7860  (blocks main thread)    │
│                                                                         │
│   THREAD-1: Wake Listener (daemon)                                      │
│   ├── VoiceListener.listen_for_wake_word()                              │
│   ├── session_active_flag → pauses when session is running              │
│   └── on "Hey Jarvis" → calls on_wake()                                 │
│                                                                         │
│   on_wake() SEQUENCE:                                                   │
│   ├── WakeSequenceCrew.kickoff()  ← CrewAI (only crew in production)    │
│   │   └── greeter_agent: LocationTool → WeatherTool →                   │
│   │       DateTimeTool → NewsTool → returns structured data             │
│   ├── Python builds greeting string → speak_with_state()               │
│   ├── load_todays_exercises(day_name)                                   │
│   └── _await_start_confirmation()                                       │
│                                                                         │
│   THREAD-2: Session Loop (daemon)                                       │
│   ├── run_session_loop(stop_flag, listener)                             │
│   ├── listen_once() → IntentParserTool (Gemini) → route intent         │
│   ├── exercise_completed → mark_exercise() → run_recommendation()      │
│   ├── All done → run_end_session() → run_diet_advice()                  │
│   └── session_active_flag.clear() → Thread-1 resumes                   │
│                                                                         │
│   GRADIO UI                                                             │
│   └── gr.Timer(2s) polls session_state.json → rebuilds 5 HTML panels   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Why Hybrid? (CrewAI + Python)

> CrewAI is powerful for **structured reasoning tasks** with a defined start and end. It is not designed for **continuous real-time loops**. During development, using CrewAI for the session loop caused 3–5 second delays per agent turn, LLM retry loops, and empty response crashes. The solution: CrewAI handles what it's best at (composing the morning greeting from multiple data sources), and Python handles what it's best at (fast, event-driven voice interaction).

---

## 🤖 Crew & Agent Design

### Active CrewAI Crew

#### `WakeSequenceCrew` — Morning Greeting

The only active CrewAI crew. Fires on every wake event.

```
WakeSequenceCrew
└── greeter_agent  (Personalized Morning Greeter)
    ├── Task: greet_user_task
    ├── Tools: LocationTool, WeatherTool, DateTimeTool, NewsTool
    └── Output: Structured data (city, temp, condition, day, headlines)
         ↓
    Python constructs greeting → speak_with_state(greeting)
```


### Python-Driven Agents (formerly CrewAI)

These were originally CrewAI agents but were moved to Python functions for reliability:


| Original Agent          | Python Replacement                                                      | Reason                                         |
| ----------------------- | ----------------------------------------------------------------------- | ---------------------------------------------- |
| `workout_manager_agent` | `load_todays_exercises()`, `mark_exercise()`, `get_pending_exercises()` | Deterministic state operations — no LLM needed |
| `recommendation_agent`  | `run_recommendation()`                                                  | Pure list lookup — 0ms vs 2-5s LLM call        |
| `diet_advisor_agent`    | `run_diet_advice()` + `DietRulesTool`                                   | Rule-based formulas — no reasoning needed      |
| `listener_agent`        | `VoiceListener` class                                                   | Hardware interface — cannot be a CrewAI agent  |


---

## 🗣️ Voice Intent System

Every utterance during an active session is classified by **Gemini 2.5 Flash** via `IntentParserTool`:

```
User says something
       ↓
IntentParserTool (Gemini 2.5 Flash)
       ↓
Returns JSON: { "intent": "exercise_completed", "exercise_name": "Push Ups" }
       ↓
Session loop routes to the correct handler
```


| Intent               | Example Phrases                              | Action                         |
| -------------------- | -------------------------------------------- | ------------------------------ |
| `exercise_completed` | "Push ups done", "I finished squats"         | Mark complete + recommend next |
| `exercise_skipped`   | "Skip bench press", "Not doing plank today"  | Mark skipped + recommend next  |
| `request_plan`       | "What's my workout?", "What do I have left?" | Speak remaining exercises      |
| `request_progress`   | "How am I doing?", "What's my progress?"     | Speak % complete + count       |
| `request_next`       | "What's next Jarvis?", "Next exercise"       | Speak next 1-2 exercises       |
| `start_workout`      | "Let's go", "Begin", "Start"                 | Speak first exercise           |
| `pause_session`      | "Jarvis pause", "Give me a break"            | Enter pause loop               |
| `resume_session`     | "Let's continue", "I'm back"                 | Resume from pause              |
| `fitness_question`   | "How many calories does a squat burn?"       | Gemini direct answer           |
| `unknown`            | Anything unrecognized                        | "Sorry, could you repeat?"     |


---

## 🛠️ Tech Stack


| Layer                  | Technology                  | Purpose                                                  |
| ---------------------- | --------------------------- | -------------------------------------------------------- |
| **Agent Framework**    | CrewAI 0.100+               | Multi-agent orchestration, YAML-driven agent/task config |
| **LLM**                | Gemini 2.5 Flash            | Intent parsing, greeting composition, fitness Q&A        |
| **Voice Input (STT)**  | SpeechRecognition + PyAudio | Google Speech-to-Text backend, mic capture               |
| **Voice Output (TTS)** | pyttsx3                     | Offline, zero-cost, OS-native voices                     |
| **UI Framework**       | Gradio 5.0+                 | Dark-themed living interface, 2s auto-refresh            |
| **Weather**            | OpenWeatherMap API          | Real-time temperature and conditions                     |
| **News**               | newsdata.io API             | Top 3 headlines (health, sports, general)                |
| **Location**           | ipinfo.io                   | Free IP-based city + coordinates detection               |
| **LLM SDK**            | google-genai                | Native Google GenAI SDK (not deprecated generativeai)    |
| **Config**             | python-dotenv               | Environment variable management                          |
| **Data**               | JSON files                  | Workout plan, session state, diet rules                  |
| **Concurrency**        | Python threading            | Daemon threads for listener + session loop               |


---

## 📁 Project Structure

```
jarvisfit/
│
├── src/
│   └── jarvisfit/
│       ├── config/
│       │   ├── agents.yaml                  ← Agent definitions (role, goal, backstory)
│       │   ├── wake_tasks.yaml              ← greet_user_task definition
│       │   └── settings.py                  ← API keys, constants, wake/sleep phrases
│       │
│       ├── tools/
│       │   ├── weather_tool.py              ← OpenWeatherMap API
│       │   ├── location_tool.py             ← ipinfo.io IP geolocation
│       │   ├── datetime_tool.py             ← Current date, time, day, greeting period
│       │   ├── news_tool.py                 ← newsdata.io top 3 headlines
│       │   ├── workout_plan_loader_tool.py  ← Load today's plan from JSON
│       │   ├── session_state_tool.py        ← Read/write session_state.json
│       │   ├── intent_parser_tool.py        ← Gemini intent classification
│       │   ├── diet_rules_tool.py           ← Rule-based nutrition calculator
│       │   ├── speaker_tool.py              ← pyttsx3 TTS playback
│       │   └── voice_listener_tool.py       ← Microphone input capture
│       │
│       ├── voice/
│       │   └── listener.py                  ← Wake word loop + listen_once()
│       │
│       ├── ui/
│       │   └── gradio_app.py                ← Living Gradio UI (CSS, HTML, auto-refresh)
│       │
│       ├── data/
│       │   ├── workout_plan.json            ← 7-day weekly workout plan (Beginner)
│       │   ├── session_state.json           ← Runtime state (resets on launch)
│       │   └── diet_rules.json              ← Nutrition formulas and meal suggestions
│       │
│       ├── crew.py                          ← Crews, session loop, controller, helpers
│       └── main.py                          ← Entry point
│
├── output/                                  ← Session logs
├── .env                                     ← API keys (gitignored)
├── pyproject.toml
└── README.md
```

---

## 🔧 Installation

### Prerequisites

- Python 3.10–3.13
- A microphone connected and accessible
- API keys for Gemini, OpenWeatherMap, and newsdata.io

**Install PortAudio (required for PyAudio):**

```bash
# Ubuntu / WSL
sudo apt-get install portaudio19-dev

# macOS
brew install portaudio

# Windows
pip install pipwin
pipwin install pyaudio
```

---

### Step-by-Step Setup

> JarvisFit uses **uv** as the package manager. If you don't have it yet, install it first.

**0. Install uv (one-time setup)**

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

---

**1. Clone the repository**

```bash
git clone https://github.com/abhishekpoddar29/Jarvis-Fit.git
cd jarvisfit
```

---

**2. Create a virtual environment with uv**

```bash
uv venv
```

This creates a `.venv` folder in your project root. Now activate it:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.venv\Scripts\activate.bat
```

You should see `(jarvisfit)` or `(.venv)` appear in your terminal prompt confirming the environment is active.

---

**3. Install dependencies**

```bash
uv pip install -e .
```

This installs JarvisFit in editable mode along with all dependencies defined in `pyproject.toml`.

If you ever add new packages to `pyproject.toml` later, run:

```bash
uv sync
```

---

**4. Install PortAudio (required for PyAudio / microphone)**

PyAudio needs PortAudio installed at the system level before it can work.

```bash
# Ubuntu / Debian / WSL
sudo apt-get install portaudio19-dev

# macOS
brew install portaudio

# Windows
# PortAudio is bundled via pipwin — run this inside your activated venv:
uv pip install pipwin
pipwin install pyaudio
```

---

**5. Set up your API keys**

Create a `.env` file in the project root (same level as `pyproject.toml`):

```bash
# macOS / Linux
touch .env

# Windows
type nul > .env
```

Open `.env` and add your keys:

```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
NEWSDATA_API_KEY=your_newsdata_api_key_here
```

Get your keys here:


| Key                       | Where to get it                                                      | Cost                 |
| ------------------------- | -------------------------------------------------------------------- | -------------------- |
| 🔑 `GEMINI_API_KEY`       | [aistudio.google.com](https://aistudio.google.com) → Get API Key     | Free tier available  |
| 🌤️ `OPENWEATHER_API_KEY` | [openweathermap.org/api](https://openweathermap.org/api) → Free tier | 1,000 calls/day free |
| 📰 `NEWSDATA_API_KEY`     | [newsdata.io](https://newsdata.io) → Sign up                         | 200 credits/day free |


---

**6. Update your name**

Open `src/jarvisfit/config/settings.py` and set your name and body weight:

```python
USER_NAME            = "YourName"   # Jarvis greets you by this name
```

Open `src/jarvisfit/tools/diet_rules_tool.py` and update your weight for accurate protein calculation:

```python
body_weight_kg = 70.0   # replace with your actual weight in kg
```

---

**7. Run JarvisFit**

```bash
# Recommended — uses pyproject.toml entry point
crewai run

# Alternative — run directly
python src/jarvisfit/main.py
```

You should see: 
[jarvisfit] System online. Waiting for wake word...

[VoiceListener] Listening for wake word...

[jarvisfit] System online. Launching UI at [http://localhost:7860](http://localhost:7860)

---

**8. Open the UI**

Navigate to [http://localhost:7860](http://localhost:7860) in your browser. You will see the animated orb in **SLEEPING** state.

---

**9. Wake Jarvis up**

Make sure your microphone is on, then say clearly: "Hey Jarvis"

---

## 🎮 Voice Commands


| Say This                     | What Happens                                     |
| ---------------------------- | ------------------------------------------------ |
| `"Hello Jarvis"`             | Wakes Jarvis — morning briefing begins           |
| `"Let's start the workout"`  | Begins the workout session                       |
| `"[Exercise] done"`          | Marks exercise complete — e.g. *"Push ups done"* |
| `"[Exercise] completed"`     | Same as above — e.g. *"Bench press completed"*   |
| `"Skip [exercise]"`          | Skips an exercise — e.g. *"Skip plank today"*    |
| `"What's next Jarvis"`       | Get your next 1-2 exercises                      |
| `"What is my workout today"` | Hear all remaining exercises                     |
| `"How am I doing"`           | Hear your progress percentage                    |
| `"Jarvis pause"`             | Pause the session                                |
| `"Let's continue"`           | Resume after a pause                             |
| `"[Any fitness question]"`   | Ask anything — Gemini answers directly           |
| `"Jarvis Turn Off"`          | Ends session, delivers nutrition summary, sleeps |


---

### Orb States


| Orb Color            | State              | Meaning                     |
| -------------------- | ------------------ | --------------------------- |
| 🔵 Dark navy, dim    | **SLEEPING**       | Jarvis is not awake         |
| 🟠 Orange / Red fire | **LISTENING**      | Waiting for your voice      |
| 🟢 Green             | **SPEAKING**       | Jarvis is talking           |
| 🔵 Cyan / Blue       | **ACTIVE SESSION** | Workout in progress         |
| 🟡 Amber / Gold      | **PAUSED**         | Session paused              |
| 🔵 Teal              | **AWAKE**          | Awake but no active session |


---

## 🥗 Nutrition System

Protein is calculated as **body weight (kg) × 2 grams**. Update your weight in `diet_rules_tool.py`:

```python
body_weight_kg=70.0   # change to your weight
```

Each post-workout summary includes:

- 💪 **Protein target** in grams (weight × 2)
- 🔥 **Calories burned** (calculated per exercise from lookup table)
- 💧 **Water intake** (3.0–4.0L depending on workout intensity)
- 🥗 **Meal suggestions** (pre-workout, post-workout, dinner, snacks)
- 💊 **Vitamins** (C, D, B12, Magnesium, Omega-3)
- 😴 **Zinc** (11mg nightly, timed 30 mins before bed for better sleep)

---

## ⚠️ Important Rules for Developers

**Do's:**

- Always call `speak_with_state()` instead of `speaker_tool._run()` directly — this keeps the orb in sync
- Use `from google import genai` — the `google.generativeai` package is deprecated
- Always pass the shared `VoiceListener` instance — never create a new one inside the session loop
- Use `thinking={"thinking_budget": 0}` on the LLM — disables Gemini thinking tokens for CrewAI
**Don'ts:**
- Don't add `SpeakerTool` to `greeter_agent` tools in `WakeSequenceCrew` — causes LLM retry loops
- Don't use `{curly_braces}` in YAML task descriptions — CrewAI treats them as template variables
- Don't commit `session_state.json` to git — it's runtime state and will cause merge conflicts
- Don't create multiple `VoiceListener` instances — causes audio device crashes on Windows

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Built with ❤️ and way too many voice commands**

*"The truth is... I am Iron-Man."*

⭐ Star this repo if Jarvis made you actually work out
