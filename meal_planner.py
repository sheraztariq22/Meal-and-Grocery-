from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional
import json
import os

@dataclass
class Ingredient:
    name: str
    quantity: float = 1.0
    unit: Optional[str] = None

@dataclass
class Meal:
    name: str
    ingredients: List[Ingredient] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

class MealPlanner:
    def __init__(self, meals: List[Meal]):
        self.meals = meals

    @classmethod
    def load_from_json(cls, path: str) -> "MealPlanner":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        meals = []
        for m in data:
            ings = []
            for ing in m.get("ingredients", []):
                ings.append(Ingredient(name=ing.get("name"), quantity=ing.get("quantity", 1.0), unit=ing.get("unit")))
            meals.append(Meal(name=m.get("name"), ingredients=ings, tags=m.get("tags", [])))
        return cls(meals)

    def find_meals(self, tags: List[str]) -> List[Meal]:
        if not tags:
            return self.meals
        tags_set = set(t.lower() for t in tags)
        return [m for m in self.meals if tags_set.intersection(t.lower() for t in m.tags)]

    def simple_plan(self, days: int, preferences: Dict = None) -> List[Meal]:
        avail = self.find_meals(preferences.get("tags") if preferences else [])
        if not avail:
            avail = self.meals
        plan = []
        idx = 0
        for _ in range(days):
            plan.append(avail[idx % len(avail)])
            idx += 1
        return plan

    def shopping_list_from_plan(self, plan: List[Meal]) -> Dict[str, Dict[str, float]]:
        sl = {}
        for meal in plan:
            for ing in meal.ingredients:
                key = ing.name.lower()
                unit = ing.unit or ""
                if key not in sl:
                    sl[key] = {"quantity": 0.0, "unit": unit}
                try:
                    sl[key]["quantity"] += float(ing.quantity)
                except Exception:
                    sl[key]["quantity"] = sl[key].get("quantity", 0) + 1
        return sl


def call_model_stub(prompt: str) -> str:
    raise NotImplementedError("Implement call to Google Gemini / LangChain here. Provide a function that accepts a prompt and returns a string response.")


def generate_meal_plan(planner: MealPlanner, days: int = 7, preferences: Dict = None, model_call: Callable[[str], str] = None) -> Dict:
    if model_call is None:
        plan = planner.simple_plan(days, preferences or {})
        shopping = planner.shopping_list_from_plan(plan)
        return {"plan": [m.name for m in plan], "shopping_list": shopping}

    prompt = {
        "days": days,
        "preferences": preferences or {},
        "available_meals": [ {"name": m.name, "tags": m.tags, "ingredients": [{"name": i.name, "quantity": i.quantity, "unit": i.unit} for i in m.ingredients]} for m in planner.meals]
    }
    response = model_call(json.dumps(prompt))
    try:
        out = json.loads(response)
        return out
    except Exception:
        return {"raw_response": response}


if __name__ == "__main__":
    base = os.path.dirname(__file__)
    meals_path = os.path.join(base, "meals.json")
    planner = MealPlanner.load_from_json(meals_path) if os.path.exists(meals_path) else MealPlanner([])
    result = generate_meal_plan(planner, days=7)
    print(json.dumps(result, indent=2))
