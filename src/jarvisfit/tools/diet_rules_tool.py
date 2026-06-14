import json
import os
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from src.jarvisfit.config.settings import DIET_RULES_PATH



class DietRulesInput(BaseModel):
    completed_exercises: list = Field(
        ...,
        description="List of completed exercise dicts with name and category"
    )
    focus: str = Field(
        default="General Fitness",
        description="Today's workout focus eg. Chest and Triceps, Legs, Full Body Strength"
    )
    body_weight_kg: float = Field(
        default=57.0,
        description="User body weight in kg for protein calculation"
    )


class DietRulesTool(BaseTool):
    name: str = "DietRulesTool"
    description: str = (
        "Applies rule-based nutrition formulas to calculate post-workout protein "
        "intake, water intake, and meal recommendations based on completed exercises "
        "and today's workout focus. Uses diet_rules.json for formula definitions."
    )
    args_schema: Type[BaseModel] = DietRulesInput

    def _run(self, completed_exercises: list, focus: str = "General Fitness", body_weight_kg: float = 57.0,) -> dict:
        try:
            with open(DIET_RULES_PATH, "r") as f:
                rules = json.load(f)
        except Exception as e:
            return {"error": str(e)}

        default_weight = rules["meta"]["default_body_weight_kg"]
        weight         = body_weight_kg if body_weight_kg !=57.0 else default_weight
        multiplier     = rules["base_nutrition"]["protein_multiplier"]

        # Protein based on weight * 2
        protein_grams  = round(weight * multiplier)

        # Calories burned from completed exercises
        cal_table      = rules.get("exercise_calories", {})
        calories_burned = 0
        for ex in completed_exercises:
            name = ex.get("name", "")
            if name in cal_table:
                entry = cal_table[name]
                if "calories_per_set" in entry:
                    calories_burned += entry["calories_per_set"] * entry.get("sets", 3)
                elif "calories_per_minute" in entry:
                    # Use duration from exercise if available
                    duration = ex.get("duration_minutes", 10)
                    calories_burned += entry["calories_per_minute"] * duration

        # Get day plan from focus
        day_plan = None
        for day, plan in rules["daily_plans"].items():
            if plan["focus"].lower() == focus.lower():
                day_plan = plan
                break

        if not day_plan:
            day_plan = rules["daily_plans"]["Monday"]

        vitamins  = day_plan["vitamins"]
        meals     = day_plan["meal_suggestions"]
        water     = day_plan["water_liters"]

        return {
            "total_exercises_completed": len(completed_exercises),
            "calories_burned":           calories_burned,
            "protein_grams":             protein_grams,
            "protein_formula":           f"{weight}kg x 2 = {protein_grams}g",
            "water_liters":              water,
            "pre_workout_meal":          meals["pre_workout"],
            "post_workout_meal":         meals["post_workout"],
            "dinner":                    meals["dinner"],
            "snacks":                    meals["snacks"],
            "vitamins": {
                "vitamin_c":   f"{vitamins['vitamin_c_mg']}mg",
                "vitamin_d":   f"{vitamins['vitamin_d_iu']}IU",
                "vitamin_b12": f"{vitamins['vitamin_b12_mcg']}mcg",
                "magnesium":   f"{vitamins['magnesium_mg']}mg",
                "omega3":      f"{vitamins['omega3_grams']}g",
            },
            "zinc": {
                "amount_mg": vitamins["zinc_mg"],
                "timing":    vitamins["zinc_timing"],
            },
            "nutrition_note":  day_plan["nutrition_note"],
            "protein_note":    day_plan["protein_note"],
        }

    def _default_rules(self) -> dict:
        return {
            "base_protein_grams": 120,
            "protein_per_gym_exercise": 5,
            "protein_per_yoga_exercise": 2,
            "protein_per_running_exercise": 8,
            "base_water_liters": 2.5,
            "water_per_exercise_liters": 0.1,
        }