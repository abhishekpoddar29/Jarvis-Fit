from typing import List

class AppState:
    headlines: List[str] = []
    last_update: str = ""

app_state = AppState()