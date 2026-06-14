import requests
from crewai.tools import BaseTool
from pydantic import BaseModel


class LocationToolInput(BaseModel):
    pass


class LocationTool(BaseTool):
    name: str = "LocationTool"
    description: str = (
        "Detects the user's current city, country, latitude, and longitude "
        "automatically using their IP address via ipinfo.io. No input required."
    )
    args_schema: type[BaseModel] = LocationToolInput

    def _run(self) -> dict:
        try:
            response = requests.get("https://ipinfo.io/json", timeout=10)
            response.raise_for_status()
            data = response.json()
            loc = data.get("loc", "0,0").split(",")
            return {
                "city": data.get("city", "Unknown City"),
                "region": data.get("region", ""),
                "country": data.get("country", ""),
                "lat": float(loc[0]),
                "lon": float(loc[1]),
            }
        except Exception as e:
            return {
                "city": "Unknown City",
                "region": "",
                "country": "",
                "lat": 0.0,
                "lon": 0.0,
                "error": str(e),
            }