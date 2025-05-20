import streamlit as st
from utils.chemistry_tools import balance_chemical_equation

# Set page title and icon
st.set_page_config(page_title="Chemistry Tools", page_icon="🧪")

st.title("Chemistry Tools 🧪")

st.markdown("---")

# Chemical Equation Balancer
st.subheader("Chemical Equation Balancer")
st.markdown("""
Enter an unbalanced chemical equation and click "Balance Equation". 
Use standard chemical formulas. Reactants and products should be separated by '->'. 
Individual species on each side should be separated by '+'. 
Example: `H2 + O2 -> H2O`
""")

# Initialize session state for equation input if it doesn't exist
if 'unbalanced_eq_input' not in st.session_state:
    st.session_state.unbalanced_eq_input = "H2 + O2 -> H2O" # Default example

# User input for the unbalanced equation
unbalanced_eq = st.text_input(
    "Enter Unbalanced Equation:",
    value=st.session_state.unbalanced_eq_input,
    key="unbalanced_eq_input_key" # Give a unique key to allow updating session state
)

# Update session state when text_input changes
st.session_state.unbalanced_eq_input = unbalanced_eq 

if st.button("Balance Equation", key="balance_button"):
    if st.session_state.unbalanced_eq_input:
        # Call the balancing function from the utils module
        balanced_result = balance_chemical_equation(st.session_state.unbalanced_eq_input)
        
        # Display the result
        if balanced_result and "Error:" not in balanced_result:
            st.success(f"**Balanced Equation:** {balanced_result}")
            # Optionally, provide a more structured output if needed
            # st.markdown(f"```\n{balanced_result}\n```") 
        elif "Error:" in balanced_result:
            st.error(balanced_result)
        else: # Should not happen if balance_chemical_equation always returns string
            st.warning("Could not balance the equation or an unknown issue occurred.")
            
    else:
        st.warning("Please enter a chemical equation to balance.")

st.markdown("---")
st.markdown("More chemistry tools may be added here in the future!")

# You can add explanations or tips about equation balancing if desired.
with st.expander("Tips for Entering Equations"):
    st.markdown("""
    - Ensure correct capitalization for element symbols (e.g., `H`, `He`, `Cl` not `h`, `he`, `cl`).
    - Use parentheses for polyatomic ions, e.g., `Fe(NO3)3`.
    - Ensure there's a clear separation between reactants and products using `->`.
    - Separate multiple reactants or products using `+` with spaces around it for clarity, though the balancer attempts to handle various spacings.
    - Example: `KMnO4 + HCl -> KCl + MnCl2 + H2O + Cl2`
    - The balancer currently does not support states like (aq), (s), (g), (l). Please omit them.
    """)
