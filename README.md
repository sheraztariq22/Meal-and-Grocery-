Meal & Grocery Planner

A complete multi-agent meal planning system using CrewAI, LangChain, and Google Gemini.

## Features

- **Multi-Agent Coordination**: Meal Planner, Shopping Organizer, Budget Advisor, Leftover Manager, Report Compiler
- **Web Recipe Search**: Real-time recipe research via web search
- **Organized Shopping Lists**: Grouped by store sections for efficient shopping
- **Budget Analysis**: Cost tracking and money-saving tips
- **Leftover Management**: Minimize food waste with creative recipes
- **Google Gemini Integration**: Powered by Google's latest LLM
- **Fallback Mode**: Works without API keys using local agent stubs

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Gemini API Key

**Option A: Using .env file (Recommended)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_actual_key_here
```

Get a free API key: https://ai.google.dev/

**Option B: Using Environment Variable**

```bash
export GEMINI_API_KEY="your_key_here"    # macOS / Linux
setx GEMINI_API_KEY "your_key_here"      # Windows (PowerShell restart required)
```

### 3. Run the System

```bash
python main.py
```

This runs a complete workflow and outputs results to `workflow_results.json`.

## Configuration

### .env File (Recommended)

Copy `.env.example` to `.env` and configure:

```
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here  # Optional, for web search
DEBUG=false
```

**Important:** The `.env` file is in `.gitignore` - it will never be committed.

### Without .env

Set environment variables directly:

```bash
export GEMINI_API_KEY="your_key"
python main.py
```

## Project Structure

```
├── main.py                     # Primary entry point (NEW)
├── crewai_multi_agent.py       # Multi-agent coordinator
├── leftover.py                 # YAML-based leftover manager
├── config/
│   ├── agents.yaml             # Agent configurations
│   └── tasks.yaml              # Task configurations
├── meal_planner.py             # DEPRECATED (see main.py)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .gitignore                  # Git ignore patterns
```

## Architecture

```
┌─────────────────┐
│  main.py        │ (Entry point)
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Coordinator (CrewAI)            │
├──────────────────────────────────┤
│  1. Meal Planner (web search)    │
│  2. Shopping Organizer           │
│  3. Budget Advisor               │
│  4. LeftoversCrew (YAML-based)   │
│  5. Report Compiler              │
└──────────────────────────────────┘
         │
         ▼
  Google Gemini API
  (or local fallback)
```

## Module Details

### main.py
Primary entry point that orchestrates all agents and displays results.

### crewai_multi_agent.py
- `Coordinator` class: Manages sequential agent workflow
- `GeminiWrapper`: Handles Google Gemini API calls
- Pydantic models for structured data
- Local agent stubs for fallback mode

### leftover.py
YAML-based CrewAI module for food waste reduction using `@CrewBase` decorator.

## Usage Examples

### Basic Run (Default)
```bash
python main.py
```

### With Custom Inputs
Edit `main.py` and modify the `sample_inputs` dictionary:

```python
sample_inputs = {
    "meal_name": "Pasta Primavera",
    "servings": 2,
    "budget": "$15",
    "dietary_restrictions": ["vegetarian"],
    "cooking_skill": "intermediate"
}
```

### Programmatic Usage
```python
from crewai_multi_agent import Coordinator, build_llm_callable_from_gemini

llm_call = build_llm_callable_from_gemini()
coordinator = Coordinator(llm_call, use_leftovers_crew=True)

results = coordinator.run_sequential({
    "meal_name": "Chicken Stir Fry",
    "servings": 4,
    "budget": "$25",
    "dietary_restrictions": ["no nuts"],
    "cooking_skill": "beginner"
})

print(results['summary'])
```

## API Key Management

### Using .env File (Recommended)

1. **Create `.env` from the example:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your credentials:**
   ```
   GEMINI_API_KEY=sk_...your_key...
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

The `.env` file is automatically loaded by both `main.py` and `crewai_multi_agent.py`.

### Using Environment Variables

```bash
export GEMINI_API_KEY="your_key"
python main.py
```

### Security Best Practices

- ✅ Use `.env` files for local development (never commit)
- ✅ Use environment variables in CI/CD pipelines
- ✅ Use secrets management services in production
- ❌ Never hardcode API keys in source files
- ❌ Never commit `.env` to version control (already in `.gitignore`)
- ❌ Never share credentials in pull requests or issues

## Fallback Mode

If you don't have a Gemini API key or dependencies installed, the system runs in **fallback mode** using local agent stubs. This allows testing without real API calls.

## Dependencies

- `crewai==0.141.0` - Multi-agent orchestration
- `langchain==0.3.20` - LLM chain management
- `google-generativeai>=0.3.0` - Google Gemini API
- `pydantic>=1.10` - Data validation
- `ruamel.yaml>=0.17.0` - YAML parsing
