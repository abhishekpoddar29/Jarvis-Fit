import os
import json
import threading
from datetime import datetime

from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from dotenv import load_dotenv
import google.generativeai as genai

from src.jarvisfit.tools.voice_listener_tool import VoiceListenerTool
from src.jarvisfit.tools.weather_tool import WeatherTool
from src.jarvisfit.tools.location_tool import LocationTool
from src.jarvisfit.tools.datetime_tool import DateTimeTool
from src.jarvisfit.tools.workout_plan_loader_tool import WorkoutPlanLoaderTool
from src.jarvisfit.tools.session_state_tool import (
    SessionStateReaderTool,
    SessionStateWriterTool,
)
from src.jarvisfit.tools.intent_parser_tool import IntentParserTool
from src.jarvisfit.tools.diet_rules_tool import DietRulesTool
from src.jarvisfit.tools.speaker_tool import SpeakerTool
from src.jarvisfit.voice.listener import VoiceListener
from src.jarvisfit.config.settings import (
    USER_NAME,
    WAKE_PHRASES,
    SHUTDOWN_PHRASES,
    GEMINI_MODEL,
    SESSION_PATH
)
from src.jarvisfit.tools.news_tool import NewsTool

load_dotenv()


# ─────────────────────────────────────────────
# LLM
# ─────────────────────────────────────────────

llm = LLM(
    model="gemini/gemini-2.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    thinking={"thinking_budget": 0},
    temperature=0.4,

)


# ─────────────────────────────────────────────
# SHARED TOOL INSTANCES
# ─────────────────────────────────────────────

voice_listener_tool = VoiceListenerTool()
weather_tool        = WeatherTool()
location_tool       = LocationTool()
datetime_tool       = DateTimeTool()
workout_loader_tool = WorkoutPlanLoaderTool()
state_reader_tool   = SessionStateReaderTool()
state_writer_tool   = SessionStateWriterTool()
intent_parser_tool  = IntentParserTool()
diet_rules_tool     = DietRulesTool()
speaker_tool        = SpeakerTool()
news_tool           = NewsTool()


# ─────────────────────────────────────────────
# SESSION STATE HELPERS
# ─────────────────────────────────────────────

def read_state() -> dict:
    with open(SESSION_PATH, "r") as f:
        return json.load(f)


def write_state(updates: dict):
    state_writer_tool._run(updates=updates)


def reset_session_state():
    write_state({
        "session_status": "not_started",
        "session_start_time": None,
        "session_end_time": None,
        "diet_summary_given": False,
        "today_progress": {
            "gym_completed": False,
            "yoga_completed": False,
            "running_completed": False,
            "completion_percentage": 0,
            "exercises": {"gym": [], "yoga": [], "running": []},
        },
        "agent_state": {
            "jarvis_awake": False,
            "listening_for_command": False,
            "awaiting_user_confirmation": False,
            "next_action": "await_wake",
            "active_session": False,
            "speaking": False, 
        },
        "last_speech": "", 
        "last_updated": datetime.now().isoformat(),
    })

# ─────────────────────────────────────────────
# SPEAKING STATE HELPER
# ─────────────────────────────────────────────

def speak_with_state(text: str) -> str:
    """
    Speak text through TTS while updating the UI state.
    Orb glows green + shows text during speech,
    then returns to orange listening mode.
    """
    # Pre-speech: green orb, show text
    write_state({
        "agent_state": {
            "jarvis_awake": read_state()["agent_state"].get("jarvis_awake", True),
            "active_session": read_state()["agent_state"].get("active_session", False),
            "listening_for_command": False,
            "awaiting_user_confirmation": read_state()["agent_state"].get("awaiting_user_confirmation", False),
            "next_action": read_state()["agent_state"].get("next_action", "idle"),
            "speaking": True,
        },
        "last_speech": text,
        "last_updated": datetime.now().isoformat(),
    })
    
    # Execute TTS
    result = speaker_tool._run(text=text)
    
    # Post-speech: return to listening (orange orb)
    write_state({
        "agent_state": {
            "jarvis_awake": read_state()["agent_state"].get("jarvis_awake", True),
            "active_session": read_state()["agent_state"].get("active_session", False),
            "listening_for_command": True,
            "awaiting_user_confirmation": read_state()["agent_state"].get("awaiting_user_confirmation", False),
            "next_action": read_state()["agent_state"].get("next_action", "idle"),
            "speaking": False,
        },
        "last_speech": "",
        "last_updated": datetime.now().isoformat(),
    })
    
    return result


def reset_week_if_needed():
    state  = read_state()
    dt     = datetime_tool._run()
    if dt.get("is_monday") and len(state.get("completed_days", [])) > 0:
        write_state({
            "completed_days": [],
            "streak_days": 0,
            "week_progress_percentage": 0,
            "daily_logs": {
                day: {
                    "gym_completed": False,
                    "yoga_completed": False,
                    "running_completed": False,
                    "notes": "",
                }
                for day in [
                    "Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday",
                ]
            },
        })
        print("[jarvisfit] Monday detected. Weekly progress has been reset.")


def load_todays_exercises(day_name: str) -> dict:
    plan = workout_loader_tool._run(day_name=day_name)
    if "error" in plan:
        return {}

    def fmt_gym(e):
        return {
            "name": e["exercise"], "category": "gym", "status": "pending",
            "sets": e.get("sets"), "reps": e.get("reps"),
            "duration_seconds": e.get("duration_seconds"),
            "duration_minutes": e.get("duration_minutes"),
        }

    def fmt_yoga(e):
        return {
            "name": e["pose"], "category": "yoga", "status": "pending",
            "duration_minutes": e.get("duration_minutes"),
        }

    def fmt_run(e):
        return {
            "name": e.get("type", "Running"), "category": "running",
            "status": "pending", "duration_minutes": e.get("duration_minutes"),
        }

    gym_list     = [fmt_gym(e)  for e in plan.get("gym_workout", [])]
    yoga_list    = [fmt_yoga(e) for e in plan.get("yoga_session", [])]
    running_list = [fmt_run(e)  for e in plan.get("running_session", [])]

    write_state({
        "current_day": day_name,
        "today_progress": {
            "gym_completed": False,
            "yoga_completed": False,
            "running_completed": False,
            "completion_percentage": 0,
            "exercises": {
                "gym": gym_list,
                "yoga": yoga_list,
                "running": running_list,
            },
        },
    })
    return plan


def get_pending_exercises() -> list:
    state = read_state()
    CATEGORIES = ["gym", "yoga", "running"]
    return [
        ex
        for cat in CATEGORIES
        for ex in state["today_progress"]["exercises"].get(cat, [])
        if ex["status"] == "pending"
    ]



def get_all_exercise_names() -> list:
    state = read_state()
    CATEGORIES = ["gym", "yoga", "running"]
    return [
        ex["name"]
        for cat in CATEGORIES
        for ex in state["today_progress"]["exercises"].get(cat, [])
    ]


def get_completed_exercises() -> list:
    state = read_state()
    CATEGORIES = ["gym", "yoga", "running"]
    return [
        {"name": ex["name"], "category": cat}
        for cat in CATEGORIES
        for ex in state["today_progress"]["exercises"].get(cat, [])
        if ex["status"] == "completed"
    ]


def mark_exercise(exercise_name: str, status: str) -> tuple:
    state     = read_state()
    exercises = state["today_progress"]["exercises"]
    matched   = False

    CATEGORIES = ["gym", "yoga", "running"]    # explicit list, ignore booleans

    for cat in CATEGORIES:
        for ex in exercises.get(cat, []):
            if ex["name"].lower() == exercise_name.lower():
                ex["status"] = status
                matched = True
                break
        if matched:
            break

    total = sum(len(exercises.get(c, [])) for c in CATEGORIES)
    done  = sum(
        1 for c in CATEGORIES
        for e in exercises.get(c, [])
        if e["status"] in ["completed", "skipped"]
    )
    pct = round((done / total) * 100) if total > 0 else 0

    gym_done  = all(e["status"] != "pending" for e in exercises.get("gym",     [{"status": "completed"}]))
    yoga_done = all(e["status"] != "pending" for e in exercises.get("yoga",    [{"status": "completed"}]))
    run_done  = all(e["status"] != "pending" for e in exercises.get("running", [{"status": "completed"}]))

    write_state({
        "today_progress": {
            "gym_completed":     gym_done,
            "yoga_completed":    yoga_done,
            "running_completed": run_done,
            "completion_percentage": pct,
            "exercises": exercises,
        },
        "last_updated": datetime.now().isoformat(),
    })
    return matched, pct


# ─────────────────────────────────────────────
# CREW 1 — WAKE SEQUENCE CREW
# Agents: greeter_agent, workout_manager_agent
# Tasks : greet_user_task, load_and_present_workout_task
# Process: Sequential
# Triggered by: on_wake() after wake word detected
# ─────────────────────────────────────────────

@CrewBase
class WakeSequenceCrew:
    agents_config = "config/agents.yaml"
    tasks_config  = "config/wake_tasks.yaml"

    # ── agents ──────────────────────────────

    @agent
    def greeter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["greeter_agent"],
            tools=[location_tool, weather_tool, datetime_tool,news_tool],
            llm=llm,
            verbose=True,
            allow_delegation=False,
        )


    # ── tasks ───────────────────────────────

    @task
    def greet_user_task(self) -> Task:
        return Task(
            config=self.tasks_config["greet_user_task"],
            agent=self.greeter_agent(),
        )


    # ── crew ────────────────────────────────

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )




# ─────────────────────────────────────────────
# PYTHON SESSION LOOP
# Handles all real time voice intents during
# an active workout session. Runs in a daemon
# thread. Calls EndSessionCrew when session ends.
# ─────────────────────────────────────────────

def run_recommendation(completed_name: str = None) -> bool:
    pending = get_pending_exercises()
    if not pending:
        speak_with_state(
            text=(
                f"Amazing work {USER_NAME}! You have completed all exercises for today. "
                "Let me put together your nutrition summary."
            )
        )
        return True

    next_one = pending[0]["name"]
    next_two = pending[1]["name"] if len(pending) > 1 else None

    if completed_name:
        msg = f"Great work on {completed_name}! Next up is {next_one}."
    else:
        msg = f"Next up is {next_one}."

    if next_two:
        msg += f" After that move on to {next_two}."

    speak_with_state(text=msg)
    return False  # session continues


def run_diet_advice():
    state     = read_state()
    if state.get("diet_summary_given"):
        return

    completed = get_completed_exercises()
    focus     = state.get("today_progress", {}).get("focus", "General Fitness")
    nutrition = diet_rules_tool._run(
        completed_exercises=completed,
        focus=focus,
        body_weight_kg=57.0,
    )

    summary = (
        f"Great work today {USER_NAME}. Here is your nutrition summary. "
        f"You completed {nutrition['total_exercises_completed']} exercises "
        f"and burned approximately {nutrition['calories_burned']} calories. "
        f"Your protein target today is {nutrition['protein_grams']} grams "
        f"based on your body weight. "
        f"Drink {nutrition['water_liters']} litres of water through the day. "
        f"For your post workout meal, {nutrition['post_workout_meal']}. "
        f"For dinner, {nutrition['dinner']}. "
        f"Take {nutrition['zinc']['amount_mg']} milligrams of zinc tonight. "
        f"{nutrition['zinc']['timing']}. "
        f"{nutrition['nutrition_note']}"
    )
    print(f"[Diet] {summary}")
    speak_with_state(text=summary)
    write_state({"diet_summary_given": True})


def run_end_session():
    state          = read_state()
    day            = state.get("current_day", "today")
    completed_days = state.get("completed_days", [])

    if day not in completed_days:
        completed_days.append(day)

    write_state({
        "session_status":    "completed",
        "session_end_time":  datetime.now().isoformat(),
        "completed_days":    completed_days,
        "streak_days":       state.get("streak_days", 0) + 1,
        "daily_logs": {
            day: {
                "gym_completed":     state["today_progress"]["gym_completed"],
                "yoga_completed":    state["today_progress"]["yoga_completed"],
                "running_completed": state["today_progress"]["running_completed"],
                "notes": "Session completed via jarvisfit",
            }
        },
        "agent_state": {
            "jarvis_awake":               False,
            "listening_for_command":      False,
            "awaiting_user_confirmation": False,
            "next_action":                "idle",
            "active_session":             False,
        },
    })

    run_diet_advice()

    speak_with_state(
        text=f"Jarvis going to sleep. Have a great day {USER_NAME}.  Goodbye."
    )
    print("[jarvisfit] Session ended. Returning to idle.")

def run_session_loop(stop_flag: threading.Event,listener: VoiceListener):

    print("[jarvisfit] Session loop started. Listening for commands...")

    while not stop_flag.is_set():
        state = read_state()
        if not state["agent_state"].get("active_session"):
            break

        utterance = listener.listen_once(timeout=8, phrase_limit=12)

        if utterance is None:
            continue


        print(f"[SessionLoop] Heard: {utterance}")

        # Shutdown check before intent parsing
        if any(phrase in utterance for phrase in SHUTDOWN_PHRASES):
            speak_with_state(
                text=f"Understood {USER_NAME}. Ending your session now."
            )
            run_end_session()
            stop_flag.set()
            break

        # Intent classification via Gemini
        intent_result  = intent_parser_tool._run(
            utterance=utterance,
            available_exercises=get_all_exercise_names(),
        )
        print(f"[SessionLoop] Intent results: {intent_result}")

        intent        = intent_result.get("intent", "unknown")
        exercise_name = intent_result.get("exercise_name", "")
        print(f"[SessionLoop] Routing to intent: {intent}")
        # ── Intent routing ───────────────────
        if intent == "start_workout":
            pending = get_pending_exercises()
            if pending:
                first = pending[0]["name"]
                second = pending[1]["name"] if len(pending) > 1 else None
                msg = f"Let us get started. Your first exercise is {first}."
                if second:
                    msg += f" After that move on to {second}."
                speak_with_state(text=msg)
            else:
                speak_with_state(text="All exercises are already completed for today.")


        elif intent == "exercise_completed":
            if not exercise_name:
                speak_with_state(
                    text="Which exercise did you complete? Please say the exercise name."
                )
                continue
            matched, pct = mark_exercise(exercise_name, "completed")

            if matched:
                if run_recommendation(completed_name=exercise_name):
                    run_end_session()
                    stop_flag.set()
                    break
            else:
                speak_with_state(
                    text=f"I could not find {exercise_name} in today's plan. Please try again."
                )

        elif intent == "exercise_skipped":
            matched, pct = mark_exercise(exercise_name, "skipped")
            if matched:
                speak_with_state(text=f"Okay, skipping {exercise_name}.")
                if run_recommendation():
                    run_end_session()
                    stop_flag.set()
                    break
            else:
                speak_with_state(
                    text=f"I could not find {exercise_name} in today's plan."
                )

        elif intent == "request_plan":
            pending = get_pending_exercises()
            names   = ", ".join(e["name"] for e in pending) if pending else "none"
            speak_with_state(
                text=f"Your remaining exercises for today are: {names}." if pending
                else "You have completed all exercises for today."
            )

        elif intent == "request_progress":
            state = read_state()
            pct   = state["today_progress"]["completion_percentage"]
            left  = len(get_pending_exercises())
            speak_with_state(
                text=(
                    f"You are {pct} percent through today's workout. "
                    f"You have {left} exercises remaining."
                )
            )

        elif intent == "request_next":
            run_recommendation()

        elif intent == "fitness_question":
            question = intent_result.get("question", utterance)
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model    = genai.GenerativeModel("gemini-2.5-flash-lite")
            response = model.generate_content(
                f"Answer this fitness question briefly in 2 to 3 sentences: {question}"
            )
            speak_with_state(text=response.text.strip())

        elif intent == "pause_session":
            write_state({"session_status": "paused"})
            speak_with_state(
                text=f"Sure {USER_NAME}, taking a break. Say let us continue when you are ready."
            )
            # Nested resume loop
            while not stop_flag.is_set():
                resume_utt = listener.listen_once(timeout=10, phrase_limit=8)
                if not resume_utt:
                    continue
                if any(phrase in resume_utt for phrase in SHUTDOWN_PHRASES):
                    run_end_session()
                    stop_flag.set()
                    break
                resume_intent = intent_parser_tool._run(
                    utterance=resume_utt,
                    available_exercises=[],
                )
                if resume_intent.get("intent") == "resume_session":
                    write_state({"session_status": "active"})
                    pending = get_pending_exercises()
                    names   = ", ".join(e["name"] for e in pending) if pending else "nothing"
                    speak_with_state(
                        text=f"Welcome back {USER_NAME}. Remaining exercises: {names}."
                    )
                    break

        elif intent == "unknown":
            speak_with_state(
                text="Sorry, I did not catch that. Could you please repeat?"
            )


# ─────────────────────────────────────────────
# jarvisfit MASTER CONTROLLER
# Owns the wake word listener thread.
# Calls WakeSequenceCrew on wake.
# Starts session loop thread after confirmation.
# Calls EndSessionCrew via run_end_session.
# ─────────────────────────────────────────────
def speak_todays_plan(day_name: str, plan: dict):
        if not plan:
            speak_with_state(text="Sorry, I could not load today's plan.")
            return

        gym_count     = len(plan.get("gym_workout", []))
        yoga_count    = len(plan.get("yoga_session", []))
        running_count = len(plan.get("running_session", []))
        focus         = plan.get("focus", "General Fitness")
        pending       = get_pending_exercises()
        first         = pending[0]["name"] if pending else "your first exercise"

        text = (
            f"Here is your plan for today, {day_name}. "
            f"Your focus is {focus}. "
            f"You have {gym_count} gym exercises, {yoga_count} yoga poses, "
            f"and {running_count} running activities. "
            f"Let us get started. Your first exercise is {first}."
        )

        print(f"[Plan] {text}")               # ADD THIS
        result = speak_with_state(text=text)


        
class JarvisFitController:

    def __init__(self):
        self.stop_flag      = threading.Event()
        self.session_active_flag=threading.Event()
        self.session_thread = None
        self._day_name      = None
        self._listener      = None

    

    # ── Wake handler ────────────────────────

    def on_wake(self):
        result = speak_with_state(text="Jarvis online.")
        print(f"[TTS] {result}")

        reset_session_state()
        reset_week_if_needed()

        dt             = datetime_tool._run()
        self._day_name = dt["day_name"]

        # ── Check if today already completed ────
        state         = read_state()
        today_log     = state.get("daily_logs", {}).get(self._day_name, {})
        day_completed = (
            today_log.get("gym_completed", False) or
            today_log.get("yoga_completed", False)
        )

        # ── CREW 1 — data fetch only, no SpeakerTool ────
        WakeSequenceCrew().crew().kickoff(inputs={
            "user_name": USER_NAME,
            "day_name":  self._day_name,
        })

        # ── Build and speak greeting in Python ──────────
        location  = location_tool._run()
        weather   = weather_tool._run(lat=location["lat"], lon=location["lon"])
        dt_data   = datetime_tool._run()
        news      = news_tool._run()

        headlines = news.get("headlines", [])
        news_text = ""
        if headlines:
            labels     = ["First", "Second", "Third"]
            news_lines = [
                f"{labels[i]}: {h}."
                for i, h in enumerate(headlines[:3])
            ]
            news_text = "Here are your top headlines for today. " + " ".join(news_lines)

        greeting = (
            f"Good {dt_data['greeting_time']} {USER_NAME}, good to see you. "
            f"Today is {dt_data['day_name']}, {dt_data['date_formatted']}. "
            f"It is currently {dt_data['time_formatted']}. "
            f"In {weather['city']}, the temperature is {weather['temperature']} degrees "
            f"with {weather['condition']}. "
            f"{news_text} "
            f"How would you like to start your day?"
        )
        print(f"[Jarvis] {greeting}")
        speak_with_state(text=greeting)

        # ── Day already completed branch ────────────────
        if day_completed:
            speak_with_state(
                text=(
                    f"By the way, you have already completed your "
                    f"{self._day_name} workout. Great discipline! "
                    f"How can I help you today?"
                )
            )
            write_state({
                "agent_state": {
                    "jarvis_awake":               True,
                    "listening_for_command":      True,
                    "awaiting_user_confirmation": False,
                    "next_action":                "free_assist",
                    "active_session":             False,
                    "speaking":                   False,
                }
            })
            if self._listener is None:
                self._listener = VoiceListener()
            self._free_assist_loop(self._listener)
            return

        # ── Normal workout flow ──────────────────────────
        plan = load_todays_exercises(self._day_name)
        speak_todays_plan(self._day_name, plan)

        write_state({
            "agent_state": {
                "jarvis_awake":               True,
                "listening_for_command":      True,
                "awaiting_user_confirmation": True,
                "next_action":                "await_start_confirmation",
                "active_session":             False,
                "speaking":                   False,
            }
        })

        if self._listener is None:
            self._listener = VoiceListener()

        self._await_start_confirmation(self._listener)

    # ── Await start confirmation ─────────────

    def _await_start_confirmation(self,listener:VoiceListener):
        speak_with_state(text="I am ready whenever you are.")

        while True:
            utterance = listener.listen_once(timeout=10, phrase_limit=8)
            if utterance is None:
                continue

            if any(phrase in utterance for phrase in SHUTDOWN_PHRASES):
                speak_with_state(
                    text=f"Okay {USER_NAME}, going back to sleep."
                )
                write_state({
                    "agent_state": {"jarvis_awake": False}
                })
                return

            intent_result = intent_parser_tool._run(
                utterance=utterance,
                available_exercises=[],
            )

            if intent_result.get("intent") == "start_workout":
                # Mark session active
                write_state({
                    "session_status": "active",
                    "session_start_time": datetime.now().isoformat(),
                    "agent_state": {
                        "jarvis_awake": True,
                        "listening_for_command": True,
                        "awaiting_user_confirmation": False,
                        "next_action": "track_exercises",
                        "active_session": True,
                    },
                })
                # Start session loop on daemon thread
                self.stop_flag.clear()
                self.session_active_flag.set()

                self.session_thread = threading.Thread(
                    target=self._run_session_and_resume,
                    args=(listener,),
                    daemon=True,
                )
                self.session_thread.start()
                return
            else:
                speak_with_state(
                    text="Say let us start the workout whenever you are ready."
                )
    def _run_session_and_resume(self, listener: VoiceListener):
        run_session_loop(self.stop_flag, listener)
        self.session_active_flag.clear()

    def _free_assist_loop(self, listener: VoiceListener):
    
        speak_with_state(text="I am listening. Ask me anything or say Jarvis turn off.")

        while True:
            utterance = listener.listen_once(timeout=10, phrase_limit=12)
            if utterance is None:
                continue

            if any(phrase in utterance for phrase in SHUTDOWN_PHRASES):
                speak_with_state(
                    text=f"Goodbye {USER_NAME}. Jarvis going to sleep."
                )
                write_state({
                    "agent_state": {
                        "jarvis_awake":  False,
                        "active_session": False,
                    }
                })
                return

            # Answer anything as a fitness question
            try:
                genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                model    = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(
                    f"You are a fitness assistant. Answer briefly in 2-3 sentences: {utterance}"
                )
                speak_with_state(text=response.text.strip())
            except Exception as e:
                speak_with_state(
                    text="Sorry, I could not process that right now."
                )
    # ── Shutdown handler ─────────────────────

    def on_shutdown(self):
        if not self.stop_flag.is_set():
            self.stop_flag.set()
        self.session_active_flag.clear()
        state = read_state()
        if state["agent_state"].get("active_session"):
            speak_with_state(
                text=f"Understood {USER_NAME}. Ending your session now."
            )
            run_end_session()
        else:
            speak_with_state(
                text=f"Goodbye {USER_NAME}. Jarvis going to sleep."
            )
            write_state({
                "agent_state": {
                    "jarvis_awake": False,
                    "active_session": False,
                }
            })

    # ── Wake word listener thread ────────────

    def start_listener(self):
    # CHANGE — create ONE listener here and store it on self
        self._listener = VoiceListener()
        stop_main      = threading.Event()
        self._listener.listen_for_wake_word(
            wake_phrases=WAKE_PHRASES,
            shutdown_phrases=SHUTDOWN_PHRASES,
            on_wake=self.on_wake,
            on_shutdown=self.on_shutdown,
            stop_flag=stop_main,
            session_active_flag=self.session_active_flag,
        )

    def kickoff(self) -> threading.Thread:
        print("[jarvisfit] System online. Waiting for wake word...")
        listener_thread = threading.Thread(
            target=self.start_listener,
            daemon=True,
        )
        listener_thread.start()
        return listener_thread