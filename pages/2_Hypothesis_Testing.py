import streamlit as st
import pandas as pd
import numpy as np
from utils.chem_data import get_chemistry_topics, get_experiment_types

# Set page title
st.title("Hypothesis Formulation")
st.markdown("### Develop a testable hypothesis for your chemistry IA")

# Initialize session state variables if they don't exist
if 'hypothesis' not in st.session_state:
    st.session_state.hypothesis = ""
if 'null_hypothesis' not in st.session_state:
    st.session_state.null_hypothesis = ""
if 'alternative_hypothesis' not in st.session_state:
    st.session_state.alternative_hypothesis = ""
if 'rationale' not in st.session_state:
    st.session_state.rationale = ""

# Display guidance for formulating a good hypothesis
st.subheader("Hypothesis Guidance")

st.markdown("""
### Characteristics of a Good Hypothesis
A well-formulated hypothesis for an IB Chemistry IA should be:

1. **Testable**: Can be measured and analyzed using available equipment
2. **Specific**: Clearly identifies variables and expected relationships
3. **Based on research**: Grounded in scientific principles
4. **Directional**: Predicts the direction of the relationship (if applicable)
5. **Concise**: Stated clearly and effectively

### Hypothesis Format

A good hypothesis typically follows this structure:

> "If [independent variable] is [changed in this way], then [dependent variable] will [expected effect] because [scientific rationale]."

For example:
> "If the concentration of hydrochloric acid is increased, then the rate of reaction with magnesium will increase because there will be more frequent collisions between acid particles and the magnesium surface."
""")

# Topic and experiment reminder
if 'experiment_topic' in st.session_state and 'experiment_type' in st.session_state:
    if st.session_state.experiment_topic and st.session_state.experiment_type:
        st.info(f"Your selected topic is **{st.session_state.experiment_topic}** and experiment type is **{st.session_state.experiment_type}**")
else:
    st.warning("Please complete the Experiment Planning section first to define your experiment topic and type.")

# Step 1: Formulate scientific hypothesis
st.subheader("Step 1: Formulate Your Scientific Hypothesis")

st.markdown("Your hypothesis should predict the relationship between your independent and dependent variables.")

if 'independent_var' in st.session_state and 'dependent_var' in st.session_state:
    if st.session_state.independent_var and st.session_state.dependent_var:
        st.markdown(f"""
        **Remember:**
        - Your independent variable is: *{st.session_state.independent_var}*
        - Your dependent variable is: *{st.session_state.dependent_var}*
        """)

st.session_state.hypothesis = st.text_area(
    "Enter your hypothesis (If... then... because...)",
    value=st.session_state.hypothesis,
    height=100,
    help="State your prediction about how the independent variable will affect the dependent variable and why"
)

# Step 2: Statistical Hypotheses
st.subheader("Step 2: Statistical Hypotheses")

st.markdown("""
For statistical testing, you need to formulate null and alternative hypotheses:

- **Null Hypothesis (H₀)**: States that there is no effect or relationship between variables
- **Alternative Hypothesis (H₁)**: States that there is an effect or relationship between variables
""")

st.session_state.null_hypothesis = st.text_area(
    "Null Hypothesis (H₀)",
    value=st.session_state.null_hypothesis,
    height=80,
    help="Usually states that there is no effect or relationship between variables"
)

st.session_state.alternative_hypothesis = st.text_area(
    "Alternative Hypothesis (H₁)",
    value=st.session_state.alternative_hypothesis,
    height=80,
    help="States the effect or relationship you expect to observe"
)

# Step 3: Scientific Rationale
st.subheader("Step 3: Scientific Rationale")

st.markdown("""
Provide the scientific reasoning behind your hypothesis. This should be based on:
- Chemical principles relevant to your experiment
- Previous research or established theories
- Your understanding of the underlying mechanisms
""")

st.session_state.rationale = st.text_area(
    "Scientific Rationale",
    value=st.session_state.rationale,
    height=150,
    help="Explain the scientific principles that support your hypothesis"
)

# Step 4: Hypothesis Evaluation
if st.session_state.hypothesis and st.session_state.null_hypothesis and st.session_state.alternative_hypothesis:
    st.subheader("Step 4: Hypothesis Evaluation")
    
    evaluation_criteria = [
        "Is your hypothesis testable with your available equipment?",
        "Does your hypothesis clearly specify the relationship between variables?",
        "Is your hypothesis based on scientific principles?",
        "Does your hypothesis predict a direction or magnitude of effect?",
        "Is your hypothesis concise and clearly stated?"
    ]
    
    st.markdown("Check if your hypothesis meets these criteria:")
    
    for criterion in evaluation_criteria:
        st.checkbox(criterion)
    
    # Provide suggested improvements based on best practices
    st.markdown("### Suggested Improvements")
    
    # Check for common issues in hypotheses
    suggestions = []
    
    if "because" not in st.session_state.hypothesis.lower():
        suggestions.append("- Include a scientific explanation (because...) in your hypothesis")
    
    if "if" not in st.session_state.hypothesis.lower() or "then" not in st.session_state.hypothesis.lower():
        suggestions.append("- Format your hypothesis as 'If [independent variable change], then [expected effect]'")
    
    if len(st.session_state.hypothesis.split()) < 15:
        suggestions.append("- Consider adding more detail to your hypothesis")
    
    if suggestions:
        for suggestion in suggestions:
            st.markdown(suggestion)
    else:
        st.success("Your hypothesis appears to be well-formulated!")

# Save hypothesis
if st.session_state.hypothesis and st.session_state.null_hypothesis and st.session_state.alternative_hypothesis and st.session_state.rationale:
    if st.button("Save Hypothesis"):
        st.success("Hypothesis saved successfully! Continue to Data Analysis.")
        
        # Summary of formulated hypotheses
        st.subheader("Hypothesis Summary")
        
        summary_md = f"""
        **Scientific Hypothesis:**  
        {st.session_state.hypothesis}
        
        **Null Hypothesis (H₀):**  
        {st.session_state.null_hypothesis}
        
        **Alternative Hypothesis (H₁):**  
        {st.session_state.alternative_hypothesis}
        
        **Scientific Rationale:**  
        {st.session_state.rationale}
        """
        
        st.markdown(summary_md)
