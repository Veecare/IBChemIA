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
- **Chemistry Tools**: Access helpful utilities like an equation balancer
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

st.markdown("---")

# --- Manage Progress ---
import json
import io

# Define keys that are expected to be DataFrames
DATAFRAME_KEYS = ['data_df'] 

# Define keys that should be skipped during serialization/deserialization
# These might include keys for internal UI state, widget values that are not data, etc.
# For now, focusing on Streamlit internal-like keys and keys used for momentary widget states.
KEYS_TO_SKIP = [
    'FormSubmitter:Report Information-Save Experiment Plan', # Example of Streamlit internal key
    'FormSubmitter:Hypothesis Formulation-Save Hypothesis',
    'FormSubmitter:Data Analysis-Update Data Table', # etc.
    # Add keys for temporary widget states if they are not meant to be persisted long-term
    # e.g. 'unbalanced_eq_input_key', 'balance_button' if they are just momentary UI states.
    # However, for this app, most widget keys are directly tied to persistent session_state values.
    # The main concern is filtering out Streamlit's own internal keys if any get mixed in.
    # The main concern is filtering out Streamlit's own internal keys if any get mixed in.
]
# Import date and datetime explicitly for type checking
from datetime import date, datetime

def preprocess_session_state_for_json(session_state_dict):
    """
    Prepares the Streamlit session state dictionary for JSON serialization.

    This function iterates through the session state, converts complex objects
    like Pandas DataFrames and datetime objects into JSON-serializable formats,
    and filters out internal or specified keys.

    Args:
        session_state_dict (dict): The dictionary obtained from 
                                   `st.session_state.to_dict()`.

    Returns:
        dict: A new dictionary where complex objects are serialized and
              unwanted keys are removed.
    """
    serializable_state = {}
    for key, value in session_state_dict.items():
        # Skip internal Streamlit keys (often starting with '_') or explicitly defined KEYS_TO_SKIP
        if key.startswith('_') or key.startswith('FormSubmitter:') or key in KEYS_TO_SKIP:
            continue
        
        if isinstance(value, pd.DataFrame):
            # Convert DataFrame to a list of records dictionary for JSON compatibility
            serializable_state[key] = value.to_dict(orient='records')
            # Add a metadata key to flag this entry as a DataFrame for deserialization
            serializable_state[f"{key}__is_dataframe"] = True 
        elif isinstance(value, (datetime, date)): # Check if it's a datetime or date object
             # Convert datetime/date objects to ISO format string
             serializable_state[key] = value.isoformat()
             # Add a metadata key to flag this entry for date parsing during deserialization
             serializable_state[f"{key}__is_date"] = True
        elif isinstance(value, np.ndarray):
            # Convert NumPy arrays to Python lists
            serializable_state[key] = value.tolist()
        elif isinstance(value, set):
            # Convert sets to Python lists
            serializable_state[key] = list(value)
        else:
            # For other data types, attempt to include them if they are JSON serializable
            try:
                # Test serializability by attempting to dump the individual value.
                # This is a basic check; complex nested objects might still cause issues
                # if not handled explicitly.
                json.dumps({key: value}) 
                serializable_state[key] = value
            except (TypeError, OverflowError):
                # If a type is not directly serializable, warn the user and skip it.
                st.warning(f"Skipping non-serializable session state key: '{key}' of type {type(value)}")
                continue
    return serializable_state

def restore_session_state_from_dict(loaded_data_dict):
    """
    Restores Python objects from a dictionary that was previously prepared
    for JSON serialization (e.g., by `preprocess_session_state_for_json`).

    This function converts dictionary representations of DataFrames back into
    Pandas DataFrames and ISO date strings back into datetime objects.

    Args:
        loaded_data_dict (dict): The dictionary loaded from the JSON progress file.

    Returns:
        dict: A new dictionary with objects like DataFrames and dates restored
              to their original Python types.
    """
    restored_state = {}
    for key, value in loaded_data_dict.items():
        # Skip metadata keys used for type identification during deserialization
        if key.endswith('__is_dataframe') or key.endswith('__is_date'):
            continue

        # Check if the current key has associated DataFrame metadata
        if loaded_data_dict.get(f"{key}__is_dataframe"):
            # Convert the list of records back into a Pandas DataFrame
            restored_state[key] = pd.DataFrame.from_records(value)
        # Check if the current key has associated date metadata
        elif loaded_data_dict.get(f"{key}__is_date"):
            # Convert the ISO format string back to a datetime object
            restored_state[key] = datetime.fromisoformat(value)
        else:
            # For all other keys, assign the value directly
            restored_state[key] = value
    return restored_state


st.sidebar.title("Manage Progress")
# Section for downloading and uploading session state

# Download Progress
try:
    # Create a dictionary from st.session_state.to_dict() for processing
    current_session_state_dict = st.session_state.to_dict()
    json_str = json.dumps(preprocess_session_state_for_json(current_session_state_dict), indent=2)
    
    st.sidebar.download_button(
        label="Download Full Progress",
        data=json_str,
        file_name="ia_lab_tool_progress.json",
        mime="application/json",
    )
except Exception as e:
    st.sidebar.error(f"Error preparing download: {e}")
    st.sidebar.exception(e) # For debugging

# Upload Progress
uploaded_file = st.sidebar.file_uploader("Upload Progress File", type=["json"])

if uploaded_file is not None:
    try:
        loaded_data = json.load(io.TextIOWrapper(uploaded_file, encoding='utf-8'))
        restored_data = restore_session_state_from_dict(loaded_data)
        
        st.session_state.clear() # Clear existing state
        for key, value in restored_data.items():
            st.session_state[key] = value
            
        st.success("Progress loaded successfully! The application will now refresh.")
        st.experimental_rerun() # Rerun to reflect loaded state across all pages
        
    except json.JSONDecodeError:
        st.sidebar.error("Error: Invalid JSON file. Please upload a valid progress file.")
    except Exception as e:
        st.sidebar.error(f"Error loading progress: {e}")
        st.sidebar.exception(e) # For debugging
