"""CrewAI + LangChain multi-agent coordinator with Google Gemini wrapper.

This module provides:
- Pydantic models for structured meal/shopping data (copied/adapted from the notebook)
- A small wrapper for Google Gemini (via `google-generativeai`) with a fallback stub
- Helpers to build CrewAI agents/tasks when `crewai` is installed, otherwise local stubs
- A Coordinator class to run a sequential multi-agent workflow (local fallback if dependencies missing)

Usage:
- Set `GEMINI_API_KEY` in your environment for real LLM calls.
- Install optional dependencies: `pip install crewai langchain google-generativeai pydantic ruamel.yaml`

This file is intentionally defensive: it will run without optional deps so you can prototype locally.
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any, Callable
import os
import json
from pydantic import BaseModel, Field

# Optional imports (soft)
try:
    import google.generativeai as genai
    HAS_GENAI = True
except Exception:
    genai = None
    HAS_GENAI = False

try:
    import crewai
    from crewai import Agent, Task, Crew, Process, LLM
    HAS_CREWAI = True
except Exception:
    Agent = None
    Task = None
    Crew = None
    Process = None
    LLM = None
    HAS_CREWAI = False

try:
    import yaml
    HAS_YAML = True
except Exception:
    yaml = None
    HAS_YAML = False


# -------------------- Pydantic models --------------------
class GroceryItem(BaseModel):
    name: str = Field(..., description="Name of the grocery item")
    quantity: str = Field(..., description="Quantity needed (e.g. '2 lbs')")
    estimated_price: Optional[str] = Field(None, description="Estimated price")
    category: Optional[str] = Field(None, description="Store section")

class MealPlan(BaseModel):
    meal_name: str
    difficulty_level: str
    servings: int
    researched_ingredients: List[str]

class ShoppingCategory(BaseModel):
    section_name: str
    items: List[GroceryItem]
    estimated_total: Optional[str]

class GroceryShoppingPlan(BaseModel):
    total_budget: Optional[str]
    meal_plans: List[MealPlan]
    shopping_sections: List[ShoppingCategory]
    shopping_tips: List[str] = []


# -------------------- Gemini (Google) wrapper --------------------
class GeminiWrapper:
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-tiny"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in environment and not provided")
        if not HAS_GENAI:
            raise RuntimeError("google-generativeai library is not installed. Install with 'pip install google-generativeai'")
        genai.configure(api_key=self.api_key)

    def call(self, prompt: str, **kwargs) -> str:
        """Call the Gemini model and return text response.

        This is a minimal wrapper. For advanced usage (structured output, multimodal), adapt accordingly.
        """
        if not HAS_GENAI:
            raise RuntimeError("google-generativeai not available")
        resp = genai.generate(model=self.model, prompt=prompt, **kwargs)
        # The response object shape may vary; defensively extract text
        if hasattr(resp, "text"):
            return resp.text
        try:
            return str(resp)
        except Exception:
            return json.dumps(resp, default=str)


# -------------------- CrewAI helpers / local fallbacks --------------------
class LocalAgent:
    """Simple local agent fallback that uses a callable LLM and synchronous logic."""
    def __init__(self, name: str, llm_call: Callable[[str], str], role: str = "agent"):
        self.name = name
        self.llm_call = llm_call
        self.role = role

    def run(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Any:
        enriched = f"Agent: {self.name}\nRole: {self.role}\nContext:{json.dumps(context or {})}\nPrompt:\n{prompt}"
        return self.llm_call(enriched)


def build_llm_callable_from_gemini(api_key: Optional[str] = None, model: str = "gemini-tiny") -> Callable[[str], str]:
    """Return a simple callable that sends text prompts to Gemini and returns text.

    Raises helpful errors if dependencies are missing.
    """
    if not (api_key or os.environ.get("GEMINI_API_KEY")):
        # fallback: echo stub
        def stub(prompt: str) -> str:
            return json.dumps({"stub": True, "prompt": prompt[:500]})
        return stub

    if not HAS_GENAI:
        raise RuntimeError("google-generativeai not installed; run: pip install google-generativeai")

    gw = GeminiWrapper(api_key=api_key, model=model)

    def call(prompt: str) -> str:
        return gw.call(prompt)

    return call


def build_agent_stubs(llm_call: Callable[[str], str]) -> Dict[str, LocalAgent]:
    """Create a small set of local agent stubs used if CrewAI not installed."""
    agents = {
        "meal_planner": LocalAgent("Meal Planner", llm_call, role="Recipe researcher and meal planner"),
        "shopping_organizer": LocalAgent("Shopping Organizer", llm_call, role="Organize shopping lists by store section"),
        "budget_advisor": LocalAgent("Budget Advisor", llm_call, role="Analyze budgets and suggest savings"),
        "summary_agent": LocalAgent("Report Compiler", llm_call, role="Compile final shopping guide")
    }
    return agents


# -------------------- Coordinator --------------------
class Coordinator:
    """Coordinate agents and tasks using CrewAI if available, otherwise local sequential execution."""
    def __init__(self, llm_call: Callable[[str], str], config_path: Optional[str] = None):
        self.llm_call = llm_call
        self.config_path = config_path
        self.agents = {}
        if HAS_CREWAI:
            # If crewai is installed, prefer using its Agent/Task abstractions
            self._build_crewai_agents()
        else:
            self.agents = build_agent_stubs(llm_call)

    def _build_crewai_agents(self):
        # basic example using CrewAI; users can extend with YAML configs
        try:
            # create an LLM wrapper for CrewAI if supported
            crew_llm = LLM(model="gemini-tiny") if LLM is not None else None
            self.agents = {
                "meal_planner": Agent(role="Meal Planner & Recipe Researcher", goal="Search recipes and create meal plans", tools=[], llm=crew_llm, verbose=False),
                "shopping_organizer": Agent(role="Shopping Organizer", goal="Organize shopping lists by store sections", tools=[], llm=crew_llm, verbose=False),
                "budget_advisor": Agent(role="Budget Advisor", goal="Provide cost estimates and money-saving tips", tools=[], llm=crew_llm, verbose=False),
                "summary_agent": Agent(role="Report Compiler", goal="Compile report", tools=[], llm=crew_llm, verbose=False),
            }
        except Exception as e:
            # Graceful fallback
            self.agents = build_agent_stubs(self.llm_call)

    def run_sequential(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run a simple sequential pipeline using either CrewAI or local agent stubs.

        Returns a dict with agent outputs.
        """
        results = {}
        # Stage 1: Meal planner
        meal_prompt = (
            f"Create a meal plan for {inputs.get('meal_name')} for {inputs.get('servings')} servings. "
            f"Budget: {inputs.get('budget')}. Dietary restrictions: {inputs.get('dietary_restrictions')}. Skill: {inputs.get('cooking_skill')}"
        )
        if HAS_CREWAI and isinstance(self.agents.get("meal_planner"), Agent):
            # best-effort using CrewAI kickoff style if available
            try:
                crew = Crew(agents=[self.agents['meal_planner']], tasks=[], process=Process.sequential)
                mp_out = crew.kickoff(inputs={
                    "meal_name": inputs.get('meal_name'),
                    "servings": inputs.get('servings'),
                    "budget": inputs.get('budget'),
                    "dietary_restrictions": inputs.get('dietary_restrictions'),
                    "cooking_skill": inputs.get('cooking_skill')
                })
                results['meal_planner'] = mp_out
            except Exception:
                results['meal_planner'] = self.agents['meal_planner'].run(meal_prompt)
        else:
            results['meal_planner'] = self.agents['meal_planner'].run(meal_prompt)

        # Stage 2: Shopping organizer
        shopping_prompt = f"Given the meal output: {truncate_for_prompt(results['meal_planner'])}\nProduce an organized shopping list grouped by store sections and quantities."
        results['shopping_organizer'] = (self._crew_task_fallback('shopping_organizer', shopping_prompt, context=results))

        # Stage 3: Budget advisor
        budget_prompt = f"Given shopping list: {truncate_for_prompt(results['shopping_organizer'])}\nEnsure total cost fits {inputs.get('budget')} and suggest savings."
        results['budget_advisor'] = (self._crew_task_fallback('budget_advisor', budget_prompt, context=results))

        # Stage 4: Summary
        summary_prompt = f"Compile a user-friendly guide containing meal plan, shopping list, budget tips, and leftovers suggestions. Context: {truncate_for_prompt(results)}"
        results['summary'] = (self._crew_task_fallback('summary_agent', summary_prompt, context=results))

        return results

    def _crew_task_fallback(self, agent_key: str, prompt: str, context: Optional[Dict[str, Any]] = None) -> Any:
        agent = self.agents.get(agent_key)
        if HAS_CREWAI and isinstance(agent, Agent):
            try:
                crew = Crew(agents=[agent], tasks=[], process=Process.sequential)
                return crew.kickoff(inputs={'prompt': prompt, 'context': context})
            except Exception:
                return agent.run(prompt, context=context)
        elif isinstance(agent, LocalAgent):
            return agent.run(prompt, context=context)
        else:
            # last-resort: call llm directly
            return self.llm_call(prompt)


# -------------------- Utilities --------------------

def truncate_for_prompt(obj: Any, limit: int = 1500) -> str:
    s = json.dumps(obj, default=str)
    return s if len(s) <= limit else s[:limit] + '...'


# -------------------- CLI / Example --------------------
if __name__ == "__main__":
    print("CrewAI + LangChain multi-agent coordinator example")
    # Build llm callable (falls back to a stub if no API key)
    try:
        llm_call = build_llm_callable_from_gemini()
    except Exception as e:
        print("Warning: Gemini not fully configured; using local stub. Error:", e)
        def llm_call(prompt: str) -> str:
            return json.dumps({"stub": True, "prompt": prompt[:400]})

    coord = Coordinator(llm_call)
    sample_inputs = {
        "meal_name": "Chicken Stir Fry",
        "servings": 4,
        "budget": "$25",
        "dietary_restrictions": ["no nuts"],
        "cooking_skill": "beginner"
    }
    out = coord.run_sequential(sample_inputs)
    print("\n=== Summary Output ===")
    try:
        print(json.dumps(out, indent=2, default=str))
    except Exception:
        print(out)
