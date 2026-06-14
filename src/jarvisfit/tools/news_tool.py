import requests
import os
from crewai.tools import BaseTool
from pydantic import BaseModel
from src.jarvisfit.config.settings import NEWSDATA_API_KEY, NEWSDATA_URL
from src.jarvisfit.state import app_state
import time


class NewsToolInput(BaseModel):
    pass


class NewsTool(BaseTool):
    name: str = "NewsTool"
    description: str = (
        "Fetches the top 3 latest breaking news headlines relevant to health, "
        "fitness, or general news from newsdata.io. Returns a short list of "
        "headlines to be included in the morning greeting. No input required."
    )
    args_schema: type[BaseModel] = NewsToolInput

    def _run(self) -> dict:
        try:
            params = {
                "apikey":   NEWSDATA_API_KEY,
                "language": "en",
                "category": "health,sports,top",
                "size":     3,
            }
            response = requests.get(NEWSDATA_URL, params=params, timeout=10)
            response.raise_for_status()
            data     = response.json()
            articles = data.get("results", [])

            headlines = []
            for article in articles[:3]:
                title = article.get("title", "").strip()
                if title:
                    headlines.append(title)
            app_state.headlines = headlines
            app_state.last_update = time.strftime("%H:%M")

            if not headlines:
                return {
                    "status":    "no_headlines",
                    "headlines": [],
                    "summary":   "No news headlines available right now.",
                }

            return {
                "status":    "success",
                "headlines": headlines,
                "summary":   " | ".join(headlines),
            }

        except Exception as e:
            return {
                "status":    "error",
                "headlines": [],
                "summary":   "Could not fetch news right now.",
                "error":     str(e),
            }