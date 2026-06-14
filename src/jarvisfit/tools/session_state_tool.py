import json
import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Any

from src.jarvisfit.config.settings import SESSION_PATH



class SessionStateReaderInput(BaseModel):
    pass


class SessionStateReaderTool(BaseTool):
    name: str = "SessionStateReaderTool"
    description: str = (
        "Reads and returns the full current session state from session_state.json. "
        "Use this to check exercise completion status, session flags, agent state, "
        "and today's progress."
    )
    args_schema: type[BaseModel] = SessionStateReaderInput

    def _run(self) -> dict:
        try:
            with open(SESSION_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}


class SessionStateWriterInput(BaseModel):
    updates: dict = Field(..., description="Dictionary of key-value pairs to update in session state")


class SessionStateWriterTool(BaseTool):
    name: str = "SessionStateWriterTool"
    description: str = (
        "Writes updates to session_state.json. Accepts a dictionary of updates "
        "which are deep-merged into the existing session state. Use this after "
        "every state change such as exercise completion, session start, or session end."
    )
    args_schema: Type[BaseModel] = SessionStateWriterInput

    def _run(self, updates: dict) -> dict:
        try:
            with open(SESSION_PATH, "r") as f:
                state = json.load(f)

            state = self._deep_merge(state, updates)

            with open(SESSION_PATH, "w") as f:
                json.dump(state, f, indent=2)

            return {"status": "success", "updated_keys": list(updates.keys())}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _deep_merge(self, base: dict, updates: dict) -> dict:
        for key, value in updates.items():
            if (
                key in base
                and isinstance(base[key], dict)
                and isinstance(value, dict)
            ):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base