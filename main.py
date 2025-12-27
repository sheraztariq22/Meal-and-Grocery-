#!/usr/bin/env python3
"""
Main entry point for the Meal & Grocery Planner with CrewAI + LangChain

This module orchestrates:
1. Meal Planner Agent - researches recipes via web search
2. Shopping Organizer Agent - organizes shopping list by store sections
3. Budget Advisor Agent - analyzes costs and suggests savings
4. LeftoversCrew - manages food waste and leftover ingredients
5. Report Compiler Agent - creates final comprehensive guide

Usage:
    python main.py

Environment variables can be set via:
    - .env file (recommended)
    - shell environment variables (export GEMINI_API_KEY="...")

Set GEMINI_API_KEY in your .env or environment for real LLM calls.
"""

import sys
import os
import json
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_file = Path(".env")
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✓ Loaded environment from {env_file}\n")
except ImportError:
    pass  # python-dotenv not installed

from crewai_multi_agent import Coordinator, build_llm_callable_from_gemini

def print_banner():
    print("\n" + "="*70)
    print("  🍽️  Meal & Grocery Planner with CrewAI + LangChain + Google Gemini")
    print("="*70 + "\n")

def print_results(results: dict):
    print("\n" + "-"*70)
    print("📋 Multi-Agent Workflow Results")
    print("-"*70 + "\n")
    
    for stage, output in results.items():
        print(f"\n✓ {stage.upper().replace('_', ' ')}")
        print("  " + "-"*60)
        
        # Truncate output for readability
        if isinstance(output, str):
            lines = output.split("\n")
            preview = "\n  ".join(lines[:5])
            if len(lines) > 5:
                preview += f"\n  ... ({len(lines) - 5} more lines)"
            print(f"  {preview}")
        else:
            print(f"  {json.dumps(output, indent=2)[:500]}")

def main():
    print_banner()
    
    # Check for API key (from .env or environment)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  GEMINI_API_KEY not found.")
        print("   Running in FALLBACK mode (local agent stubs only).\n")
        print("   To enable real LLM calls, create a .env file:")
        print("     cp .env.example .env")
        print("     # Edit .env and add your GEMINI_API_KEY\n")
        print("   Or set environment variable:")
        print("     export GEMINI_API_KEY='your_key_here'\n")
    else:
        print("✓ GEMINI_API_KEY loaded from environment or .env file.")
        print(f"   Key: {api_key[:10]}...{api_key[-5:]}\n")
    
    # Build LLM callable (will use stub if no API key)
    try:
        llm_call = build_llm_callable_from_gemini(api_key=api_key)
    except Exception as e:
        print(f"⚠️  Could not initialize Gemini: {e}")
        print("   Using local stub mode.\n")
        def llm_call(prompt: str) -> str:
            return json.dumps({"stub": True, "prompt": prompt[:400]})
    
    # Initialize coordinator (with LeftoversCrew integration)
    print("🤖 Initializing Multi-Agent Coordinator...\n")
    coordinator = Coordinator(llm_call, use_leftovers_crew=True)
    
    # Sample meal planning request
    sample_inputs = {
        "meal_name": "Chicken Stir Fry",
        "servings": 4,
        "budget": "$25",
        "dietary_restrictions": ["no nuts"],
        "cooking_skill": "beginner"
    }
    
    print("📝 Starting Meal Planning Workflow...\n")
    print(f"   Meal: {sample_inputs['meal_name']}")
    print(f"   Servings: {sample_inputs['servings']}")
    print(f"   Budget: {sample_inputs['budget']}")
    print(f"   Restrictions: {', '.join(sample_inputs['dietary_restrictions'])}")
    print(f"   Skill Level: {sample_inputs['cooking_skill']}\n")
    
    # Run the workflow
    results = coordinator.run_sequential(sample_inputs)
    
    # Display results
    print_results(results)
    
    # Save results to file
    output_file = "workflow_results.json"
    try:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n✓ Results saved to {output_file}")
    except Exception as e:
        print(f"\n⚠️  Could not save results: {e}")
    
    print("\n" + "="*70)
    print("✅ Workflow completed!\n")
    print("📚 Next steps:")
    print("   1. Check workflow_results.json for full output")
    print("   2. Set GEMINI_API_KEY for real LLM integration")
    print("   3. Customize inputs in main.py for your meals")
    print("   4. See README.md for more information\n")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
