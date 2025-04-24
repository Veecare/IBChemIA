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
    st.markdown("#### Instrument Precision Uncertainty")
    instrument_value = st.number_input("Measured Value", value=0.0)
    instrument_precision = st.number_input("Instrument Precision (smallest scale division)", value=0.1, min_value=0.000001, format="%.6f")
    
    # Calculate uncertainty
    absolute_uncertainty_instr = instrument_precision / 2
    
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
        
        # Create input fields for each variable
        st.markdown("#### Enter values and uncertainties for each variable:")
        
        # Initialize/update variables dictionary if needed
        if not st.session_state.error_variables:
            st.session_state.error_variables = {var.name: {"value": 0.0, "uncertainty": 0.0} for var in variables}
        
        # Make sure all variables from the expression are in the dictionary
        for var in variables:
            if var.name not in st.session_state.error_variables:
                st.session_state.error_variables[var.name] = {"value": 0.0, "uncertainty": 0.0}
        
        # Create columns for inputs
        cols = st.columns(len(variables))
        
        # Populate inputs for each variable
        for i, var in enumerate(variables):
            with cols[i]:
                st.markdown(f"**Variable: {var.name}**")
                value = st.number_input(f"Value for {var.name}", 
                                       value=float(st.session_state.error_variables[var.name]["value"]),
                                       key=f"value_{var.name}")
                
                uncertainty = st.number_input(f"Uncertainty in {var.name}", 
                                           value=float(st.session_state.error_variables[var.name]["uncertainty"]),
                                           min_value=0.0,
                                           key=f"uncertainty_{var.name}")
                
                # Store values in session state
                st.session_state.error_variables[var.name]["value"] = value
                st.session_state.error_variables[var.name]["uncertainty"] = uncertainty
        
        # Calculate propagated error
        if st.button("Calculate Propagated Error") and variables:
            try:
                # Substitute values to calculate result
                subs_dict = {var.name: st.session_state.error_variables[var.name]["value"] for var in variables}
                result = expr.subs(subs_dict)
                
                # Calculate partial derivatives and propagate error
                error_squared_sum = 0
                
                for var in variables:
                    # Calculate partial derivative
                    partial_deriv = diff(expr, var)
                    
                    # Substitute values in the partial derivative
                    partial_deriv_value = partial_deriv.subs(subs_dict)
                    
                    # Get uncertainty for this variable
                    var_uncertainty = st.session_state.error_variables[var.name]["uncertainty"]
                    
                    # Add term to the sum
                    error_squared_sum += (partial_deriv_value * var_uncertainty) ** 2
                
                # Calculate propagated error
                propagated_error = math.sqrt(error_squared_sum)
                
                # Store the result
                st.session_state.propagated_error = propagated_error
                
                # Calculate percentage error
                if result != 0:
                    percentage_error = (propagated_error / abs(float(result))) * 100
                    st.session_state.percentage_error = percentage_error
                else:
                    percentage_error = None
                    st.session_state.percentage_error = None
                
                # Display results
                st.markdown(f"**Function:** {expression}")
                st.markdown(f"**Result:** {float(result):.6g} ± {propagated_error:.6g}")
                
                if percentage_error is not None:
                    st.markdown(f"**Percentage Error:** {percentage_error:.4g}%")
                
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
        st.success("Error analysis saved successfully! Continue to Report Generation.")
else:
    st.info("Complete the error analysis steps above to generate a summary.")
