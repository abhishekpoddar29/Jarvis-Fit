import json
import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from src.jarvisfit.config.settings import WORKOUT_PLAN_PATH


class WorkoutPlanLoaderInput(BaseModel):
    day_name: str = Field(..., description="Day name eg. Monday, Tuesday to load from plan")


class WorkoutPlanLoaderTool(BaseTool):
    name: str = "WorkoutPlanLoaderTool"
    description: str = (
        "Loads the workout plan for a specific day from workout_plan.json. "
        "Returns gym exercises, yoga poses, and running sessions for that day "
        "along with the focus area."
    )
    args_schema: Type[BaseModel] = WorkoutPlanLoaderInput

    def _run(self, day_name: str) -> dict:
        try:
            with open(WORKOUT_PLAN_PATH, "r") as f:
                plan = json.load(f)

            for day in plan["days"]:
                if day["day"].lower() == day_name.lower():
                    return {
                        "day": day["day"],
                        "focus": day.get("focus", "General Fitness"),
                        "gym_workout": day.get("gym_workout", []),
                        "yoga_session": day.get("yoga_session", []),
                        "running_session": day.get("running_session", []),
                    }

            return {"error": f"Day {day_name} not found in workout plan"}

        except Exception as e:
            return {"error": str(e)}