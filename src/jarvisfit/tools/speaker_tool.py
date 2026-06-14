import threading
from typing import Type

import pyttsx3
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

_tts_lock = threading.Lock()


class SpeakerToolInput(BaseModel):
    text: str = Field(..., description="Text to be spoken aloud by Jarvis")


class SpeakerTool(BaseTool):
    name: str = "SpeakerTool"
    description: str = (
        "Converts text to speech and plays it aloud using the system TTS engine. "
        "Use this whenever Jarvis needs to speak to the user."
    )
    args_schema: Type[BaseModel] = SpeakerToolInput

    def _run(self, text: str) -> dict:
        print(f"[Jarvis] {text}")
        try:
            with _tts_lock:
                engine = pyttsx3.init()
                voices = engine.getProperty("voices")

                # Try to pick a male voice for Jarvis feel
                for voice in voices:
                    vname = voice.name.lower()
                    if any(x in vname for x in ["male", "david", "mark", "james", "george"]):
                        engine.setProperty("voice", voice.id)
                        break

                engine.setProperty("rate", 175)
                engine.setProperty("volume", 1.0)
                engine.say(text)
                engine.runAndWait()
                engine.stop()

            return {"status": "spoken", "text": text, "engine": "pyttsx3"}

        except Exception as e:
            print(f"[SpeakerTool] Error: {e}")
            return {"status": "error", "error": str(e), "text": text}