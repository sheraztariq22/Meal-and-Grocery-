Meal & Grocery Planner

- Module: `meal_planner.py`

Quick start

1. Install minimal deps:

```bash
python -m pip install -r requirements.txt
```

2. Provide `meals.json` in the workspace root (same folder as `meal_planner.py`). The file should be a list of meals. Example entry:

```json
[
  {
    "name": "Spaghetti Bolognese",
    "tags": ["dinner", "meat"],
    "ingredients": [
      {"name": "spaghetti", "quantity": 200, "unit": "g"},
      {"name": "ground beef", "quantity": 300, "unit": "g"}
    ]
  }
]
```

3. Run the simple local planner:

```bash
python meal_planner.py
```

4. Integrate Google Gemini / LangChain:

- Implement a function that accepts a string prompt and returns the model's string response.
- Pass that function as `model_call` to `generate_meal_plan()`.

Security

- Do not commit API keys. Use environment variables or a local credential file kept out of source control.

LangChain + CrewAI integration

- To run the multi-agent coordinator that uses Google Gemini and CrewAI, see `crewai_multi_agent.py`.
- Set `GEMINI_API_KEY` in your environment before running for real LLM calls:

```bash
export GEMINI_API_KEY="your_key_here"    # macOS / Linux
setx GEMINI_API_KEY "your_key_here"      # Windows (PowerShell restart required)
```

- Install optional dependencies for full functionality:

```bash
python -m pip install crewai langchain google-generativeai pydantic ruamel.yaml
```

- Run the coordinator locally (fallback mode works without optional deps):

```bash
python crewai_multi_agent.py
```

- The module is defensive: if `google-generativeai` or `crewai` are not installed, it falls back to local agent stubs that simulate behaviour.
