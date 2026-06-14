import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class WeatherToolInput(BaseModel):
    lat: float = Field(..., description="Latitude of the user location")
    lon: float = Field(..., description="Longitude of the user location")


class WeatherTool(BaseTool):
    name: str = "WeatherTool"
    description: str = (
        "Fetches current weather conditions for a given latitude and longitude "
        "using OpenWeatherMap API. Returns temperature, condition, humidity, and city name."
    )
    args_schema: Type[BaseModel] = WeatherToolInput

    def _run(self, lat: float, lon: float) -> dict:
        import os
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "city": data.get("name", "your city"),
                "temperature": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"].capitalize(),
                "wind_speed": data["wind"]["speed"],
            }
        except Exception as e:
            return {
                "city": "your city",
                "temperature": "N/A",
                "feels_like": "N/A",
                "humidity": "N/A",
                "condition": "unavailable",
                "wind_speed": "N/A",
                "error": str(e),
            }