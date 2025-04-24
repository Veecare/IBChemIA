import streamlit as st
import pandas as pd
import numpy as np
from utils.chem_data import get_chemistry_topics

# Set page configuration
st.set_page_config(
    page_title="IB Chemistry IA Planner",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page header
st.title("IB Chemistry Internal Assessment Planner")
st.markdown("### A comprehensive tool for planning and analyzing chemistry experiments")

# Introduction
st.markdown("""
This application is designed to help IB Chemistry students plan and execute 
their Internal Assessment experiments. Use the sidebar to navigate through different 
features of the application:

- **Experiment Planning**: Design your experiment with proper controls and variables
- **Hypothesis Testing**: Formulate testable hypotheses aligned with IB criteria
- **Data Analysis**: Analyze your collected data with appropriate statistical methods
- **Error Analysis**: Calculate uncertainties and identify sources of error
- **Report Generation**: Create a well-structured IA report based on your work
""")

# Display key features
col1, col2 = st.columns(2)

with col1:
    st.subheader("Why use this tool?")
    st.markdown("""
    - Specifically designed for IB Chemistry requirements
    - Guides you through the entire IA process
    - Helps formulate appropriate hypotheses
    - Performs statistical analysis with proper interpretation
    - Calculates experimental uncertainties
    - Provides templates for common chemistry experiments
    - Creates professional reports that meet IB standards
    """)

with col2:
    st.subheader("Getting Started")
    st.markdown("""
    1. Begin by selecting "Experiment Planning" in the sidebar
    2. Choose a chemistry topic and experiment type
    3. Define your variables (independent, dependent, controlled)
    4. Formulate your hypothesis using the guidance provided
    5. Plan your methodology and collect data
    6. Analyze your results and perform statistical tests
    7. Generate a complete IA report
    """)

# Display chemistry topics covered
st.subheader("Chemistry Topics Covered")
topics = get_chemistry_topics()
cols = st.columns(3)
for i, topic in enumerate(topics):
    cols[i % 3].markdown(f"- {topic}")

# Usage instructions
st.info("""
**Note for students**: This tool will help you structure your IA, but remember that the 
quality of your experimental design, data collection, and analysis are key to a successful IA. 
Always consult with your chemistry teacher throughout the process.
""")
