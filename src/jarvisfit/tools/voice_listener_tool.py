from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from src.jarvisfit.voice.listener import VoiceListener


class VoiceListenerToolInput(BaseModel):
    timeout: int = Field(default=5, description="Seconds to wait for speech input")
    phrase_limit: int = Field(default=10, description="Max seconds for a single phrase")


class VoiceListenerTool(BaseTool):
    name: str = "VoiceListenerTool"
    description: str = (
        "Captures a single voice utterance from the microphone and returns it "
        "as text. Used during active session loops to capture user commands like "
        "exercise completions, questions, and control phrases."
    )
    args_schema: Type[BaseModel] = VoiceListenerToolInput

    def _run(self, timeout: int = 5, phrase_limit: int = 10) -> dict:
        listener = VoiceListener()
        utterance = listener.listen_once(timeout=timeout, phrase_limit=phrase_limit)
        if utterance:
            return {"status": "captured", "utterance": utterance}
        return {"status": "no_input", "utterance": None}