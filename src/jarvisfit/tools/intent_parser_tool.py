import json
import os
import google.generativeai as genai
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class IntentParserInput(BaseModel):
    utterance: str = Field(..., description="Raw voice utterance text from the user to classify")
    available_exercises: list = Field(
        default=[],
        description="List of exercise names available today for fuzzy matching"
    )


class IntentParserTool(BaseTool):
    name: str = "IntentParserTool"
    description: str = (
        "Uses Gemini to classify a user voice utterance into one of the defined "
        "intents: exercise_completed, exercise_skipped, request_plan, "
        "request_progress, request_next, fitness_question, start_workout, "
        "pause_session, resume_session, or unknown. Returns a JSON object with "
        "intent and optionally exercise_name or question fields."
    )
    args_schema: Type[BaseModel] = IntentParserInput

    def _run(self, utterance: str, available_exercises: list = []) -> dict:
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-2.5-flash")

            exercise_list = ", ".join(available_exercises) if available_exercises else "not provided"

            prompt = f"""
                You are an intent parser for a voice-activated fitness assistant called JarvisFit.

                Classify the user utterance into exactly one of these intents:
                - exercise_completed
                - exercise_skipped
                - request_plan
                - request_progress
                - request_next
                - fitness_question
                - start_workout
                - pause_session
                - resume_session
                - unknown

                Today's available exercises for fuzzy matching: {exercise_list}

                Rules:
                1. If intent is exercise_completed or exercise_skipped, extract the exercise name
                and match it as closely as possible to the available exercises list.
                2. If intent is fitness_question, return the question field with the raw utterance.
                3. Respond ONLY with a valid JSON object. No explanation, no markdown, no extra text.

                Examples:
                Input: "push ups done"
                Output: {{"intent": "exercise_completed", "exercise_name": "Push Ups"}}

                Input: "what should I do next"
                Output: {{"intent": "request_next"}}

                Input: "skip the plank today"
                Output: {{"intent": "exercise_skipped", "exercise_name": "Plank"}}

                Input: "how many calories does a squat burn"
                Output: {{"intent": "fitness_question", "question": "how many calories does a squat burn"}}

                User utterance: "{utterance}"
                Output:
                """
            response = model.generate_content(prompt)
            raw = response.text.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()
            return json.loads(raw)

        except json.JSONDecodeError:
            return {"intent": "unknown", "error": "Failed to parse Gemini response as JSON"}
        except Exception as e:
            return {"intent": "unknown", "error": str(e)}