"""
Streamlit interface for the Meal & Grocery Planner with CrewAI + Gemini.

Run with: streamlit run streamlit_app.py
"""
import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from crewai_multi_agent import Coordinator, build_llm_callable_from_gemini

# Configure page
st.set_page_config(
    page_title="🍽️ Meal & Grocery Planner",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 0;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and header
st.markdown("# 🍽️ Meal & Grocery Planner")
st.markdown("**An intelligent meal planning and grocery shopping assistant powered by CrewAI + Google Gemini**")
st.divider()

# Initialize session state for storing results
if "results" not in st.session_state:
    st.session_state.results = None
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

# Sidebar for inputs
with st.sidebar:
    st.markdown("## 📝 Planning Preferences")
    
    # Meal input
    meal_name = st.text_input(
        "🍲 Meal Name",
        value="Chicken Stir Fry",
        help="Enter the name of the meal you want to plan"
    )
    
    # Servings
    servings = st.number_input(
        "👥 Number of Servings",
        min_value=1,
        max_value=20,
        value=4,
        step=1,
        help="How many people will you be cooking for?"
    )
    
    # Budget
    budget = st.number_input(
        "💰 Budget ($)",
        min_value=5.0,
        max_value=500.0,
        value=25.0,
        step=1.0,
        help="Your total budget for groceries"
    )
    
    # Dietary restrictions
    restrictions = st.multiselect(
        "🚫 Dietary Restrictions",
        options=["None", "Vegetarian", "Vegan", "Gluten-free", "Dairy-free", "Nut allergies", "Other"],
        default=["None"],
        help="Select any dietary restrictions"
    )
    
    # Convert restrictions to string
    restrictions_str = ", ".join([r for r in restrictions if r != "None"]) or "none"
    
    # Skill level
    skill_level = st.select_slider(
        "👨‍🍳 Cooking Skill Level",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Beginner",
        help="Your cooking experience level"
    )
    
    st.divider()
    st.markdown("### ⚙️ Settings")
    
    # API configuration
    api_key_placeholder = st.checkbox("✓ API Key Configured", value=True, disabled=True)
    st.caption("Uses GEMINI_API_KEY from .env file")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Planning Details")
    plan_details = f"""
    - **Meal:** {meal_name}
    - **Servings:** {servings} people
    - **Budget:** ${budget:.2f}
    - **Restrictions:** {restrictions_str}
    - **Skill Level:** {skill_level}
    """
    st.info(plan_details)

with col2:
    st.markdown("### Status")
    if st.session_state.is_loading:
        st.warning("⏳ Processing...")
    elif st.session_state.results:
        st.success("✅ Planning Complete")
    else:
        st.info("👇 Click 'Generate Plan' to start")

# Main button
st.divider()

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    run_button = st.button(
        "🚀 Generate Meal & Shopping Plan",
        use_container_width=True,
        type="primary"
    )

with col2:
    if st.session_state.results:
        save_button = st.button(
            "💾 Save Results",
            use_container_width=True
        )
    else:
        save_button = False

with col3:
    if st.session_state.results:
        clear_button = st.button(
            "🔄 Clear",
            use_container_width=True
        )
    else:
        clear_button = False

# Handle clear button
if clear_button:
    st.session_state.results = None
    st.rerun()

# Handle generate button
if run_button:
    st.session_state.is_loading = True
    
    with st.spinner("🤖 Initializing Multi-Agent Coordinator..."):
        try:
            # Create LLM callable from Gemini
            llm_call = build_llm_callable_from_gemini()
            
            # Create coordinator with the LLM callable
            coordinator = Coordinator(llm_call=llm_call)
            
            # Prepare inputs
            sample_inputs = {
                "meal_name": meal_name,
                "servings": servings,
                "budget": budget,
                "restrictions": restrictions_str,
                "skill_level": skill_level
            }
            
            # Run the workflow
            with st.spinner("🧠 Running multi-agent workflow..."):
                results = coordinator.run_sequential(sample_inputs)
            
            st.session_state.results = results
            st.session_state.is_loading = False
            st.success("✅ Planning complete!")
            st.rerun()
            
        except Exception as e:
            st.session_state.is_loading = False
            st.error(f"❌ Error: {str(e)}")
            st.caption("Tip: Make sure your GEMINI_API_KEY is set in the .env file")

# Display results if available
if st.session_state.results:
    st.divider()
    st.markdown("## 📊 Results")
    
    tabs = st.tabs(["🍽️ Meal Plan", "🛒 Shopping List", "💡 Budget Analysis", "🔄 Leftovers", "📋 Summary"])
    
    results = st.session_state.results
    
    with tabs[0]:
        st.markdown("### Meal Planning Analysis")
        if "meal_planner" in results:
            meal_analysis = results["meal_planner"]
            st.markdown(meal_analysis)
        else:
            st.info("No meal plan generated yet")
    
    with tabs[1]:
        st.markdown("### Shopping List Organization")
        if "shopping_organizer" in results:
            shopping_list = results["shopping_organizer"]
            st.markdown(shopping_list)
        else:
            st.info("No shopping list generated yet")
    
    with tabs[2]:
        st.markdown("### Budget Analysis & Tips")
        if "budget_advisor" in results:
            budget_analysis = results["budget_advisor"]
            st.markdown(budget_analysis)
        else:
            st.info("No budget analysis generated yet")
    
    with tabs[3]:
        st.markdown("### Leftovers & Storage Guide")
        if "leftovers_crew" in results:
            leftovers_guide = results["leftovers_crew"]
            st.markdown(leftovers_guide)
        else:
            st.info("No leftovers guide generated yet")
    
    with tabs[4]:
        st.markdown("### Complete Planning Summary")
        if "summary_agent" in results:
            summary = results["summary_agent"]
            st.markdown(summary)
        else:
            st.info("No summary generated yet")
    
    # Export options
    st.divider()
    st.markdown("### 📥 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON export
        json_results = json.dumps(results, indent=2)
        st.download_button(
            label="📄 Download as JSON",
            data=json_results,
            file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        # Markdown export
        md_content = "# Meal & Grocery Plan\n\n"
        md_content += f"**Meal:** {meal_name}  \n"
        md_content += f"**Servings:** {servings}  \n"
        md_content += f"**Budget:** ${budget}  \n"
        md_content += f"**Restrictions:** {restrictions_str}  \n"
        md_content += f"**Skill Level:** {skill_level}  \n\n"
        
        for key, value in results.items():
            md_content += f"## {key.replace('_', ' ').title()}\n\n{value}\n\n"
        
        st.download_button(
            label="📝 Download as Markdown",
            data=md_content,
            file_name=f"meal_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

# Footer
st.divider()
st.markdown("""
---
**🍽️ Meal & Grocery Planner** | Powered by CrewAI + LangChain + Google Gemini

*Created for efficient meal planning and smart grocery shopping*
""")
