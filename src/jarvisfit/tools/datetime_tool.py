from crewai.tools import BaseTool
from pydantic import BaseModel
from datetime import datetime


class DateTimeToolInput(BaseModel):
    pass


class DateTimeTool(BaseTool):
    name: str = "DateTimeTool"
    description: str = (
        "Returns the current date, time, day name, and a formatted date string. "
        "Used to dynamically determine which day's workout plan to load and to "
        "construct the greeting message. No input required."
    )
    args_schema: type[BaseModel] = DateTimeToolInput

    def _run(self) -> dict:
        now = datetime.now()
        hour = now.hour
        if hour < 12:
            greeting_time = "morning"
        elif hour < 17:
            greeting_time = "afternoon"
        else:
            greeting_time = "evening"

        return {
            "day_name": now.strftime("%A"),
            "date_formatted": now.strftime("%B %d"),
            "time_formatted": now.strftime("%I:%M %p").lstrip("0"),
            "greeting_time": greeting_time,
            "timestamp": now.isoformat(),
            "is_monday": now.weekday() == 0,
        }