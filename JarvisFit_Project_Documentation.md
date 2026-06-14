
# JARVISFIT — PROJECT DOCUMENTATION
## Voice-Activated Fitness Intelligence System

---

## 1. EXECUTIVE SUMMARY

**JarvisFit** is a voice-activated, AI-powered fitness assistant inspired by the J.A.R.V.I.S. interface from Iron Man. It combines CrewAI multi-agent orchestration with a real-time Gradio web UI to deliver a hands-free workout companion that greets users, presents daily workout plans, tracks exercise progress via voice commands, and provides personalized nutrition advice — all through natural speech interaction.

**Core Paradigm:** The system operates on a **wake-sleep cycle** controlled by voice. When dormant, it listens for the wake phrase "Hey Jarvis." Once awakened, it enters a conversational session loop where users can complete exercises, skip them, ask fitness questions, pause/resume, and end sessions — all via voice.

---

## 2. FUNCTIONAL REQUIREMENTS

### 2.1 Voice Interaction System

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-001 | **Wake Word Detection:** Continuously listen for "Hey Jarvis" or configured wake phrases | P0 | ✅ Implemented |
| FR-002 | **Shutdown Detection:** Listen for "Jarvis off," "goodbye," "sleep" to end session | P0 | ✅ Implemented |
| FR-003 | **Intent Classification:** Parse user utterances into structured intents (start, complete, skip, pause, resume, progress, plan, question) | P0 | ✅ Implemented |
| FR-004 | **Text-to-Speech (TTS):** Speak responses aloud using pyttsx3 (offline, zero cost) | P0 | ✅ Implemented |
| FR-005 | **Speech-to-Text (STT):** Capture user voice via microphone using SpeechRecognition + PyAudio | P0 | ✅ Implemented |
| FR-006 | **Session Loop Listening:** During active workout, listen for exercise completion/skip commands with 8-second timeout | P0 | ✅ Implemented |

### 2.2 Workout Management

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-007 | **Daily Plan Loading:** Load gym, yoga, and running exercises for the current day from JSON plan | P0 | ✅ Implemented |
| FR-008 | **Exercise Tracking:** Mark exercises as completed, skipped, or pending | P0 | ✅ Implemented |
| FR-009 | **Progress Calculation:** Calculate completion percentage across all categories | P0 | ✅ Implemented |
| FR-010 | **Next Exercise Recommendation:** Automatically suggest the next exercise after completion | P0 | ✅ Implemented |
| FR-011 | **Session Persistence:** Save session state (start time, end time, completed exercises) to JSON | P0 | ✅ Implemented |
| FR-012 | **Weekly Reset:** Automatically reset weekly progress on Monday | P1 | ✅ Implemented |
| FR-013 | **Streak Tracking:** Maintain consecutive-day completion streak | P1 | ✅ Implemented |
| FR-014 | **Daily Log:** Record gym/yoga/running completion per day | P1 | ✅ Implemented |

### 2.3 Intelligence & Context

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-015 | **Weather Integration:** Fetch current weather for user's location (OpenWeatherMap) | P0 | ✅ Implemented |
| FR-016 | **Location Detection:** Determine user's city/coordinates | P0 | ✅ Implemented |
| FR-017 | **DateTime Awareness:** Know current day, date, time, greeting period (morning/afternoon/evening) | P0 | ✅ Implemented |
| FR-018 | **News Headlines:** Fetch top 3 health/fitness/sports headlines from NewsData.io | P1 | ✅ Implemented |
| FR-019 | **Diet/Nutrition Advice:** Generate personalized post-workout nutrition summary based on completed exercises | P0 | ✅ Implemented |
| FR-020 | **Fitness Q&A:** Answer general fitness questions using Gemini LLM | P1 | ✅ Implemented |
| FR-021 | **Free Assist Mode:** When workout is already complete, allow open-ended fitness Q&A | P1 | ✅ Implemented |

### 2.4 UI & Visualization

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-022 | **Iron Man Orb:** Animated central orb that changes color based on state (sleeping, awake, listening, speaking, active, paused) | P0 | ✅ Implemented |
| FR-023 | **State Visualization:** Display system status, session info, weekly log, workout list, session summary | P0 | ✅ Implemented |
| FR-024 | **Voice Wave Animation:** Visual audio wave when listening for commands | P0 | ✅ Implemented |
| FR-025 | **Speech Text Display:** Show text being spoken by Jarvis in real-time | P0 | ✅ Implemented |
| FR-026 | **News Headlines Cards:** Display top 3 news as styled cards below Voice Commands | P1 | ✅ Implemented |
| FR-027 | **Auto-Refresh:** UI polls state every 2 seconds for real-time updates | P0 | ✅ Implemented |
| FR-028 | **Progress Bar:** Visual completion percentage for today's workout | P0 | ✅ Implemented |

### 2.5 State Management

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-029 | **Atomic State Writes:** All state changes go through SessionStateWriterTool | P0 | ✅ Implemented |
| FR-030 | **State Read:** UI reads from shared JSON state file | P0 | ✅ Implemented |
| FR-031 | **Speaking State:** Dedicated state for TTS (green orb + text display) | P0 | ✅ Implemented |
| FR-032 | **Listening State:** Orange orb when awaiting user command | P0 | ✅ Implemented |

---

## 3. TECHNOLOGY STACK & FLOW

### 3.1 Core Technologies

```
┌─────────────────────────────────────────────────────────────────┐
│                    JARVISFIT TECHNOLOGY STACK                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   GRADIO     │    │   CREWAI     │    │   GEMINI     │       │
│  │   (UI)       │◄──►│  (Agents)    │◄──►│   (LLM)      │       │
│  │  v5.0+       │    │  v0.100+     │    │  2.5 Flash   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         ▲                   ▲                   ▲                │
│         │                   │                   │                │
│         │            ┌──────────────┐           │                │
│         │            │  PYTHON 3.12 │           │                │
│         │            │  Threading   │           │                │
│         │            │  Event-Driven│           │                │
│         │            └──────────────┘           │                │
│         │                   │                   │                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   PYTTSX3    │    │SPEECHRECOGN. │    │  NEWSDATA    │       │
│  │   (TTS)      │    │   (STT)      │    │    API       │       │
│  │  Offline     │    │  + PyAudio   │    │  Headlines   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  OPENWEATHER │    │   JSON       │    │   DOTENV     │       │
│  │    MAP API   │    │   State      │    │   Secrets    │       │
│  │  Weather     │    │   File       │    │   Config     │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW PIPELINE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  USER VOICE ──► SpeechRecognition ──► Text ──► IntentParserTool     │
│     ▲                                              │                 │
│     │                                              ▼                 │
│  SpeakerTool ◄── TTS ◄── Response Text ◄── CrewAI Agents            │
│  (pyttsx3)         │                              │                  │
│                    │                              ▼                  │
│                    │                    ┌─────────────────────┐       │
│                    │                    │  Gemini LLM         │       │
│                    │                    │  (gemini-2.5-flash) │       │
│                    │                    └─────────────────────┘       │
│                    │                              │                  │
│                    │                              ▼                  │
│                    │                    ┌─────────────────────┐       │
│                    │                    │  SessionStateWriter │       │
│                    │                    │  (JSON persistence) │       │
│                    │                    └─────────────────────┘       │
│                    │                              │                  │
│                    │                              ▼                  │
│                    │                    ┌─────────────────────┐       │
│                    │                    │  Gradio UI (polls     │       │
│                    │                    │  every 2 seconds)     │       │
│                    │                    └─────────────────────┘       │
│                    │                              │                  │
│                    └──────────────────────────────┘                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.3 External API Dependencies

| Service | Purpose | API Key Env Var | Endpoint |
|---------|---------|-----------------|----------|
| **Google Gemini** | LLM for agent reasoning, intent parsing, fitness Q&A | `GEMINI_API_KEY` | `generativelanguage.googleapis.com` |
| **NewsData.io** | Top 3 health/fitness/sports headlines | `NEWSDATA_API_KEY` | `newsdata.io/api/1/latest` |
| **OpenWeatherMap** | Current weather by coordinates | (embedded in WeatherTool) | `api.openweathermap.org` |
| **IP-API** | User location detection | (no key needed) | `ip-api.com` |

---

## 4. PROJECT FOLDER STRUCTURE

```
jarvisfit/
│
├── .env                              # Environment variables (API keys, user config)
│   ├── GEMINI_API_KEY=...
│   ├── NEWSDATA_API_KEY=...
│   └── USER_NAME=Abhi
│
├── .venv/                            # Python virtual environment
│
├── src/
│   └── jarvisfit/
│       │
│       ├── __init__.py
│       │
│       ├── main.py                   # Entry point: initializes controller, launches UI
│       │   └── JarvisFitController().kickoff() → starts listener thread
│       │       └── launch_ui() → starts Gradio server
│       │
│       ├── crew.py                   # CORE: All CrewAI agents, tasks, crews, session logic
│       │   ├── LLM configuration (Gemini 2.5 Flash)
│       │   ├── Tool instances (shared across agents)
│       │   ├── State helpers (read_state, write_state, reset_session_state)
│       │   ├── Speaking helper (speak_with_state)
│       │   ├── Exercise helpers (load_todays_exercises, mark_exercise, etc.)
│       │   ├── WakeSequenceCrew (CrewBase class)
│       │   ├── run_recommendation()
│       │   ├── run_diet_advice()
│       │   ├── run_end_session()
│       │   ├── run_session_loop()    # MAIN SESSION LOOP
│       │   └── JarvisFitController   # MASTER CONTROLLER CLASS
│       │       ├── on_wake()         # Wake word handler
│       │       ├── _await_start_confirmation()
│       │       ├── _run_session_and_resume()
│       │       ├── _free_assist_loop()
│       │       ├── on_shutdown()
│       │       ├── start_listener()  # Background thread
│       │       └── kickoff()         # Returns listener thread
│       │
│       ├── gradio_app.py             # Gradio UI builder + CSS + HTML generators
│       │   ├── CSS string (Iron Man theme, animations, orb styles)
│       │   ├── build_orb_html()      # Orb state machine (sleep/awake/listening/speaking/active/paused)
│       │   ├── build_workout_html()  # Exercise list with status badges
│       │   ├── build_weather_html()  # Session info card
│       │   ├── build_log_html()      # Weekly completion grid
│       │   ├── build_summary_html()  # Post-workout stats
│       │   ├── build_news_html()     # News headline cards
│       │   ├── read_state()          # JSON state reader
│       │   ├── refresh()             # UI polling function (every 2s)
│       │   └── launch_ui()           # gr.Blocks() builder + timer
│       │
│       ├── state.py                  # Shared in-memory state (headlines, last_update)
│       │   └── app_state (singleton)
│       │
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py           # All constants, paths, API keys from env
│       │   │   ├── USER_NAME
│       │   │   ├── WAKE_PHRASES = ["hey jarvis", "hello jarvis", "jarvis"]
│       │   │   ├── SHUTDOWN_PHRASES = ["jarvis off", "goodbye", "sleep"]
│       │   │   ├── GEMINI_MODEL
│       │   │   ├── SESSION_PATH (JSON state file)
│       │   │   ├── NEWSDATA_API_KEY
│       │   │   └── NEWSDATA_URL
│       │   │
│       │   ├── agents.yaml           # Agent role definitions (greeter_agent)
│       │   └── wake_tasks.yaml       # Task definitions (greet_user_task)
│       │
│       ├── tools/                    # ALL CREWAI TOOLS
│       │   ├── __init__.py
│       │   ├── voice_listener_tool.py   # VoiceListenerTool wrapper
│       │   ├── weather_tool.py            # OpenWeatherMap API
│       │   ├── location_tool.py           # IP-based geolocation
│       │   ├── datetime_tool.py           # Current day/date/time/greeting
│       │   ├── workout_plan_loader_tool.py # JSON plan reader
│       │   ├── session_state_tool.py      # Read/Write JSON state
│       │   ├── intent_parser_tool.py      # Gemini-based intent classification
│       │   ├── diet_rules_tool.py         # Nutrition calculation engine
│       │   ├── speaker_tool.py            # pyttsx3 TTS engine
│       │   └── news_tool.py             # NewsData.io API + saves to app_state
│       │
│       ├── voice/
│       │   ├── __init__.py
│       │   └── listener.py           # VoiceListener class
│       │       ├── listen_for_wake_word()  # Background wake word detection
│       │       ├── listen_once()           # Single utterance capture
│       │       └── _transcribe()           # SpeechRecognition wrapper
│       │
│       └── data/
│           └── workout_plan.json     # Weekly exercise schedule
│
├── session_state.json                # Runtime state (read/written by SessionStateTool)
│
├── requirements.txt                  # Python dependencies
│   ├── gradio>=5.0.0
│   ├── crewai>=0.100.0
│   ├── pydantic>=2.0.0
│   ├── pyttsx3
│   ├── SpeechRecognition
│   ├── PyAudio
│   ├── requests
│   ├── python-dotenv
│   └── google-generativeai
│
└── pyproject.toml                    # Project metadata, entry points
```

---

## 5. END-TO-END WORKFLOW DIAGRAM

### 5.1 System Lifecycle (Wake → Sleep)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           JARVISFIT LIFECYCLE                               │
└─────────────────────────────────────────────────────────────────────────────┘

                                ┌─────────────┐
                                │   STARTUP   │
                                │  (main.py)  │
                                └──────┬──────┘
                                       │
                                       ▼
                    ┌────────────────────────────────────┐
                    │  JarvisFitController.kickoff()     │
                    │  → start_listener() on daemon      │
                    │    thread                          │
                    └────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              SLEEPING STATE                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  VoiceListener.listen_for_wake_word()                                 │  │
│  │  • Continuous microphone monitoring                                   │  │
│  │  • Energy threshold-based activation                                  │  │
│  │  • Listens for: "hey jarvis", "hello jarvis", "jarvis"                │  │
│  │  • Orb: dark blue, pulsing slowly, label "SLEEPING"                   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                       │                                     │
│                    "Hey Jarvis"       │                                     │
│                    detected           ▼                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               WAKE SEQUENCE                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  on_wake() — IMMEDIATE STATE UPDATE (Critical Fix)                      │  │
│  │  Step 1: write_state(jarvis_awake=True, listening_for_command=False,   │  │
│  │                    current_status="AWAKE")                            │  │
│  │  Step 2: speak_with_state("Jarvis online.") → green orb + text          │  │
│  │  Step 3: reset_session_state() + reset_week_if_needed()               │  │
│  │  Step 4: WakeSequenceCrew().crew().kickoff()                          │  │
│  │          → greeter_agent fetches: location, weather, datetime, news  │  │
│  │  Step 5: Build greeting string in Python (NOT via crew output)        │  │
│  │  Step 6: speak_with_state(greeting) → green orb during TTS            │  │
│  │  Step 7: After TTS → write_state(listening_for_command=True)         │  │
│  │          → orange orb, label "LISTENING"                              │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                       │                                     │
│                    If day already       │                                     │
│                    completed            ▼                                     │
│                              ┌─────────────────────┐                          │
│                              │  FREE ASSIST MODE   │                          │
│                              │  _free_assist_loop()│                          │
│                              │  • Open-ended Q&A   │                          │
│                              │  • Gemini answers   │                          │
│                              │  • Say "Jarvis off" │                          │
│                              │    to sleep         │                          │
│                              └─────────────────────┘                          │
│                                       │                                     │
│                    Normal flow        ▼                                     │
│                              ┌─────────────────────┐                          │
│                              │  _await_start_      │                          │
│                              │  confirmation()     │                          │
│                              │  • "I am ready..."  │                          │
│                              │  • Listens for      │                          │
│                              │    "let's start"    │                          │
│                              │  • Orange orb       │                          │
│                              └─────────────────────┘                          │
│                                       │                                     │
│                    "Let's start"      ▼                                     │
│                              ┌─────────────────────┐                          │
│                              │  SESSION ACTIVE     │                          │
│                              │  write_state(       │                          │
│                              │    active_session=  │                          │
│                              │    True)            │                          │
│                              └─────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ACTIVE SESSION LOOP                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  run_session_loop(stop_flag, listener)                                │  │
│  │                                                                       │  │
│  │  WHILE active_session:                                                │  │
│  │    1. listen_once(timeout=8, phrase_limit=12)                         │  │
│  │    2. Check shutdown phrases → run_end_session() + break            │  │
│  │    3. intent_parser_tool._run(utterance) → {intent, exercise}     │  │
│  │    4. Route to handler:                                               │  │
│  │                                                                       │  │
│  │    ┌─────────────────┬─────────────────────────────────────────────┐  │  │
│  │    │ INTENT          │ ACTION                                      │  │  │
│  │    ├─────────────────┼─────────────────────────────────────────────┤  │  │
│  │    │ start_workout   │ Announce first exercise(s)                  │  │  │
│  │    │ exercise_       │ Mark completed, announce next, or end if    │  │  │
│  │    │   completed     │ all done                                    │  │  │
│  │    │ exercise_       │ Mark skipped, announce next, or end       │  │  │
│  │    │   skipped       │                                             │  │  │
│  │    │ request_plan    │ List remaining exercises                    │  │  │
│  │    │ request_        │ "You are X% through, Y remaining"           │  │  │
│  │    │   progress      │                                             │  │  │
│  │    │ request_next    │ run_recommendation()                        │  │  │
│  │    │ fitness_        │ Gemini Q&A → speak answer                   │  │  │
│  │    │   question      │                                             │  │  │
│  │    │ pause_session   │ write_state(status="paused"), wait for      │  │  │
│  │    │                 │ "let's continue"                            │  │  │
│  │    │ unknown         │ "Sorry, I didn't catch that"                │  │  │
│  │    └─────────────────┴─────────────────────────────────────────────┘  │  │
│  │                                                                       │  │
│  │  Orb states during loop:                                              │  │
│  │  • Speaking: green orb + text display                                 │  │
│  │  • Listening: orange orb + voice wave animation                         │  │
│  │  • Active: cyan orb (during exercise)                                 │  │
│  │  • Paused: yellow orb                                                   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                       │                                     │
│                    All exercises      │                                     │
│                    completed          ▼                                     │
│                              ┌─────────────────────┐                          │
│                              │  END SESSION        │                          │
│                              │  run_end_session()  │                          │
│                              │  1. Save completion │                          │
│                              │  2. Update streak   │                          │
│                              │  3. run_diet_advice │                          │
│                              │  4. Speak goodbye   │                          │
│                              │  5. write_state(    │                          │
│                              │     jarvis_awake=   │                          │
│                              │     False)          │                          │
│                              └─────────────────────┘                          │
│                                       │                                     │
│                                       ▼                                     │
┌─────────────────────────────────────────────────────────────────────────────┐
│                              RETURN TO SLEEP                                  │
│  • Listener thread continues (daemon)                                         │
│  • Orb returns to dark blue "SLEEPING"                                        │
│  • Awaits next "Hey Jarvis"                                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Agent Orchestration Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CREWAI AGENT ORCHESTRATION                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         CREW 1: WAKE SEQUENCE CREW                          │
│  Class: WakeSequenceCrew (CrewBase)                                         │
│  Process: Sequential                                                          │
│  Trigger: on_wake() after wake word detected                                  │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │                         greeter_agent                               │
    │  Role: Fitness AI Assistant                                         │
    │  Goal: Greet user with personalized morning briefing                │
    │  Tools: [location_tool, weather_tool, datetime_tool, news_tool]   │
    │  LLM: gemini-2.5-flash-lite                                         │
    │  allow_delegation: False                                            │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │                         greet_user_task                             │
    │  Description: "Greet {user_name} warmly..."                           │
    │  Expected Output: Greeting string                                     │
    │  Agent: greeter_agent                                               │
    │  Context: Uses tools to fetch real-time data                        │
    └─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │  NOTE: The crew's actual output is NOT used for TTS.                │
    │  Instead, on_wake() manually builds the greeting string in Python   │
    │  by calling tools directly, then passes it to speak_with_state().   │
    │  This ensures:                                                      │
    │  1. Immediate state updates (AWAKE → SPEAKING → LISTENING)          │
    │  2. No delay between wake and orb glow                              │
    │  3. Precise control over greeting format                            │
    └─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                    OTHER AGENTS (Tool-based, not Crew-based)                │
│  These are CrewAI BaseTool instances, used directly by Python logic:        │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │  intent_parser_agent (via IntentParserTool)                         │
    │  • Not a formal CrewAI Agent                                        │
    │  • Uses Gemini directly to classify utterances                      │
    │  • Returns: {intent, exercise_name, question}                         │
    │  • Called every iteration of run_session_loop()                     │
    └─────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │  diet_advisor_agent (via DietRulesTool)                           │
    │  • Calculates nutrition based on completed exercises                │
    │  • Returns: calories, protein, water, zinc, meal suggestions      │
    │  • Called once at session end by run_diet_advice()                  │
    └─────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────┐
    │  workout_manager_agent (implied, via WorkoutPlanLoaderTool)       │
    │  • Loads daily exercise plan from JSON                              │
    │  • Formats exercises for tracking                                   │
    │  • Called during on_wake()                                          │
    └─────────────────────────────────────────────────────────────────────┘
```

---

## 6. UI STATE MACHINE (Orb Colors)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORB STATE MACHINE                                   │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │   STARTUP   │
                              └──────┬──────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STATE: SLEEPING                                                            │
│  Color: Dark blue (#1a3a4a → #0d2030)                                       │
│  Opacity: 0.35                                                                │
│  Animation: Slow pulse, particle orbit                                        │
│  Label: "SLEEPING"                                                          │
│  Voice Wave: Hidden                                                           │
│  Speech Text: Hidden                                                          │
│  Trigger: Wake word detected                                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
              "Hey Jarvis"           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STATE: AWAKE (brief)                                                       │
│  Color: Cyan (#7efff5 → #00bfff)                                            │
│  Opacity: 1.0                                                                 │
│  Animation: Core brightens, rings spin faster                               │
│  Label: "AWAKE"                                                               │
│  Duration: ~1-2 seconds (while crew initializes)                            │
│  Trigger: speak_with_state() called                                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STATE: SPEAKING                                                            │
│  Color: Green (#39ff14 → #2eb80f)                                           │
│  Opacity: 1.0                                                                 │
│  Animation: Core pulses, scanline on text                                   │
│  Label: "SPEAKING"                                                          │
│  Voice Wave: Hidden                                                           │
│  Speech Text: VISIBLE — shows text being spoken                             │
│  Trigger: TTS starts (speak_with_state)                                     │
│  Exit: TTS completes → transitions to LISTENING                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
              TTS done                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STATE: LISTENING                                                           │
│  Color: Orange (#ffbf48 → #be4a1d)                                          │
│  Opacity: 1.0                                                                 │
│  Animation: Voice wave bars animate                                         │
│  Label: "LISTENING"                                                         │
│  Voice Wave: ACTIVE — 10 bars bouncing                                      │
│  Speech Text: Hidden                                                          │
│  Trigger: TTS complete, awaiting user command                               │
│  Exit: User speaks → intent parsed → action → SPEAKING                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
              "Let's start"          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STATE: ACTIVE SESSION                                                      │
│  Color: Cyan (#00ffe7 → #00bfff)                                            │
│  Opacity: 1.0                                                                 │
│  Animation: Steady glow, rings active                                         │
│  Label: "ACTIVE SESSION"                                                    │
│  Voice Wave: Hidden (unless listening for next command)                      │
│  Speech Text: Hidden (unless speaking)                                        │
│  Trigger: User confirms start                                               │
│  Exit: All exercises done → END SESSION, or "Jarvis off"                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
              "Jarvis pause"         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STATE: PAUSED                                                              │
│  Color: Yellow (#f5a623 → #c47d0e)                                          │
│  Opacity: 1.0                                                                 │
│  Animation: Slow pulse                                                        │
│  Label: "PAUSED"                                                            │
│  Voice Wave: Hidden                                                           │
│  Speech Text: Hidden                                                          │
│  Trigger: User says "pause"                                                 │
│  Exit: "Let's continue" → returns to ACTIVE/LISTENING                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
              All done /               ┌─────────────────────┐
              "Jarvis off"             │   END SESSION       │
                                       │   → SLEEPING        │
                                       └─────────────────────┘
```

---

## 7. DO'S AND DON'TS

### 7.1 Do's

| # | Rule | Rationale |
|---|------|-----------|
| 1 | **Always call `speak_with_state()` instead of `speaker_tool._run()` directly** | Ensures orb shows green + text during speech, then returns to listening state |
| 2 | **Set state BEFORE doing any work in `on_wake()`** | UI must know we're awake immediately; crew execution takes seconds |
| 3 | **Use `_tts_lock` (threading.Lock) around pyttsx3** | Prevents overlapping speech if multiple agents trigger simultaneously |
| 4 | **Read state fresh in every loop iteration** | State changes asynchronously between threads |
| 5 | **Handle `None` from `listen_once()`** | Timeout means no speech detected; continue loop |
| 6 | **Use `daemon=True` for background threads** | Prevents zombie threads on main process exit |
| 7 | **Check shutdown phrases BEFORE intent parsing** | Faster exit path, avoids unnecessary LLM calls |
| 8 | **Keep `allow_delegation=False` on agents** | Prevents infinite agent loops, reduces token cost |
| 9 | **Use `thinking_budget=0` for Gemini** | Disables CoT for faster, cheaper responses |
| 10 | **Refresh UI every 2 seconds via `gr.Timer`** | Gradio components don't auto-update from file changes |

### 7.2 Don'ts

| # | Rule | Rationale |
|---|------|-----------|
| 1 | **Don't assign arbitrary attributes on CrewAI BaseTool subclasses** | Pydantic v2 raises `ValueError`; use `PrivateAttr` for runtime attributes |
| 2 | **Don't use `self.client = ...` in a BaseTool** | Use `self._client = PrivateAttr(default=None)` instead |
| 3 | **Don't call Gemini TTS models without checking pricing** | `gemini-3.1-flash-tts-preview` is expensive; pyttsx3 is free |
| 4 | **Don't block the main thread with `engine.runAndWait()`** | Use `_tts_lock` but keep it in a non-UI thread |
| 5 | **Don't assume `app_state` persists across Gradio reloads** | It's in-memory; re-fetch from JSON on startup |
| 6 | **Don't hardcode API keys** | Always use `os.getenv()` + `.env` file (gitignored) |
| 7 | **Don't create a new `VoiceListener` per wake word** | Reuse the same instance; creating multiple listeners causes audio conflicts |
| 8 | **Don't forget to `engine.stop()` after pyttsx3 speech** | Prevents audio device lock issues |
| 9 | **Don't use `time.sleep()` in Gradio event handlers** | Blocks the UI; use async or threading instead |
| 10 | **Don't commit `session_state.json` to git** | It's runtime state, will cause merge conflicts |

---

## 8. KEY DESIGN DECISIONS

### 8.1 Why CrewAI + Manual Python (Hybrid)

The system uses **CrewAI for structured agent tasks** (wake greeting data gathering) but **manual Python for the session loop** (real-time voice interaction). This hybrid approach was chosen because:

- CrewAI's sequential process is too slow for real-time voice loops (2–5s per agent)
- Voice sessions require millisecond-level responsiveness
- Direct tool calling in Python allows precise state control between TTS and listening
- CrewAI is used where it shines: multi-step data gathering with clear inputs/outputs

### 8.2 Why pyttsx3 over Cloud TTS

| Factor | pyttsx3 | Gemini TTS |
|--------|---------|------------|
| Cost | $0 | ~$0.001–0.01 per request |
| Latency | <100ms | 1–3s |
| Offline | ✅ Yes | ❌ No |
| Voice Quality | Robotic but functional | Natural, expressive |
| Dependency | Local OS voices | API key + network |

**Decision:** pyttsx3 for production reliability; Gemini TTS optional for demos.

### 8.3 Why JSON File for State (Not Database)

- Simple read/write pattern matches Gradio's polling model
- No database setup required
- Human-readable for debugging
- Single-writer (SessionStateWriterTool) prevents corruption
- Trade-off: Not scalable beyond single-user, but fits the personal assistant use case

### 8.4 Why Gradio over React/Vue

- Python-native: No separate frontend build step
- Hot-reload during development
- Built-in microphone component for web deployment
- Easy CSS injection for custom theming
- Single-file deployment to Hugging Face Spaces

---

## 9. GLOSSARY

| Term | Definition |
|------|------------|
| **CrewAI** | Multi-agent orchestration framework; agents with roles, tasks, and tools collaborate |
| **BaseTool** | CrewAI's Pydantic-based tool class; all custom tools inherit from this |
| **PrivateAttr** | Pydantic v2 mechanism for non-schema attributes on models |
| **Wake Word** | Trigger phrase ("Hey Jarvis") that transitions system from sleep to awake |
| **Session Loop** | Real-time voice interaction loop during active workout |
| **Intent Parser** | Gemini-powered classifier that maps natural speech to structured intents |
| **TTS** | Text-to-Speech; pyttsx3 engine |
| **STT** | Speech-to-Text; SpeechRecognition + Google Speech API (free tier) |
| **Orb** | Central UI element; color-coded circle representing system state |
| **State File** | `session_state.json`; single source of truth for runtime state |
| **Daemon Thread** | Background thread that exits when main process exits |

---

## 10. KNOWN ISSUES & FUTURE WORK

| Issue | Severity | Workaround | Future Fix |
|-------|----------|------------|------------|
| pyttsx3 voice quality | Low | Accept robotic voice | Integrate Coqui TTS (free, local) |
| HF Spaces sleep | Medium | Use CPU Basic tier or wake via button | Implement webhook wake |
| No exercise timer | Medium | User self-times | Add `gr.Timer` countdown per exercise |
| Single-user only | Low | N/A (personal assistant) | Add user auth + multi-profile |
| News headlines not clickable | Low | Display only | Add `gr.HTML` links |
| No workout history chart | Low | Weekly log only | Add `gr.Plotly` trend graphs |

---

*Generated: 2026-06-13*
*Project: JarvisFit — Voice-Activated Fitness Intelligence*
