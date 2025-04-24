import streamlit as st
import pandas as pd
import numpy as np
from utils.chem_data import get_chemistry_topics, get_experiment_types, get_experiment_template, get_safety_info

# Set page title
st.title("Experiment Planning")
st.markdown("### Design your chemistry experiment according to IB requirements")

# Initialize session state variables if they don't exist
if 'experiment_topic' not in st.session_state:
    st.session_state.experiment_topic = ""
if 'experiment_type' not in st.session_state:
    st.session_state.experiment_type = ""
if 'independent_var' not in st.session_state:
    st.session_state.independent_var = ""
if 'dependent_var' not in st.session_state:
    st.session_state.dependent_var = ""
if 'controlled_vars' not in st.session_state:
    st.session_state.controlled_vars = []
if 'methodology' not in st.session_state:
    st.session_state.methodology = ""
if 'safety_considerations' not in st.session_state:
    st.session_state.safety_considerations = ""
if 'materials' not in st.session_state:
    st.session_state.materials = []

# Step 1: Select chemistry topic
st.subheader("Step 1: Select Chemistry Topic")
topics = get_chemistry_topics()
selected_topic = st.selectbox("Choose a chemistry topic for your IA", topics)

if selected_topic != st.session_state.experiment_topic:
    st.session_state.experiment_topic = selected_topic
    # Reset experiment type when topic changes
    st.session_state.experiment_type = ""

# Step 2: Select experiment type based on topic
if st.session_state.experiment_topic:
    st.subheader("Step 2: Select Experiment Type")
    experiment_types = get_experiment_types(st.session_state.experiment_topic)
    selected_experiment = st.selectbox("Choose an experiment type", experiment_types)
    
    if selected_experiment != st.session_state.experiment_type:
        st.session_state.experiment_type = selected_experiment
        # Get experiment template
        if selected_experiment:
            template = get_experiment_template(st.session_state.experiment_topic, selected_experiment)
            
            # Populate default values
            st.session_state.independent_var = template.get("independent_var", "")
            st.session_state.dependent_var = template.get("dependent_var", "")
            st.session_state.controlled_vars = template.get("controlled_vars", [])
            st.session_state.methodology = template.get("methodology", "")
            st.session_state.materials = template.get("materials", [])
            
            # Get safety info
            st.session_state.safety_considerations = get_safety_info(selected_experiment)

# Step 3: Define Variables
if st.session_state.experiment_type:
    st.subheader("Step 3: Define Experimental Variables")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Independent Variable")
        st.markdown("*What you will change in your experiment*")
        st.session_state.independent_var = st.text_area("Independent Variable", 
                                          value=st.session_state.independent_var,
                                          help="Describe what you will change and how you will measure it")
        
        st.markdown("##### Dependent Variable")
        st.markdown("*What you will measure as a result*")
        st.session_state.dependent_var = st.text_area("Dependent Variable", 
                                        value=st.session_state.dependent_var,
                                        help="Describe what you will measure and how you will measure it")
    
    with col2:
        st.markdown("##### Controlled Variables")
        st.markdown("*What you will keep constant*")
        
        # Convert controlled variables list to string for editing
        if isinstance(st.session_state.controlled_vars, list):
            controlled_vars_text = "\n".join(st.session_state.controlled_vars)
        else:
            controlled_vars_text = st.session_state.controlled_vars
            
        edited_controlled_vars = st.text_area("Controlled Variables (one per line)", 
                                         value=controlled_vars_text,
                                         height=150,
                                         help="List the variables you will keep constant")
        
        # Convert back to list
        st.session_state.controlled_vars = [var.strip() for var in edited_controlled_vars.split("\n") if var.strip()]

# Step 4: Materials and Equipment
if st.session_state.experiment_type:
    st.subheader("Step 4: Materials and Equipment")
    
    # Convert materials list to string for editing
    if isinstance(st.session_state.materials, list):
        materials_text = "\n".join(st.session_state.materials)
    else:
        materials_text = st.session_state.materials
        
    edited_materials = st.text_area("List all materials and equipment needed (one per line)", 
                                   value=materials_text,
                                   height=150)
    
    # Convert back to list
    st.session_state.materials = [item.strip() for item in edited_materials.split("\n") if item.strip()]

# Step 5: Methodology
if st.session_state.experiment_type:
    st.subheader("Step 5: Experimental Methodology")
    st.markdown("*Describe the step-by-step procedure for your experiment*")
    
    st.session_state.methodology = st.text_area("Experimental Procedure", 
                                  value=st.session_state.methodology,
                                  height=200,
                                  help="Provide detailed step-by-step instructions that would allow someone else to replicate your experiment")

# Step 6: Safety Considerations
if st.session_state.experiment_type:
    st.subheader("Step 6: Safety Considerations")
    
    st.session_state.safety_considerations = st.text_area("Safety Considerations", 
                                            value=st.session_state.safety_considerations,
                                            height=150,
                                            help="List all safety hazards and precautions")

# Save experiment plan
if st.session_state.experiment_type:
    st.subheader("Save Your Experiment Plan")
    
    if st.button("Save Experiment Plan"):
        # In a real application, this would save to a database or file
        st.success("Experiment plan saved successfully! Continue to Hypothesis Testing.")
        
        # Display a summary of the experiment plan
        st.subheader("Experiment Plan Summary")
        
        summary_md = f"""
        **Topic:** {st.session_state.experiment_topic}  
        **Experiment Type:** {st.session_state.experiment_type}  
        
        **Independent Variable:** {st.session_state.independent_var}  
        **Dependent Variable:** {st.session_state.dependent_var}  
        
        **Controlled Variables:**  
        """
        
        for var in st.session_state.controlled_vars:
            summary_md += f"- {var}  \n"
            
        summary_md += "\n**Materials and Equipment:**  \n"
        for item in st.session_state.materials:
            summary_md += f"- {item}  \n"
        
        st.markdown(summary_md)
