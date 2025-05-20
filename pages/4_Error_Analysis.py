import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import math
from sympy import symbols, diff, sympify, parsing

# Set page title
st.title("Error Analysis")
st.markdown("### Calculate uncertainties and analyze errors in your experiment")

# Initialize session state variables if they don't exist
if 'random_errors' not in st.session_state:
    st.session_state.random_errors = []
if 'systematic_errors' not in st.session_state:
    st.session_state.systematic_errors = []
if 'error_formula' not in st.session_state:
    st.session_state.error_formula = ""
if 'error_variables' not in st.session_state:
    st.session_state.error_variables = {}
if 'propagated_error' not in st.session_state:
    st.session_state.propagated_error = None
if 'percentage_error' not in st.session_state:
    st.session_state.percentage_error = None

# Step 1: Identify Sources of Error
st.subheader("Step 1: Identify Sources of Error")

st.markdown("""
In any chemistry experiment, there are two main types of errors:

1. **Random Errors**: Also known as precision errors, these cause measurements to fluctuate around the true value due to unpredictable variations.
2. **Systematic Errors**: Also known as accuracy errors, these cause measurements to consistently deviate from the true value in a particular direction.
""")

# Random Errors Section
st.markdown("#### Random Errors")
st.markdown("List all random errors that might have affected your experiment:")

# Convert random errors list to string for editing
if isinstance(st.session_state.random_errors, list):
    random_errors_text = "\n".join(st.session_state.random_errors)
else:
    random_errors_text = st.session_state.random_errors

edited_random_errors = st.text_area("Random Errors (one per line)", 
                                   value=random_errors_text,
                                   height=150,
                                   help="Examples: reading scales, temperature fluctuations, timing errors")

# Convert back to list
st.session_state.random_errors = [err.strip() for err in edited_random_errors.split("\n") if err.strip()]

# Systematic Errors Section
st.markdown("#### Systematic Errors")
st.markdown("List all systematic errors that might have affected your experiment:")

# Convert systematic errors list to string for editing
if isinstance(st.session_state.systematic_errors, list):
    systematic_errors_text = "\n".join(st.session_state.systematic_errors)
else:
    systematic_errors_text = st.session_state.systematic_errors

edited_systematic_errors = st.text_area("Systematic Errors (one per line)", 
                                       value=systematic_errors_text,
                                       height=150,
                                       help="Examples: calibration errors, impure reagents, consistent measurement bias")

# Convert back to list
st.session_state.systematic_errors = [err.strip() for err in edited_systematic_errors.split("\n") if err.strip()]

# Step 2: Absolute and Percentage Uncertainty Calculations
st.subheader("Step 2: Absolute and Percentage Uncertainty Calculations")

st.markdown("""
#### Absolute Uncertainty

For repeated measurements, you can calculate absolute uncertainty in several ways:
1. **Range Method**: (max value - min value) ÷ 2
2. **Standard Deviation**: s = √[Σ(x - x̄)² ÷ (n-1)]
3. **Instrument Precision**: Half the smallest scale division
""")

# Data input for uncertainty calculation
if 'data_df' in st.session_state and not st.session_state.data_df.empty:
    st.markdown("#### Calculate from Experimental Data")
    
    # Select column for uncertainty calculation
    numeric_cols = st.session_state.data_df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        selected_col = st.selectbox("Select data column for uncertainty calculation", options=numeric_cols)
        
        # Calculate statistics
        data_values = st.session_state.data_df[selected_col].values
        mean_value = np.mean(data_values)
        range_value = np.max(data_values) - np.min(data_values)
        std_dev = np.std(data_values, ddof=1)  # ddof=1 for sample standard deviation
        
        # Display calculated statistics
        st.markdown(f"**Mean Value:** {mean_value:.6g}")
        st.markdown(f"**Range:** {range_value:.6g}")
        st.markdown(f"**Standard Deviation:** {std_dev:.6g}")
        
        # Uncertainty calculation method
        uncertainty_method = st.radio("Select uncertainty calculation method", 
                                    ["Range Method", "Standard Deviation", "Standard Error of the Mean"])
        
        if uncertainty_method == "Range Method":
            absolute_uncertainty = range_value / 2
            uncertainty_explanation = "Calculated as (max value - min value) ÷ 2"
        elif uncertainty_method == "Standard Deviation":
            absolute_uncertainty = std_dev
            uncertainty_explanation = "Standard deviation of the data points"
        else:  # Standard Error of the Mean
            absolute_uncertainty = std_dev / math.sqrt(len(data_values))
            uncertainty_explanation = "Standard deviation ÷ √n (where n is the number of data points)"
        
        # Display results
        st.markdown(f"**Absolute Uncertainty:** {absolute_uncertainty:.6g} ({uncertainty_explanation})")
        
        # Calculate percentage uncertainty
        percentage_uncertainty = (absolute_uncertainty / abs(mean_value)) * 100
        st.markdown(f"**Percentage Uncertainty:** {percentage_uncertainty:.4g}%")
        
        # Store the results
        st.session_state.calculated_abs_uncertainty = absolute_uncertainty
        st.session_state.calculated_percentage_uncertainty = percentage_uncertainty
        
        # Visualization of uncertainty
        st.markdown("#### Visualization of Uncertainty")
        
        # Create a visualization of data with error bars
        error_array = [absolute_uncertainty] * len(data_values)
        
        fig = px.scatter(
            x=list(range(len(data_values))),
            y=data_values,
            error_y=dict(type='data', array=error_array, visible=True),
            labels={'x': 'Measurement Number', 'y': selected_col}
        )
        
        # Add a line for the mean
        fig.add_hline(y=mean_value, line_dash="dash", line_color="red", annotation_text="Mean")
        
        # Add lines for mean ± uncertainty
        fig.add_hline(y=mean_value + absolute_uncertainty, line_dash="dot", line_color="green", 
                     annotation_text="Mean + Uncertainty")
        fig.add_hline(y=mean_value - absolute_uncertainty, line_dash="dot", line_color="green", 
                     annotation_text="Mean - Uncertainty")
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No numeric data available for uncertainty calculation.")
else:
    st.info("No experimental data available. Please input data in the Data Analysis section first.")

# Manual uncertainty calculation
st.markdown("### Manual Uncertainty Calculations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Input Individual Measurements")
    manual_measurements = st.text_area("Enter measurements (one per line)", height=150)
    
    if manual_measurements:
        try:
            # Parse measurements
            measurements = [float(x.strip()) for x in manual_measurements.split('\n') if x.strip()]
            
            if measurements:
                # Calculate statistics
                mean_val = np.mean(measurements)
                range_val = np.max(measurements) - np.min(measurements)
                std_dev_val = np.std(measurements, ddof=1)
                std_err_val = std_dev_val / math.sqrt(len(measurements))
                
                # Display results
                st.markdown(f"**Mean:** {mean_val:.6g}")
                st.markdown(f"**Range:** {range_val:.6g}")
                st.markdown(f"**Standard Deviation:** {std_dev_val:.6g}")
                st.markdown(f"**Standard Error:** {std_err_val:.6g}")
                
                # Absolute uncertainty methods
                st.markdown("**Absolute Uncertainty:**")
                st.markdown(f"- Range Method: ±{range_val/2:.6g}")
                st.markdown(f"- Standard Deviation: ±{std_dev_val:.6g}")
                st.markdown(f"- Standard Error: ±{std_err_val:.6g}")
                
                # Percentage uncertainty
                st.markdown("**Percentage Uncertainty:**")
                st.markdown(f"- Range Method: {(range_val/2/abs(mean_val))*100:.4g}%")
                st.markdown(f"- Standard Deviation: {(std_dev_val/abs(mean_val))*100:.4g}%")
                st.markdown(f"- Standard Error: {(std_err_val/abs(mean_val))*100:.4g}%")
        except Exception as e:
            st.error(f"Error calculating uncertainty: {e}")

with col2:
    st.markdown("#### Instrument Uncertainty")
    instrument_value = st.number_input("Measured Value", value=0.0, key="manual_instrument_value")
    
    # Equipment Uncertainty Database
    st.markdown("##### Common Lab Equipment Uncertainties")
    # This dictionary stores typical absolute uncertainties for common lab equipment.
    # Values are examples and may vary based on specific equipment class and calibration.
    # Units are typically in mL for volumetric glassware and g for balances, unless otherwise specified in the name.
    equipment_uncertainties = {
        "Select Equipment...": 0.0,  # Default placeholder
        "Volumetric Flask (25mL Class A)": 0.03, # mL
        "Volumetric Flask (50mL Class A)": 0.05,
        "Volumetric Flask (100mL Class A)": 0.08,
        "Volumetric Flask (250mL Class A)": 0.12,
        "Volumetric Flask (500mL Class A)": 0.20,
        "Pipette (1mL Class A)": 0.006,
        "Pipette (5mL Class A)": 0.01,
        "Pipette (10mL Class A)": 0.02,
        "Pipette (25mL Class A)": 0.03,
        "Pipette (50mL Class A)": 0.05,
        "Burette (10mL Class A)": 0.02,
        "Burette (25mL Class A)": 0.03,
        "Burette (50mL Class A)": 0.05,
        "Analytical Balance (± g)": 0.0002, # typically ±0.0001g or ±0.0002g
        "Top-loading Balance (± g)": 0.01, # can vary widely
        "Digital Thermometer (± °C)": 0.1,
        "Liquid-in-glass Thermometer (± °C)": 0.2, # depends on calibration and range
        "Graduated Cylinder (10mL)": 0.1,
        "Graduated Cylinder (25mL)": 0.2,
        "Graduated Cylinder (50mL)": 0.5,
        "Graduated Cylinder (100mL)": 1.0,
    }
    
    selected_equipment = st.selectbox("Select from common equipment", 
                                      options=list(equipment_uncertainties.keys()), 
                                      key="selected_equipment")
    
    
    # Input field for the user to manually enter or adjust the absolute uncertainty of their instrument.
    # This value can be populated by selecting from the `equipment_uncertainties` list
    # or entered directly by the user.
    st.session_state.instrument_precision = st.number_input(
        "Absolute Uncertainty of Instrument (e.g., ±0.05 mL or ±0.0002 g)", 
        value=float(st.session_state.get('instrument_precision', 0.1)), # Retain last value or default
        min_value=0.00000001, # Allow for very precise instruments (e.g., microbalances)
        format="%.8f", # Display more decimal places for precision
        key="instrument_precision_input",
        help="Enter the known absolute uncertainty of your measuring instrument. This is often provided by the manufacturer or calibration certificate."
    )

    if selected_equipment != "Select Equipment...":
        # Display the typical uncertainty for the selected equipment.
        st.write(f"Typical uncertainty for {selected_equipment}: ±{equipment_uncertainties[selected_equipment]}")
        # Button to automatically populate the 'Absolute Uncertainty of Instrument' field.
        if st.button("Use this uncertainty", key="use_equipment_uncertainty"):
            st.session_state.instrument_precision = equipment_uncertainties[selected_equipment]
            # st.experimental_rerun() is used to immediately update the number_input field above
            # with the value from the selected equipment.
            st.experimental_rerun()
            
    # The `absolute_uncertainty_instr` is now directly taken from `st.session_state.instrument_precision`.
    # Previously, it might have been calculated (e.g., half of smallest division).
    # Now, it's assumed the user provides the direct absolute uncertainty.
    absolute_uncertainty_instr = st.session_state.instrument_precision
    
    if instrument_value != 0:
        percentage_uncertainty_instr = (absolute_uncertainty_instr / abs(instrument_value)) * 100
        
        st.markdown(f"**Absolute Uncertainty:** ±{absolute_uncertainty_instr:.6g}")
        st.markdown(f"**Percentage Uncertainty:** {percentage_uncertainty_instr:.4g}%")
    else:
        st.warning("Cannot calculate percentage uncertainty when measured value is zero.")

# Step 3: Error Propagation
st.subheader("Step 3: Error Propagation")

st.markdown("""
When calculations involve multiple measurements, each with their own uncertainty, the uncertainty propagates through the calculation.

#### Rules for Error Propagation:

1. **Addition and Subtraction**: 
   - Absolute uncertainties add: Δ(A±B) = √(ΔA² + ΔB²)

2. **Multiplication and Division**:
   - Percentage uncertainties add: Δ(A×B)/|A×B| = √[(ΔA/|A|)² + (ΔB/|B|)²]

3. **Powers**:
   - For y = x^n: Δy/|y| = |n| × (Δx/|x|)

4. **Complex Functions**:
   - Using partial derivatives: Δf = √[(∂f/∂x₁ × Δx₁)² + (∂f/∂x₂ × Δx₂)² + ...]
""")

st.markdown("#### Error Propagation Calculator")

# Choose propagation method
propagation_method = st.radio("Select error propagation method", 
                            ["Basic Operations", "Complex Function"])

if propagation_method == "Basic Operations":
    # Simple calculator for basic operations
    operation = st.selectbox("Select operation", ["Addition (A+B)", "Subtraction (A-B)", 
                                               "Multiplication (A×B)", "Division (A÷B)", "Power (A^n)"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        value_a = st.number_input("Value A", value=0.0)
        uncertainty_a = st.number_input("Uncertainty in A (ΔA)", value=0.0, min_value=0.0)
    
    with col2:
        if operation != "Power (A^n)":
            value_b = st.number_input("Value B", value=0.0)
            uncertainty_b = st.number_input("Uncertainty in B (ΔB)", value=0.0, min_value=0.0)
        else:
            power_n = st.number_input("Power (n)", value=2.0)
    
    # Calculate result and propagated error
    if st.button("Calculate Propagated Error"):
        if operation == "Addition (A+B)":
            result = value_a + value_b
            propagated_error = math.sqrt(uncertainty_a**2 + uncertainty_b**2)
            formula_explanation = "Δ(A+B) = √(ΔA² + ΔB²)"
        
        elif operation == "Subtraction (A-B)":
            result = value_a - value_b
            propagated_error = math.sqrt(uncertainty_a**2 + uncertainty_b**2)
            formula_explanation = "Δ(A-B) = √(ΔA² + ΔB²)"
        
        elif operation == "Multiplication (A×B)":
            result = value_a * value_b
            
            # Using percentage uncertainties for multiplication
            if value_a != 0 and value_b != 0:
                rel_error_a = uncertainty_a / abs(value_a)
                rel_error_b = uncertainty_b / abs(value_b)
                rel_error_result = math.sqrt(rel_error_a**2 + rel_error_b**2)
                propagated_error = abs(result) * rel_error_result
                formula_explanation = "Δ(A×B) = |A×B| × √[(ΔA/|A|)² + (ΔB/|B|)²]"
            else:
                propagated_error = None
                formula_explanation = "Cannot calculate when values are zero"
        
        elif operation == "Division (A÷B)":
            if value_b != 0:
                result = value_a / value_b
                
                # Using percentage uncertainties for division
                if value_a != 0 and value_b != 0:
                    rel_error_a = uncertainty_a / abs(value_a)
                    rel_error_b = uncertainty_b / abs(value_b)
                    rel_error_result = math.sqrt(rel_error_a**2 + rel_error_b**2)
                    propagated_error = abs(result) * rel_error_result
                    formula_explanation = "Δ(A÷B) = |A÷B| × √[(ΔA/|A|)² + (ΔB/|B|)²]"
                else:
                    propagated_error = None
                    formula_explanation = "Cannot calculate when values are zero"
            else:
                result = None
                propagated_error = None
                formula_explanation = "Division by zero"
        
        elif operation == "Power (A^n)":
            result = value_a ** power_n
            
            # For power function
            if value_a != 0:
                rel_error_a = uncertainty_a / abs(value_a)
                rel_error_result = abs(power_n) * rel_error_a
                propagated_error = abs(result) * rel_error_result
                formula_explanation = f"Δ(A^n) = |A^n| × |n| × (ΔA/|A|)"
            else:
                propagated_error = None
                formula_explanation = "Cannot calculate when value is zero"
        
        # Display results
        if result is not None and propagated_error is not None:
            st.markdown(f"**Result:** {result:.6g} ± {propagated_error:.6g}")
            
            # Calculate percentage error
            if result != 0:
                percentage_error = (propagated_error / abs(result)) * 100
                st.markdown(f"**Percentage Error:** {percentage_error:.4g}%")
            
            st.markdown(f"**Formula Used:** {formula_explanation}")
        else:
            st.error("Unable to calculate result or error. Check your inputs.")

else:  # Complex Function
    st.markdown("""
    For complex functions, enter a mathematical expression and the variables with their uncertainties.
    Example: For calculating density (d = m/V), enter the expression as "m/V".
    """)
    
    # Function expression input
    expression = st.text_input("Enter mathematical expression", value=st.session_state.error_formula or "x+y")
    
    # Store the expression
    st.session_state.error_formula = expression
    
    # Try to parse the expression to identify variables
    try:
        expr = sympify(expression)
        variables = sorted(list(expr.free_symbols), key=lambda x: x.name)
        
        # Create input fields for each variable identified by SymPy from the expression.
        st.markdown("#### Enter values, uncertainties, and units for each variable:")
        
        # Initialize or update the session state dictionary for error variables.
        # This ensures that if variables are added or removed from the expression,
        # the dictionary structure is updated accordingly.
        if not st.session_state.error_variables: # Initialize if empty
            st.session_state.error_variables = {var.name: {"value": 0.0, "uncertainty": 0.0, "unit": ""} for var in variables}
        
        # Ensure all current variables from the expression exist in the session state dictionary.
        # This handles cases where the expression changes and new variables are introduced.
        for var_symbol in variables:
            var_name = var_symbol.name
            if var_name not in st.session_state.error_variables:
                st.session_state.error_variables[var_name] = {"value": 0.0, "uncertainty": 0.0, "unit": ""}
        
        # Dynamically create columns for a cleaner layout of variable inputs.
        # The number of columns matches the number of identified variables.
        cols = st.columns(len(variables))
        
        # Populate input fields for each variable (value, uncertainty, unit).
        for i, var_symbol in enumerate(variables):
            var_name = var_symbol.name
            with cols[i]:
                st.markdown(f"**Variable: {var_name}**")
                # Input for the measured value of the variable.
                value = st.number_input(f"Value for {var_name}",
                                       value=float(st.session_state.error_variables[var_name].get("value", 0.0)),
                                       key=f"value_{var_name}",
                                       help=f"Enter the measured value for variable '{var_name}'.")
                
                # Input for the absolute uncertainty of the variable.
                uncertainty = st.number_input(f"Uncertainty in {var_name} (Δ{var_name})",
                                           value=float(st.session_state.error_variables[var_name].get("uncertainty", 0.0)),
                                           min_value=0.0, # Uncertainty cannot be negative.
                                           format="%.6g", # General format for displaying uncertainty.
                                           key=f"uncertainty_{var_name}",
                                           help=f"Enter the absolute uncertainty (e.g., ±0.01) for variable '{var_name}'.")
                
                # Input for the unit of the variable.
                unit = st.text_input(f"Unit for {var_name}",
                                     value=str(st.session_state.error_variables[var_name].get("unit", "")),
                                     key=f"unit_{var_name}",
                                     help=f"Enter the unit for variable '{var_name}' (e.g., g, mL, mol/L).")
                
                # Store the entered values back into the session state dictionary for this variable.
                st.session_state.error_variables[var_name]["value"] = value
                st.session_state.error_variables[var_name]["uncertainty"] = uncertainty
                st.session_state.error_variables[var_name]["unit"] = unit
        
        # Button to trigger the error propagation calculation.
        if st.button("Calculate Propagated Error for Complex Function", key="calc_complex_error_button") and variables:
            try:
                # Prepare a dictionary for substituting variable values into the SymPy expression.
                subs_dict_val = {var.name: st.session_state.error_variables[var.name]["value"] for var in variables}
                # Calculate the result of the function using the provided variable values.
                result = expr.subs(subs_dict_val)
                
                # Initialize sum of squared errors for propagation formula.
                error_squared_sum = 0.0
                
                # Display a summary of the variables, their values, uncertainties, and units.
                st.markdown("#### Summary of Variables Used in Calculation:")
                for var_symbol in variables:
                    var_name = var_symbol.name
                    val = st.session_state.error_variables[var_name]['value']
                    unc = st.session_state.error_variables[var_name]['uncertainty']
                    unit_str = st.session_state.error_variables[var_name]['unit']
                    st.markdown(f"- **{var_name}**: {val} ± {unc} {unit_str}")

                # Calculate error propagation using partial derivatives.
                # The formula is: Δf = sqrt(Σ ( (∂f/∂xi * Δxi)^2 ) )
                for var_symbol in variables:
                    var_name = var_symbol.name
                    # Calculate the partial derivative of the expression with respect to the current variable.
                    partial_deriv_expr = diff(expr, var_symbol)
                    # Substitute the measured values of variables into the partial derivative expression.
                    partial_deriv_value = partial_deriv_expr.subs(subs_dict_val)
                    
                    # Get the uncertainty for the current variable.
                    var_uncertainty = st.session_state.error_variables[var_name]["uncertainty"]
                    
                    # Add the squared term (∂f/∂xi * Δxi)^2 to the sum.
                    # Ensure conversion to float for mathematical operations.
                    error_squared_sum += (float(partial_deriv_value) * var_uncertainty) ** 2
                
                # The propagated error is the square root of the sum of squared errors.
                propagated_error = math.sqrt(error_squared_sum) 
                
                # Store the calculated propagated error in session state.
                st.session_state.propagated_error = propagated_error
                
                # Input for the overall unit of the final result.
                overall_unit = st.text_input("Overall Unit for Result", 
                                             value=st.session_state.get("overall_unit", ""),
                                             key="overall_unit_input",
                                             help="Enter the unit for the final calculated result (e.g., g/mL).")
                st.session_state.overall_unit = overall_unit # Store in session state.

                # Calculate percentage error if the result is not zero.
                if result != 0:
                    percentage_error_val = (propagated_error / abs(float(result))) * 100
                    st.session_state.percentage_error = percentage_error_val # Store in session state.
                else:
                    percentage_error_val = None
                    st.session_state.percentage_error = None # Clear if result is zero.
                
                # Display the final results: function, result with propagated error, and percentage error.
                st.markdown(f"**Function Evaluated:** `{expression}`")
                st.success(f"**Calculated Result:** {float(result):.6g} ± {propagated_error:.6g} {overall_unit}")
                
                if percentage_error_val is not None:
                    st.markdown(f"**Percentage Error in Result:** {percentage_error_val:.4g}%")
                
                # Display the formula used
                st.markdown("**Formula Used:**")
                st.latex(r"\Delta f = \sqrt{\sum_i \left(\frac{\partial f}{\partial x_i} \cdot \Delta x_i\right)^2}")
                
                # Display each partial derivative term
                st.markdown("**Partial Derivatives:**")
                
                for var in variables:
                    partial_deriv = diff(expr, var)
                    st.markdown(f"∂f/∂{var.name} = {partial_deriv}")
                
            except Exception as e:
                st.error(f"Error in calculation: {e}")
    
    except Exception as e:
        st.error(f"Error parsing expression: {e}. Please enter a valid mathematical expression.")

# Step 4: Error Minimization Strategies
st.subheader("Step 4: Error Minimization Strategies")

st.markdown("""
Based on your identified sources of error, consider strategies to minimize them in future experiments.
""")

# Random Errors Minimization
if st.session_state.random_errors:
    st.markdown("#### Strategies to Minimize Random Errors")
    
    for i, error in enumerate(st.session_state.random_errors):
        strategy = st.text_input(f"Strategy to minimize: {error}", key=f"random_strategy_{i}")
        
        # Default suggestions if empty
        if not strategy:
            if "reading" in error.lower() or "measurement" in error.lower():
                st.info("Suggestion: Take multiple readings and calculate the mean. Use more precise measuring instruments.")
            elif "temperature" in error.lower():
                st.info("Suggestion: Use a water bath or temperature-controlled environment. Monitor temperature throughout the experiment.")
            elif "timing" in error.lower():
                st.info("Suggestion: Use an automated timer or stopwatch with better precision. Practice consistent timing technique.")
            else:
                st.info("Suggestion: Take multiple measurements and use statistical methods to reduce random error.")

# Systematic Errors Minimization
if st.session_state.systematic_errors:
    st.markdown("#### Strategies to Minimize Systematic Errors")
    
    for i, error in enumerate(st.session_state.systematic_errors):
        strategy = st.text_input(f"Strategy to minimize: {error}", key=f"systematic_strategy_{i}")
        
        # Default suggestions if empty
        if not strategy:
            if "calibration" in error.lower():
                st.info("Suggestion: Calibrate instruments before use. Use standard solutions to check accuracy.")
            elif "impure" in error.lower() or "reagent" in error.lower():
                st.info("Suggestion: Use higher grade reagents. Verify reagent purity before use.")
            elif "parallax" in error.lower():
                st.info("Suggestion: Ensure eye level is perpendicular to the scale when taking readings.")
            else:
                st.info("Suggestion: Use control experiments to identify and quantify systematic errors. Apply correction factors when appropriate.")

# Summary of Error Analysis
st.subheader("Summary of Error Analysis")

summary_text = ""

# Add calculation results to summary if available
if 'calculated_abs_uncertainty' in st.session_state and 'calculated_percentage_uncertainty' in st.session_state:
    if st.session_state.calculated_abs_uncertainty is not None:
        summary_text += f"**Calculated Absolute Uncertainty:** ±{st.session_state.calculated_abs_uncertainty:.6g}\n\n"
        summary_text += f"**Calculated Percentage Uncertainty:** {st.session_state.calculated_percentage_uncertainty:.4g}%\n\n"

# Add propagated error to summary if available
if 'propagated_error' in st.session_state and 'percentage_error' in st.session_state:
    if st.session_state.propagated_error is not None:
        summary_text += f"**Propagated Error:** ±{st.session_state.propagated_error:.6g}\n\n"
        
        if st.session_state.percentage_error is not None:
            summary_text += f"**Propagated Percentage Error:** {st.session_state.percentage_error:.4g}%\n\n"

# Add identified errors to summary
if st.session_state.random_errors:
    summary_text += "**Random Errors Identified:**\n"
    for error in st.session_state.random_errors:
        summary_text += f"- {error}\n"
    summary_text += "\n"

if st.session_state.systematic_errors:
    summary_text += "**Systematic Errors Identified:**\n"
    for error in st.session_state.systematic_errors:
        summary_text += f"- {error}\n"
    summary_text += "\n"

if summary_text:
    st.markdown(summary_text)
    
    if st.button("Save Error Analysis"):
        # Most relevant data on this page is already stored in st.session_state
        # due to direct widget binding or immediate processing after widget interaction.
        # - Random/Systematic errors (lists): Updated on text_area change.
        # - Calculated uncertainties: Updated when calculation method/column changes.
        # - Instrument uncertainty inputs: Bound to session_state via keys.
        # - Error propagation inputs for complex functions: Bound to session_state via keys.
        # - Error propagation results: Set in session_state when "Calculate Propagated Error" is clicked.
        # - Error minimization strategies: Bound to session_state via dynamic keys.
        #
        # This button primarily serves as a user confirmation point. The summary displayed
        # by this button (if it were to generate one) would reflect the current st.session_state.
        # The existing summary_text variable is built *before* this button is defined.
        # For consistency, we can consider the act of clicking "Save" as confirming
        # that the `summary_text` displayed above is what they intend to "save" implicitly.
        
        # If we wanted to store the generated summary_text itself into session_state:
        # st.session_state.saved_error_analysis_summary = summary_text
        
        st.success("Error analysis saved successfully! Continue to Report Generation.")
else:
    st.info("Complete the error analysis steps above to generate a summary.")
