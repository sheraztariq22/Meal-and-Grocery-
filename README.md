# 🍽️ Meal & Grocery Planner with CrewAI

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/downloads/)
[![CrewAI 0.141.0](https://img.shields.io/badge/CrewAI-0.141.0-green)](https://crewai.io)
[![LangChain 0.3.20](https://img.shields.io/badge/LangChain-0.3.20-orange)](https://langchain.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **production-ready intelligent meal planning and grocery shopping assistant** powered by **CrewAI**, **LangChain**, and **Google Gemini**. This system uses a multi-agent architecture to coordinate specialized AI agents for meal research, shopping organization, budget analysis, and waste reduction.

> **🎯 Perfect for**: Home cooks, meal planners, budget-conscious shoppers, and those who want to minimize food waste.

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Directory Structure](#-directory-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Troubleshooting](#-troubleshooting)
- [API Keys](#-api-keys)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)

---

## ✨ Features

### 🤖 Multi-Agent System
- **Meal Planner Agent**: Researches recipes and creates meal plans based on preferences
- **Shopping Organizer Agent**: Structures groceries by store sections for efficient shopping
- **Budget Advisor Agent**: Analyzes costs and provides money-saving recommendations
- **Leftovers Manager Agent**: Suggests creative recipes to use leftover ingredients
- **Summary Agent**: Compiles comprehensive shopping guides

### 🎯 Core Capabilities
- ✅ **Intelligent Meal Planning** - AI-powered recipe research and meal design
- ✅ **Smart Grocery Organization** - Auto-grouped shopping lists by store section
- ✅ **Budget Optimization** - Real-time cost analysis and savings suggestions
- ✅ **Waste Reduction** - Creative leftover meal suggestions
- ✅ **Dietary Restrictions** - Supports vegetarian, vegan, gluten-free, dairy-free, nut allergies
- ✅ **Skill-Level Adaptation** - Tailored recipes for beginner to advanced cooks
- ✅ **Web Search Integration** - DuckDuckGo search for up-to-date recipes
- ✅ **Export Options** - Download plans as JSON or Markdown

### 🖥️ Interfaces
- **Streamlit Web UI** - Modern, interactive interface for meal planning (Recommended)
- **Python CLI** - Command-line interface for batch processing
- **Python API** - Programmatic integration into larger applications

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Gemini API Key

**Get API Key:** https://ai.google.dev/

**Option A: Using .env file (Recommended)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_actual_key_here
```

**Option B: Using Environment Variable**

```bash
export GEMINI_API_KEY="your_key_here"    # macOS / Linux
setx GEMINI_API_KEY "your_key_here"      # Windows
```

### 3. Run the Application

**Streamlit Web Interface (Recommended):**
```bash
streamlit run streamlit_app.py
# Opens at: http://localhost:8501
```

**Command-Line Interface:**
```bash
python main.py
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│         Streamlit Web Interface (UI)                │
│  - Beautiful, interactive meal planning             │
│  - Real-time results display                        │
│  - Export to JSON/Markdown                          │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│      Coordinator (Multi-Agent Orchestration)        │
│  - Sequential workflow management                   │
│  - Fallback error handling                          │
│  - Result aggregation                               │
├─────────────────────────────────────────────────────┤
│  LLM Callable (Google Gemini or Local Stub)         │
│  - Gemini API calls with retry logic                │
│  - Graceful degradation when offline                │
└────────────────────┬────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┬──────────────┐
     │               │               │              │
  ┌──▼──┐       ┌───▼────┐    ┌────▼────┐   ┌────▼────┐
  │Meal │       │Shopping│    │ Budget   │   │Leftovers│
  │Plan │       │Organizer    │ Advisor  │   │ Manager │
  │Agent│       │        │    │          │   │         │
  └──┬──┘       └───┬────┘    └────┬────┘   └────┬────┘
     │               │             │             │
     └───────────────┼─────────────┼─────────────┘
                     │
                 ┌───▼──────┐
                 │  Summary  │
                 │  Agent    │
                 └───┬───────┘
                     │
            ┌────────▼────────┐
            │  JSON Output &  │
            │  Markdown File  │
            └─────────────────┘
```

### Agent Workflow (Sequential)

1. **Meal Planner** 🍳
   - Researches recipes matching meal name, servings, budget, restrictions
   - Returns ingredients list, difficulty level, cooking instructions

2. **Shopping Organizer** 🛒
   - Structures ingredients by store sections (Produce, Dairy, Meat, etc.)
   - Adds quantities and estimated prices

3. **Budget Advisor** 💰
   - Analyzes total cost vs. budget
   - Suggests cheaper alternatives
   - Provides money-saving tips

4. **Leftovers Manager** ♻️
   - Identifies partial-use ingredients
   - Suggests 2-3 bonus recipes using leftovers
   - Helps minimize food waste

5. **Summary Agent** 📋
   - Compiles all information into user-friendly guide
   - Generates final shopping and meal plan

---

## 📁 Directory Structure

```
Meal and Grocery System-CrewAI/
│
├── 📄 README.md                          # Complete documentation (this file)
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .env.example                       # Environment variables template
├── 📄 .gitignore                         # Git ignore rules
│
├── 📄 main.py                            # CLI entry point (run: python main.py)
├── 📄 streamlit_app.py                   # Web UI (run: streamlit run streamlit_app.py)
├── 📄 crewai_multi_agent.py              # Core coordinator & agents
├── 📄 leftover.py                        # LeftoversCrew YAML-based implementation
├── 📄 meal_planner.py                    # [DEPRECATED] Legacy simple planner
│
├── 📄 meals.json                         # Sample meal data
├── 📄 shopping_guide.md                  # Sample output document
├── 📄 shopping_list.json                 # Sample shopping list
│
├── 📁 config/                            # Agent & Task YAML configuration
│   ├── agents.yaml                       # Agent definitions (role, goal, backstory)
│   └── tasks.yaml                        # Task definitions (description, output)
│
├── 📁 venv/                              # Python virtual environment (auto-created)
│   ├── Scripts/                          # Windows executables (pip, python, etc.)
│   ├── Lib/                              # Installed packages
│   ├── bin/                              # Unix executables
│   └── pyvenv.cfg                        # Environment config
│
└── 📁 __pycache__/                       # Python cache files (auto-generated)
```

### Key Files Overview

| File | Purpose | Run Command |
|------|---------|-------------|
| `main.py` | CLI entry point - runs full workflow from command line | `python main.py` |
| `streamlit_app.py` | Web UI built with Streamlit - interactive and beautiful | `streamlit run streamlit_app.py` |
| `crewai_multi_agent.py` | Core module with Coordinator, agents, and LLM wrapper | Import in code |
| `leftover.py` | YAML-based LeftoversCrew using @CrewBase decorator | Auto-loaded |
| `config/agents.yaml` | Defines agent roles, goals, and behaviors | Referenced by LeftoversCrew |
| `config/tasks.yaml` | Defines task descriptions and expected outputs | Referenced by LeftoversCrew |
| `.env.example` | Template for environment variables (copy to `.env`) | Copy & configure |

---

## 💻 Installation

### Prerequisites

- **Python**: 3.11 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: ~500MB for dependencies
- **Internet**: Required for API calls

### Step-by-Step Installation

#### Step 1: Download Project

```bash
# If using git
git clone <repository-url>
cd "Meal and Grocery System-CrewAI"

# Or manually download and extract ZIP file
```

#### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

#### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip
```

#### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs ~50 packages including:
- CrewAI, LangChain, Google Gemini
- Streamlit for web interface
- Pydantic for data validation
- And supporting libraries

**Expected output:**
```
Successfully installed crewai-0.141.0 langchain-0.3.20 streamlit-1.52.2 ... (50+ packages)
```

#### Step 5: Verify Installation

```bash
python -c "import crewai; import streamlit; import google.genai; print('✓ All packages installed!')"
```

---

## 🔐 Configuration

### Step 1: Get API Keys

#### Google Gemini API Key (Required)
1. Visit: https://ai.google.dev/
2. Click **"Get API Key"**
3. Create new Google Cloud project or select existing
4. Copy your API key (looks like: `AIzaSyD...`)

#### Serper API Key (Optional, for enhanced search)
1. Visit: https://serper.dev/
2. Sign up for free tier
3. Copy API key from dashboard

### Step 2: Create .env File

```bash
# Copy the example file
cp .env.example .env

# On Windows, if cp doesn't work:
copy .env.example .env
```

### Step 3: Configure .env File

Open `.env` in text editor and add:

```env
# Google Gemini API Key (REQUIRED)
GEMINI_API_KEY=AIzaSyD...your_actual_key...

# Serper API Key (Optional)
SERPER_API_KEY=your_serper_key_here

# Application settings (Optional)
DEBUG=false
LOG_LEVEL=INFO
```

### Step 4: Verify Configuration

The app automatically loads `.env` when started. You'll see:
```
✓ Loaded environment from .env
✓ GEMINI_API_KEY loaded from environment or .env file.
   Key: AIzaSyD...4fEcQ
```

---

## 🚀 Usage

### Option 1: Streamlit Web Interface ⭐ (Recommended)

**Start the app:**
```bash
streamlit run streamlit_app.py
```

**Access in browser:**
- Local: http://localhost:8501
- Network: http://<your-ip>:8501

**How to use:**

1. **📝 Configure preferences** (Left sidebar):
   - Meal name: "Chicken Stir Fry" (example)
   - Servings: 1-20 people
   - Budget: $5-$500
   - Dietary restrictions: Multi-select options
   - Cooking skill: Beginner/Intermediate/Advanced

2. **🚀 Click "Generate Meal & Shopping Plan"**
   - Shows progress spinners
   - Processes through all 5 agents

3. **📊 View results** in 5 tabs:
   - 🍽️ Meal Plan - Recipe details
   - 🛒 Shopping List - Organized by section
   - 💡 Budget Analysis - Cost breakdown & tips
   - 🔄 Leftovers - Bonus recipes
   - 📋 Summary - Complete guide

4. **📥 Download results:**
   - 📄 JSON - Structured data format
   - 📝 Markdown - Readable document

5. **🔄 Clear** - Reset and start over

### Option 2: Command-Line Interface

**Run:**
```bash
python main.py
```

**Output:**
- Displays results in terminal
- Saves to `workflow_results.json`

**Custom inputs:**

Edit `main.py` line ~110:

```python
sample_inputs = {
    "meal_name": "Pasta Primavera",  # Change meal
    "servings": 2,                   # Change servings
    "budget": 15,                    # Change budget
    "restrictions": "vegetarian",    # Change restrictions
    "skill_level": "intermediate"    # Change skill
}
```

Then run: `python main.py`

### Option 3: Python API

**Use in your code:**

```python
from crewai_multi_agent import Coordinator, build_llm_callable_from_gemini

# Initialize
llm_call = build_llm_callable_from_gemini()
coordinator = Coordinator(llm_call=llm_call)

# Prepare inputs
inputs = {
    "meal_name": "Tacos",
    "servings": 4,
    "budget": 20,
    "restrictions": "none",
    "skill_level": "beginner"
}

# Run workflow
results = coordinator.run_sequential(inputs)

# Access results
print(results['meal_planner'])
print(results['shopping_organizer'])
print(results['budget_advisor'])
print(results['leftovers'])
print(results['summary'])
```

---

## 🔑 API Keys & Quotas

### Google Gemini API

**Free Tier Limits:**
- 15 requests per minute
- 500,000 requests per day
- Per-model quotas apply

**Monitor usage:** https://ai.google.dev/usage

**Upgrade options:**
- Free tier: Great for testing
- Paid tiers: More requests & better models
- Enterprise: Custom limits

**Models available:**
- `gemini-1.5-flash` (default) - Fast, efficient, good for most tasks
- `gemini-2.0-flash` - Latest, more capable, slightly slower

### Serper API (Optional)

Used for enhanced web search in recipe research.

**Limits:**
- Free tier: 100 searches/month
- Paid tiers: More searches

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "GEMINI_API_KEY not set" Error

```
Error: GEMINI_API_KEY not set in environment and not provided
```

**Solutions:**
1. Verify `.env` file exists in project root
2. Check key format: `GEMINI_API_KEY=AIzaSyD...`
3. Save file (no trailing spaces)
4. Restart app
5. Verify: `echo $GEMINI_API_KEY` (Unix) or `echo %GEMINI_API_KEY%` (Windows)

#### 2. "429 RESOURCE_EXHAUSTED" Error

```
Error: You exceeded your current quota, please check your plan and billing details
```

**Solutions:**
- Free tier has rate limits (15 req/min)
- Wait 5 seconds and retry
- Upgrade plan at https://ai.google.dev/
- Use smaller prompts
- Batch requests together

#### 3. "ModuleNotFoundError" - Streamlit/CrewAI Missing

```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
# Ensure venv is activated
# Windows: .\venv\Scripts\Activate.ps1
# Unix: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 4. "LeftoversCrew failed: Missing template variable"

```
Warning: LeftoversCrew failed: Missing required template variable 'servings'
```

**Solution:**
- This is handled gracefully
- System continues without leftovers suggestions
- Verify `config/tasks.yaml` format
- Check all required variables in input dictionary

#### 5. Port 8501 Already in Use

```
Error: Address already in use
```

**Solution:**
```bash
# Kill existing process (Windows PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess | Stop-Process -Force

# Or use different port
streamlit run streamlit_app.py --server.port 8502
```

#### 6. Virtual Environment Not Activating

```
(venv) prompt not appearing
```

**Solution - Windows PowerShell:**
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv\Scripts\Activate.ps1
```

**Solution - Others:**
```bash
source venv/bin/activate  # macOS/Linux
```

#### 7. "Connection Error" or "Network Timeout"

```
Error: Connection refused or timeout
```

**Solutions:**
- Check internet connection
- Check firewall settings
- Try with VPN disabled
- Check API status: https://status.cloud.google.com/

### Getting Help

1. **Check error logs** - Streamlit shows detailed messages
2. **Verify API key** - Test in Python:
   ```python
   import os
   print(os.environ.get('GEMINI_API_KEY'))
   ```
3. **Test dependencies** - `pip list | grep crewai`
4. **Check internet** - `ping google.com`

---

## 📦 Dependencies

### Core AI/ML Stack
```
crewai==0.141.0              Multi-agent orchestration framework
langchain==0.3.20            LLM chain management
langchain-community==0.3.19  Community integrations
google-genai>=0.1.0          Google Gemini new API
google-generativeai>=0.3.0   Gemini API fallback
pydantic>=1.10               Data validation with types
```

### Web & Search
```
duckduckgo-search==7.5.2     Fallback web search
requests>=2.28               HTTP requests library
```

### UI & Configuration
```
streamlit>=1.28.0            Interactive web interface
python-dotenv>=1.0.0         Environment variable loading
pyyaml>=6.0                  YAML configuration parsing
ruamel.yaml>=0.17.0          Advanced YAML support
```

### Transitive Dependencies
~40 additional packages for async, utilities, and AI support

See [requirements.txt](requirements.txt) for complete list.

---

## 🏢 Project Components

### crewai_multi_agent.py

**Key Classes:**
- `GeminiWrapper` - Wraps Google Gemini API with fallback
- `LocalAgent` - Fallback agent when CrewAI unavailable
- `Coordinator` - Orchestrates 5-agent sequential workflow

**Pydantic Models (Type-Safe Data):**
- `GroceryItem` - Single grocery item with quantity & price
- `MealPlan` - Meal with ingredients & difficulty
- `ShoppingCategory` - Group of items by store section
- `GroceryShoppingPlan` - Complete shopping plan

**Helper Functions:**
- `build_llm_callable_from_gemini()` - Creates LLM callable
- `build_agent_stubs()` - Creates local agent fallbacks
- `truncate_for_prompt()` - Limits prompt size

### streamlit_app.py

**Features:**
- Interactive sidebar with meal preferences
- Real-time result display with 5 tabs
- JSON/Markdown export buttons
- Status indicators and progress spinners
- Session state management
- Error handling with helpful tips

### config/agents.yaml

```yaml
leftover_manager:
  role: "Leftover Manager"
  goal: "Identify uses for leftover ingredients"
  backstory: "Expert at reducing food waste..."
  tools: []
```

### config/tasks.yaml

```yaml
leftover_task:
  description: "Analyze meal '{meal_name}' for {servings} people..."
  expected_output: "List of bonus recipes using leftovers..."
  agent: leftover_manager
```

---

## 🚀 Performance Tips

### Optimize for Speed
1. Use `gemini-1.5-flash` (default)
2. Keep inputs concise
3. Set `DEBUG=false` in `.env`
4. Streamlit caches automatically

### Optimize for Quality
1. Provide detailed dietary restrictions
2. Match cooking skill level to recipes
3. Use `gemini-2.0-flash` for complex meals

### Cost Optimization
- Free tier: ~1.5M tokens/month
- Monitor at: https://ai.google.dev/usage
- Batch multiple meals together
- Cache results for similar requests

---

## 📝 Customization

### Change Default Meal

Edit `streamlit_app.py` line ~45:
```python
meal_name = st.text_input(
    "🍲 Meal Name",
    value="Your Default Meal",  # Change here
)
```

### Add Dietary Restrictions

Edit `streamlit_app.py` line ~64:
```python
options=["None", "Vegetarian", "Vegan", "Gluten-free", 
         "Dairy-free", "Nut allergies", "Keto", "Paleo"],  # Add here
```

### Customize Agent Behavior

Edit `config/agents.yaml`:
```yaml
leftover_manager:
  role: "Food Waste Reduction Expert"  # Customize
  goal: "Minimize waste and maximize ingredient usage"
  backstory: "An eco-conscious chef specialized in..."
```

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Credits

- **CrewAI** - Multi-agent framework: https://crewai.io
- **LangChain** - LLM orchestration: https://langchain.com
- **Google Gemini** - Large language model: https://ai.google.dev
- **Streamlit** - Web UI framework: https://streamlit.io
- **DuckDuckGo** - Search integration

---

## 📞 Support Resources

- 📖 **CrewAI Docs**: https://crewai.io/docs
- 📚 **LangChain Docs**: https://python.langchain.com/docs
- 🔍 **Google Gemini Guide**: https://ai.google.dev/tutorials
- 💬 **Streamlit Docs**: https://docs.streamlit.io

---

**Made with ❤️ for better meal planning**

*Last Updated: December 27, 2025*

