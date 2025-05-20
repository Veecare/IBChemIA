import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from statsmodels.formula.api import ols
import statsmodels.api as sm
from utils.statistics import perform_t_test, perform_anova, calculate_correlation, calculate_regression
from utils.visualization import create_scatter_plot, create_bar_chart, create_box_plot

# Set page title
st.title("Data Analysis")
st.markdown("### Analyze and visualize your experimental data")

# Initialize session state variables if they don't exist
if 'data_df' not in st.session_state:
    st.session_state.data_df = pd.DataFrame()
if 'analysis_type' not in st.session_state:
    st.session_state.analysis_type = ""
if 'p_value' not in st.session_state:
    st.session_state.p_value = None
if 'stat_result' not in st.session_state:
    st.session_state.stat_result = None

# Step 1: Data Input
st.subheader("Step 1: Input Your Experimental Data")

# Option to use example data
use_example = st.checkbox("Use example data for demonstration", value=False)

if use_example:
    # Create example data based on experiment type if available
    if 'experiment_type' in st.session_state and st.session_state.experiment_type:
        if "titration" in st.session_state.experiment_type.lower():
            st.session_state.data_df = pd.DataFrame({
                'Concentration (mol/L)': [0.05, 0.10, 0.15, 0.20, 0.25],
                'Volume (mL)': [19.5, 9.8, 6.5, 4.9, 3.9],
                'Trial 1': [19.2, 9.5, 6.3, 4.8, 3.8],
                'Trial 2': [19.8, 9.9, 6.6, 4.9, 4.0],
                'Trial 3': [19.5, 10.0, 6.6, 5.0, 3.9]
            })
        elif "kinetics" in st.session_state.experiment_type.lower():
            st.session_state.data_df = pd.DataFrame({
                'Temperature (°C)': [10, 20, 30, 40, 50],
                'Rate (mol/L/s)': [0.012, 0.025, 0.047, 0.085, 0.145],
                'Trial 1': [0.011, 0.024, 0.045, 0.082, 0.142],
                'Trial 2': [0.012, 0.026, 0.049, 0.087, 0.148],
                'Trial 3': [0.013, 0.025, 0.047, 0.086, 0.145]
            })
        else:
            # Generic example data
            st.session_state.data_df = pd.DataFrame({
                'Independent Variable': [1, 2, 3, 4, 5],
                'Dependent Variable': [2.1, 3.9, 6.3, 8.2, 10.5],
                'Trial 1': [2.0, 4.0, 6.1, 8.0, 10.3],
                'Trial 2': [2.2, 3.8, 6.4, 8.3, 10.6],
                'Trial 3': [2.1, 3.9, 6.4, 8.3, 10.6]
            })
    else:
        # Generic example data
        st.session_state.data_df = pd.DataFrame({
            'Independent Variable': [1, 2, 3, 4, 5],
            'Dependent Variable': [2.1, 3.9, 6.3, 8.2, 10.5],
            'Trial 1': [2.0, 4.0, 6.1, 8.0, 10.3],
            'Trial 2': [2.2, 3.8, 6.4, 8.3, 10.6],
            'Trial 3': [2.1, 3.9, 6.4, 8.3, 10.6]
        })
else:
    # Manual data entry
    st.markdown("Enter your data manually or upload a CSV file:")
    
    # File upload option
    uploaded_file = st.file_uploader("Upload a CSV file with your data", type=["csv"])
    
    if uploaded_file is not None:
        try:
            st.session_state.data_df = pd.read_csv(uploaded_file)
            st.success("Data uploaded successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    # Manual data entry option
    st.markdown("Or enter data manually:")
    
    # Define the number of rows and columns for the data table
    num_rows = st.number_input("Number of data points", min_value=2, max_value=20, value=5)
    
    # Create column inputs
    col1_name = st.text_input("Independent Variable Name", 
                             value="Independent Variable" if "independent_var" not in st.session_state else st.session_state.independent_var)
    col2_name = st.text_input("Dependent Variable Name", 
                             value="Dependent Variable" if "dependent_var" not in st.session_state else st.session_state.dependent_var)
    
    # Number of trials
    num_trials = st.number_input("Number of trials", min_value=1, max_value=5, value=3)
    
    # Generate empty dataframe if not using uploaded data
    if uploaded_file is None and st.session_state.data_df.empty:
        data = {col1_name: [0] * num_rows, col2_name: [0] * num_rows}
        for i in range(1, num_trials + 1):
            data[f"Trial {i}"] = [0] * num_rows
        
        st.session_state.data_df = pd.DataFrame(data)
    
    # Display editable dataframe
    st.markdown("Edit your data:")
    
    # Create a form for data entry
    if not st.session_state.data_df.empty:
        # Convert dataframe to a dictionary for editing
        edited_data = {}
        
        for column in st.session_state.data_df.columns:
            edited_data[column] = st.session_state.data_df[column].tolist()
        
        # Create editable fields for each cell
        cols = st.columns(len(st.session_state.data_df.columns))
        
        # Display column headers
        for i, column in enumerate(st.session_state.data_df.columns):
            cols[i].markdown(f"**{column}**")
        
        # Display and edit data
        for row in range(len(st.session_state.data_df)):
            cols = st.columns(len(st.session_state.data_df.columns))
            
            for i, column in enumerate(st.session_state.data_df.columns):
                edited_data[column][row] = cols[i].number_input(
                    f"{column} row {row+1}",
                    value=float(edited_data[column][row]),
                    key=f"{column}_{row}",
                    label_visibility="collapsed"
                )
        
        # Update dataframe with edited data
        if st.button("Update Data Table"):
            for column in st.session_state.data_df.columns:
                st.session_state.data_df[column] = edited_data[column]
            st.success("Data updated successfully!")

# Display the current dataframe
if not st.session_state.data_df.empty:
    st.subheader("Current Data Table")
    st.dataframe(st.session_state.data_df)

# Step 2: Data Visualization
if not st.session_state.data_df.empty:
    st.subheader("Step 2: Data Visualization")
    
    # Select columns for visualization
    if len(st.session_state.data_df.columns) >= 2:
        x_col = st.selectbox("Select X-axis (Independent Variable)", options=st.session_state.data_df.columns)
        y_col = st.selectbox("Select Y-axis (Dependent Variable)", 
                            options=[col for col in st.session_state.data_df.columns if col != x_col],
                            index=1 if len(st.session_state.data_df.columns) > 1 else 0)
        
        # Select plot type
        plot_type = st.selectbox("Select plot type", ["Scatter", "Line", "Bar", "Box"])
        
        # Generate plot
        if plot_type == "Scatter":
            # Plot customization
            plot_title_scatter = st.text_input("Plot Title", value=f"{y_col} vs {x_col}", key="scatter_title")
            x_label_scatter = st.text_input("X-axis Label", value=x_col, key="scatter_xlabel")
            y_label_scatter = st.text_input("Y-axis Label", value=y_col, key="scatter_ylabel")
            marker_color_scatter = st.color_picker("Marker Color", value="#1f77b4", key="scatter_color")

            fig = create_scatter_plot(st.session_state.data_df, x_col, y_col, 
                                      title=plot_title_scatter, x_label=x_label_scatter, y_label=y_label_scatter,
                                      marker_color=marker_color_scatter)
        elif plot_type == "Line":
            plot_title_line = st.text_input("Plot Title", value=f"{y_col} vs {x_col}", key="line_title")
            x_label_line = st.text_input("X-axis Label", value=x_col, key="line_xlabel")
            y_label_line = st.text_input("Y-axis Label", value=y_col, key="line_ylabel")
            line_color_line = st.color_picker("Line Color", value="#1f77b4", key="line_color")

            fig = px.line(st.session_state.data_df, x=x_col, y=y_col, markers=True)
            fig.update_layout(title=plot_title_line, xaxis_title=x_label_line, yaxis_title=y_label_line)
            fig.update_traces(line=dict(color=line_color_line), marker=dict(color=line_color_line))

        elif plot_type == "Bar":
            # Basic customization for bar chart (can be expanded)
            plot_title_bar = st.text_input("Plot Title", value=f"{y_col} by {x_col}", key="bar_title")
            x_label_bar = st.text_input("X-axis Label", value=x_col, key="bar_xlabel")
            y_label_bar = st.text_input("Y-axis Label", value=y_col, key="bar_ylabel")
            
            fig = create_bar_chart(st.session_state.data_df, x_col, y_col)
            fig.update_layout(title=plot_title_bar, xaxis_title=x_label_bar, yaxis_title=y_label_bar)

        elif plot_type == "Box":
            # Basic customization for box plot (can be expanded)
            plot_title_box = st.text_input("Plot Title", value=f"Distribution of {y_col} by {x_col}", key="box_title")
            x_label_box = st.text_input("X-axis Label", value=x_col, key="box_xlabel")
            y_label_box = st.text_input("Y-axis Label", value=y_col, key="box_ylabel")

            fig = create_box_plot(st.session_state.data_df, x_col, y_col)
            fig.update_layout(title=plot_title_box, xaxis_title=x_label_box, yaxis_title=y_label_box)
        
        # Add regression line option for scatter plots
        if plot_type == "Scatter":
            add_regression = st.checkbox("Add regression line", value=True)
            
            if add_regression:
                # Add regression line
                x_values = st.session_state.data_df[x_col]
                y_values = st.session_state.data_df[y_col]
                
                # Check if x_values are not all identical
                if len(set(x_values)) > 1:
                    try:
                        # Calculate regression
                        slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
                        
                        # Add regression line to plot
                        x_range = np.linspace(min(x_values), max(x_values), 100)
                        y_range = slope * x_range + intercept
                        
                        regression_text = f"y = {slope:.4f}x + {intercept:.4f}<br>R² = {r_value**2:.4f}<br>p-value = {p_value:.4f}"
                    except Exception as e:
                        st.error(f"Error calculating regression: {str(e)}")
                        # Use default values so the plot still shows
                        slope, intercept, r_value, p_value, std_err = 0, 0, 0, 1, 0
                        regression_text = "Unable to calculate regression"
                        # Skip adding regression line
                        x_range = np.linspace(min(x_values), max(x_values), 100)
                        y_range = np.zeros_like(x_range)
                else:
                    st.warning("Cannot calculate a linear regression when all x values are identical. Try selecting a different x-axis variable.")
                    # Use default values so the plot still shows
                    slope, intercept, r_value, p_value, std_err = 0, 0, 0, 1, 0
                    regression_text = "Unable to calculate regression - identical x values"
                    # Skip adding regression line
                    x_range = np.linspace(min(x_values), max(x_values), 100)
                    y_range = np.zeros_like(x_range)
                
                fig.add_trace(go.Scatter(
                    x=x_range, 
                    y=y_range, 
                    mode='lines',
                    name='Regression Line',
                    line=dict(color='red', dash='dash')
                ))
                
                fig.add_annotation(
                    x=max(x_values) * 0.8,
                    y=min(y_values) * 1.2,
                    text=regression_text,
                    showarrow=False,
                    bgcolor="rgba(255, 255, 255, 0.8)"
                )
        
        # Display the plot
        st.plotly_chart(fig, use_container_width=True)
        
        # Display correlation for scatter plots
        if plot_type == "Scatter":
            correlation = st.session_state.data_df[x_col].corr(st.session_state.data_df[y_col])
            st.markdown(f"**Correlation coefficient (r):** {correlation:.4f}")
            st.markdown(f"**Coefficient of determination (R²):** {correlation**2:.4f}")
    
    else:
        st.warning("Need at least two columns of data for visualization.")

# Step 3: Statistical Analysis
if not st.session_state.data_df.empty:
    st.subheader("Step 3: Statistical Analysis")
    
    # Select analysis type
    analysis_options = ["T-test", "ANOVA", "Correlation", "Linear Regression", "Non-linear Regression"]
    selected_analysis = st.selectbox("Select statistical test", options=analysis_options)
    
    if selected_analysis != st.session_state.analysis_type:
        st.session_state.analysis_type = selected_analysis
        st.session_state.p_value = None
        st.session_state.stat_result = None
    
    # Perform selected analysis
    if selected_analysis == "T-test":
        st.markdown("Compare means of two groups to determine if they are significantly different.")
        
        # Get columns for t-test
        numeric_cols = st.session_state.data_df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            col1 = st.selectbox("Select first variable", options=numeric_cols)
            col2 = st.selectbox("Select second variable", 
                               options=[col for col in numeric_cols if col != col1],
                               index=1 if len(numeric_cols) > 1 else 0)
            
            # Perform t-test
            perform_assumption_checks_t = st.checkbox("Perform assumption checks for T-test", value=False)
            
            if st.button("Run T-test"):
                sample1 = st.session_state.data_df[col1].dropna()
                sample2 = st.session_state.data_df[col2].dropna()

                # Ensure enough data points for the t-test after removing NaNs
                if len(sample1) < 3 or len(sample2) < 3:
                    st.warning("Not enough data points for T-test after removing NaNs (minimum 3 required for each sample).")
                    return # Changed from st.stop() to return for better flow control if this page is part of a larger app

                if perform_assumption_checks_t:
                    st.markdown("#### T-test Assumption Checks:")
                    # Normality Check (Shapiro-Wilk Test)
                    # Tests if each sample deviates from a normal distribution.
                    # p-value < 0.05 suggests non-normality.
                    if len(sample1) >= 3: # Shapiro-Wilk needs at least 3 samples
                        shapiro_stat1, shapiro_p1 = stats.shapiro(sample1)
                        st.markdown(f"**Normality Check (Shapiro-Wilk) for '{col1}':** Statistic={shapiro_stat1:.4f}, P-value={shapiro_p1:.4f}")
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;*Interpretation: {'Normality assumption likely met (p ≥ 0.05).' if shapiro_p1 >= 0.05 else 'Normality assumption potentially NOT met (p < 0.05). Consider visual inspection (e.g., Q-Q plot) or alternative tests if sample size is small.'}*")
                    else:
                        st.markdown(f"**Normality Check (Shapiro-Wilk) for '{col1}':** Not enough data points (minimum 3 required).")

                    if len(sample2) >= 3:
                        shapiro_stat2, shapiro_p2 = stats.shapiro(sample2)
                        st.markdown(f"**Normality Check (Shapiro-Wilk) for '{col2}':** Statistic={shapiro_stat2:.4f}, P-value={shapiro_p2:.4f}")
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;*Interpretation: {'Normality assumption likely met (p ≥ 0.05).' if shapiro_p2 >= 0.05 else 'Normality assumption potentially NOT met (p < 0.05). Consider visual inspection or alternative tests if sample size is small.'}*")
                    else:
                        st.markdown(f"**Normality Check (Shapiro-Wilk) for '{col2}':** Not enough data points (minimum 3 required).")

                    # Homogeneity of Variances (Levene's Test)
                    # Tests if the variances of the two samples are equal.
                    # p-value < 0.05 suggests variances are not equal.
                    # The t-test performed by `perform_t_test` already uses `equal_var=False` (Welch's t-test),
                    # which does not assume equal variances, making this check informative but not critical for test validity.
                    levene_stat, levene_p = stats.levene(sample1, sample2)
                    st.markdown(f"**Homogeneity of Variances (Levene's Test):** Statistic={levene_stat:.4f}, P-value={levene_p:.4f}")
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;*Interpretation: {'Homogeneity of variances assumption likely met (p ≥ 0.05).' if levene_p >= 0.05 else 'Homogeneity of variances assumption potentially NOT met (p < 0.05). Note: Welch T-test is used by default, which handles unequal variances.'}*")
                    st.markdown("---") # Visual separator

                # Perform the t-test using the utility function
                result, p_value = perform_t_test(sample1, sample2) # Assumes perform_t_test handles potential errors
                st.session_state.stat_result = result
                st.session_state.p_value = p_value
                
                # Display results
                st.markdown(f"**T-statistic:** {result.statistic:.4f}")
                st.markdown(f"**P-value:** {p_value:.4f}")
                
                # Interpretation
                if p_value < 0.05:
                    st.success("The difference between means is statistically significant (p < 0.05).")
                else:
                    st.info("The difference between means is not statistically significant (p ≥ 0.05).")
        else:
            st.warning("Need at least two numeric columns for t-test.")
    
    elif selected_analysis == "ANOVA":
        st.markdown("Compare means across multiple groups to determine if any are significantly different.")
        
        # Get columns for ANOVA
        numeric_cols = st.session_state.data_df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 3:
            selected_cols = st.multiselect("Select variables for ANOVA", options=numeric_cols, default=numeric_cols[:3])
            
            if len(selected_cols) >= 2:
                perform_assumption_checks_anova = st.checkbox("Perform assumption checks for ANOVA", value=False)
                # Perform ANOVA
                if st.button("Run ANOVA"):
                    data_for_anova = [st.session_state.data_df[col].dropna() for col in selected_cols]
                    
                    # Check if any group has less than 3 data points after removing NaNs
                    if any(len(group) < 3 for group in data_for_anova):
                        st.warning("Not enough data points for ANOVA after removing NaNs (minimum 3 required for each group).")
                        return # Changed from st.stop()

                    if perform_assumption_checks_anova:
                        st.markdown("#### ANOVA Assumption Checks:")
                        # 1. Homogeneity of Variances (Levene's Test)
                        # Tests if the variance is the same across all groups.
                        # p-value < 0.05 suggests variances are not equal.
                        # ANOVA is somewhat robust to violations if group sizes are equal.
                        levene_stat, levene_p = stats.levene(*data_for_anova) # Unpack list of arrays for Levene's test
                        st.markdown(f"**Homogeneity of Variances (Levene's Test):** Statistic={levene_stat:.4f}, P-value={levene_p:.4f}")
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;*Interpretation: {'Homogeneity of variances assumption likely met (p ≥ 0.05).' if levene_p >= 0.05 else 'Homogeneity of variances assumption potentially NOT met (p < 0.05). If violated, consider alternative tests or transformations if group sizes are very unequal.'}*")

                        # 2. Normality of Residuals (Shapiro-Wilk Test)
                        # ANOVA assumes that the residuals (differences between observed and predicted values) are normally distributed.
                        # This is checked by fitting an OLS model and performing Shapiro-Wilk on its residuals.
                        
                        # Prepare data for OLS model: concatenate all values and create corresponding group labels
                        all_values = np.concatenate([group_data for group_data in data_for_anova if len(group_data) > 0]) # Ensure group_data is not empty
                        group_labels_ols = []
                        for i, group_data in enumerate(data_for_anova):
                            if len(group_data) > 0:
                                group_labels_ols.extend([selected_cols[i]] * len(group_data))
                        
                        if len(all_values) > 0 and len(all_values) == len(group_labels_ols):
                            df_for_ols = pd.DataFrame({'value': all_values, 'group': group_labels_ols})
                            
                            try:
                                # Fit an Ordinary Least Squares (OLS) model to get residuals
                                model = ols('value ~ C(group)', data=df_for_ols).fit()
                                residuals = model.resid
                                
                                if len(residuals) >= 3: # Shapiro-Wilk needs at least 3 samples
                                    shapiro_stat, shapiro_p = stats.shapiro(residuals)
                                    st.markdown(f"**Normality of Residuals (Shapiro-Wilk):** Statistic={shapiro_stat:.4f}, P-value={shapiro_p:.4f}")
                                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;*Interpretation: {'Normality of residuals assumption likely met (p ≥ 0.05).' if shapiro_p >= 0.05 else 'Normality of residuals assumption potentially NOT met (p < 0.05). Consider visual inspection (e.g., Q-Q plot of residuals) or transformations if violated.'}*")
                                else:
                                    st.markdown("**Normality of Residuals (Shapiro-Wilk):** Not enough data points for the test on residuals (minimum 3 required).")
                            except Exception as e:
                                st.markdown(f"**Normality of Residuals (Shapiro-Wilk):** Error during calculation - {e}")
                        else:
                            st.markdown("**Normality of Residuals (Shapiro-Wilk):** Not enough data across groups to perform the test.")
                        st.markdown("---") # Visual separator

                    # Perform ANOVA using the utility function
                    result, p_value = perform_anova(st.session_state.data_df, selected_cols) # Assumes perform_anova handles potential errors
                    st.session_state.stat_result = result
                    st.session_state.p_value = p_value
                    
                    # Display results
                    st.markdown(f"**F-statistic:** {result.iloc[0, 0]:.4f}")
                    st.markdown(f"**P-value:** {p_value:.4f}")
                    
                    # Display ANOVA table
                    st.markdown("**ANOVA Table:**")
                    st.dataframe(result)
                    
                    # Interpretation
                    if p_value < 0.05:
                        st.success("There are statistically significant differences between group means (p < 0.05).")
                    else:
                        st.info("There are no statistically significant differences between group means (p ≥ 0.05).")
            else:
                st.warning("Need at least two variables for ANOVA.")
        else:
            st.warning("Need at least three numeric columns for meaningful ANOVA.")
    
    elif selected_analysis == "Correlation":
        st.markdown("Measure the strength and direction of association between variables.")
        
        # Get columns for correlation
        numeric_cols = st.session_state.data_df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            corr_type = st.radio("Correlation type", ["Pearson", "Spearman"])
            
            # Calculate and display correlation matrix
            if st.button("Calculate Correlation Matrix"):
                corr_matrix, p_matrix = calculate_correlation(st.session_state.data_df[numeric_cols], corr_type.lower())
                
                # Display correlation matrix
                st.markdown(f"**{corr_type} Correlation Matrix:**")
                
                # Format correlation as a heatmap
                fig = px.imshow(
                    corr_matrix,
                    text_auto='.2f',
                    color_continuous_scale='RdBu_r',
                    zmin=-1, zmax=1,
                    aspect="auto"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Display p-values
                st.markdown("**P-value Matrix:**")
                p_df = pd.DataFrame(p_matrix, index=numeric_cols, columns=numeric_cols)
                
                # Format p-values with highlight for significant values
                def highlight_significant(val):
                    color = 'green' if val < 0.05 else 'black'
                    return f'color: {color}'
                
                styled_p = p_df.style.format("{:.4f}").applymap(highlight_significant)
                st.dataframe(styled_p)
                
                # Select specific variables for detailed interpretation
                st.markdown("### Select Variables for Detailed Interpretation")
                var1 = st.selectbox("Select first variable for interpretation", options=numeric_cols)
                var2 = st.selectbox("Select second variable for interpretation", 
                                   options=[col for col in numeric_cols if col != var1],
                                   index=1 if len(numeric_cols) > 1 else 0)
                
                # Get correlation and p-value for selected variables
                corr_val = corr_matrix.loc[var1, var2]
                p_val = p_matrix.loc[var1, var2]
                
                # Display interpretation
                st.markdown(f"**{corr_type} correlation between {var1} and {var2}:** {corr_val:.4f}")
                st.markdown(f"**P-value:** {p_val:.4f}")
                
                # Interpretation guide
                if abs(corr_val) < 0.3:
                    strength = "weak"
                elif abs(corr_val) < 0.7:
                    strength = "moderate"
                else:
                    strength = "strong"
                
                direction = "positive" if corr_val > 0 else "negative"
                
                st.markdown(f"This indicates a {strength} {direction} correlation.")
                
                if p_val < 0.05:
                    st.success("This correlation is statistically significant (p < 0.05).")
                else:
                    st.info("This correlation is not statistically significant (p ≥ 0.05).")
        else:
            st.warning("Need at least two numeric columns for correlation analysis.")
    
    elif selected_analysis == "Linear Regression":
        st.markdown("Model the relationship between variables using linear regression.")
        
        # Get columns for regression
        numeric_cols = st.session_state.data_df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            # Select dependent variable (y)
            y_var = st.selectbox("Select dependent variable (y)", options=numeric_cols)
            
            # Select independent variables (x)
            x_vars = st.multiselect("Select independent variables (x)", 
                                  options=[col for col in numeric_cols if col != y_var],
                                  default=[numeric_cols[0] if numeric_cols[0] != y_var else numeric_cols[1]])
            
            if x_vars:
                # Perform regression
                if st.button("Run Regression"):
                    # Perform regression analysis
                    result = calculate_regression(st.session_state.data_df, y_var, x_vars)
                    st.session_state.stat_result = result
                    
                    # Display summary
                    st.markdown("**Regression Summary:**")
                    st.text(result.summary().as_text())
                    
                    # Extract key statistics
                    r_squared = result.rsquared
                    adj_r_squared = result.rsquared_adj
                    f_stat = result.fvalue
                    f_pvalue = result.f_pvalue
                    
                    # Display key statistics
                    st.markdown(f"**R-squared:** {r_squared:.4f}")
                    st.markdown(f"**Adjusted R-squared:** {adj_r_squared:.4f}")
                    st.markdown(f"**F-statistic:** {f_stat:.4f}")
                    st.markdown(f"**F-statistic p-value:** {f_pvalue:.4f}")
                    
                    # Model equation
                    eq = f"y = {result.params[0]:.4f}"
                    for i, var in enumerate(x_vars):
                        coef = result.params[i+1]
                        sign = "+" if coef > 0 else ""
                        eq += f" {sign} {coef:.4f}×{var}"
                    
                    st.markdown(f"**Model Equation:** {eq}")
                    
                    # Interpretation
                    if f_pvalue < 0.05:
                        st.success("The regression model is statistically significant (p < 0.05).")
                    else:
                        st.info("The regression model is not statistically significant (p ≥ 0.05).")
                    
                    # Visualize the model if only one independent variable
                    if len(x_vars) == 1:
                        x_var = x_vars[0]
                        
                        # Create scatter plot with regression line
                        fig = px.scatter(st.session_state.data_df, x=x_var, y=y_var, title=f"Regression: {y_var} vs {x_var}")
                        
                        # Add regression line
                        x_range = np.linspace(min(st.session_state.data_df[x_var]), max(st.session_state.data_df[x_var]), 100)
                        y_pred = result.params[0] + result.params[1] * x_range
                        
                        fig.add_trace(go.Scatter(
                            x=x_range,
                            y=y_pred,
                            mode='lines',
                            name='Regression Line',
                            line=dict(color='red')
                        ))
                        
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Please select at least one independent variable.")
        else:
            st.warning("Need at least two numeric columns for regression analysis.")

    elif selected_analysis == "Non-linear Regression":
        st.markdown("Model non-linear relationships between variables.")
        
        non_linear_options = ["Polynomial Regression", "Exponential Regression"]
        selected_non_linear = st.selectbox("Select non-linear regression type", options=non_linear_options)

        numeric_cols = st.session_state.data_df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) >= 2:
            y_var = st.selectbox("Select dependent variable (y)", options=numeric_cols, key="non_linear_y")
            x_var = st.selectbox("Select independent variable (x)",
                                 options=[col for col in numeric_cols if col != y_var],
                                 key="non_linear_x")
            
            if selected_non_linear == "Polynomial Regression":
                degree = st.number_input("Select polynomial degree", min_value=2, max_value=10, value=2)

                if st.button("Run Polynomial Regression"):
                    x_data = st.session_state.data_df[x_var]
                    y_data = st.session_state.data_df[y_var]

                    try:
                        # Fit polynomial model using numpy.polyfit
                        # coeffs are returned in order of decreasing power (e.g., for degree 2: [a, b, c] for ax^2 + bx + c)
                        coeffs = np.polyfit(x_data, y_data, degree)
                        poly_model = np.poly1d(coeffs) # Creates a callable polynomial function
                        
                        # Calculate R-squared value for the polynomial fit
                        y_pred = poly_model(x_data) # Predicted y values from the model
                        ss_res = np.sum((y_data - y_pred)**2) # Residual sum of squares
                        ss_tot = np.sum((y_data - np.mean(y_data))**2) # Total sum of squares
                        if ss_tot == 0: # Avoid division by zero if all y_data points are the same
                            r_squared = 1 if ss_res == 0 else 0 # Perfect fit if ss_res is also 0, else no fit
                        else:
                            r_squared = 1 - (ss_res / ss_tot)
                        
                        # Store results in session state for potential use in other parts of the app (e.g., report generation)
                        st.session_state.stat_result = {
                            "model_type": "Polynomial Regression",
                            "coefficients": coeffs.tolist(), # Convert numpy array to list for JSON serializability if needed
                            "r_squared": r_squared,
                            "degree": degree,
                            "x_var": x_var,
                            "y_var": y_var,
                            "equation_str": np.poly1d(coeffs) # Store the poly1d object or its string representation
                        }
                        
                        # Display the fitted polynomial equation
                        equation_parts = []
                        for i, c in enumerate(coeffs):
                            power = degree - i
                            term = f"{c:+.4f}" # Format coefficient with sign and 4 decimal places
                            if power > 1:
                                term += f"x^{power}"
                            elif power == 1:
                                term += "x"
                            equation_parts.append(term)
                        equation_str = "y = " + " ".join(equation_parts).replace("+ -", "- ") # Clean up signs
                        
                        st.markdown(f"**Polynomial Equation (degree {degree}):** `{equation_str}`")
                        st.markdown(f"**R-squared (R²):** {r_squared:.4f}")
                        
                        # Visualization of the polynomial fit
                        plot_title_poly = st.text_input("Plot Title", value=f"Polynomial Regression: {y_var} vs {x_var}", key="poly_title")
                        x_label_poly = st.text_input("X-axis Label", value=x_var, key="poly_xlabel")
                        y_label_poly = st.text_input("Y-axis Label", value=y_var, key="poly_ylabel")
                        marker_color_poly = st.color_picker("Marker Color", value="#1f77b4", key="poly_marker_color")
                        line_color_poly = st.color_picker("Fit Line Color", value="red", key="poly_line_color")

                        fig = px.scatter(st.session_state.data_df, x=x_var, y=y_var)
                        fig.update_layout(title=plot_title_poly, xaxis_title=x_label_poly, yaxis_title=y_label_poly)
                        fig.update_traces(marker=dict(color=marker_color_poly))
                        
                        x_range_poly = np.linspace(x_data.min(), x_data.max(), 100)
                        y_range_poly = poly_model(x_range_poly)
                        fig.add_trace(go.Scatter(x=x_range_poly, y=y_range_poly, mode='lines', name=f"Degree {degree} Fit", line=dict(color=line_color_poly)))
                        st.plotly_chart(fig, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"Error performing polynomial regression: {e}")
            
            elif selected_non_linear == "Exponential Regression":
                if st.button("Run Exponential Regression"):
                    x_data = st.session_state.data_df[x_var]
                    y_data = st.session_state.data_df[y_var]

                    try:
                        # Define the exponential function to fit: y = a * exp(b * x)
                        def exp_func(x, a, b):
                            return a * np.exp(b * x)
                        
                        # Fit the exponential model using scipy.optimize.curve_fit
                        # p0 provides initial guesses for parameters [a, b]
                        # maxfev increases the number of iterations if convergence is an issue
                        params, covariance = stats.curve_fit(exp_func, x_data, y_data, p0=[1, 0.1], maxfev=10000)
                        a, b = params # Unpack fitted parameters
                        
                        # Calculate R-squared for the exponential fit
                        y_pred_exp = exp_func(x_data, a, b) # Predicted y values
                        ss_res_exp = np.sum((y_data - y_pred_exp)**2) # Residual sum of squares
                        ss_tot_exp = np.sum((y_data - np.mean(y_data))**2) # Total sum of squares
                        if ss_tot_exp == 0: # Avoid division by zero
                            r_squared_exp = 1 if ss_res_exp == 0 else 0
                        else:
                            r_squared_exp = 1 - (ss_res_exp / ss_tot_exp)
                        
                        # Store results in session state
                        st.session_state.stat_result = {
                            "model_type": "Exponential Regression",
                            "coefficients": {"a": a, "b": b},
                            "r_squared": r_squared_exp,
                            "x_var": x_var,
                            "y_var": y_var,
                            "equation_str": f"y = {a:.4f} * exp({b:.4f}x)"
                        }
                        
                        # Display the fitted exponential equation and R-squared value
                        st.markdown(f"**Exponential Equation:** `y = {a:.4f} * exp({b:.4f}x)`")
                        st.markdown(f"**R-squared (R²):** {r_squared_exp:.4f}")
                        
                        # Visualization of the exponential fit
                        plot_title_exp = st.text_input("Plot Title", value=f"Exponential Regression: {y_var} vs {x_var}", key="exp_title")
                        x_label_exp = st.text_input("X-axis Label", value=x_var, key="exp_xlabel")
                        y_label_exp = st.text_input("Y-axis Label", value=y_var, key="exp_ylabel")
                        marker_color_exp = st.color_picker("Marker Color", value="#1f77b4", key="exp_marker_color")
                        line_color_exp = st.color_picker("Fit Line Color", value="green", key="exp_line_color")

                        fig = px.scatter(st.session_state.data_df, x=x_var, y=y_var)
                        fig.update_layout(title=plot_title_exp, xaxis_title=x_label_exp, yaxis_title=y_label_exp)
                        fig.update_traces(marker=dict(color=marker_color_exp))
                        
                        x_range_exp = np.linspace(x_data.min(), x_data.max(), 100)
                        y_range_exp = exp_func(x_range_exp, a, b)
                        fig.add_trace(go.Scatter(x=x_range_exp, y=y_range_exp, mode='lines', name="Exponential Fit", line=dict(color=line_color_exp)))
                        st.plotly_chart(fig, use_container_width=True)

                    except RuntimeError:
                        st.error("Could not find optimal parameters for exponential fit. Ensure data follows an exponential trend.")
                    except Exception as e:
                        st.error(f"Error performing exponential regression: {e}")
        else:
            st.warning("Need at least two numeric columns for non-linear regression analysis.")


# Step 4: Statistical Significance and Conclusion
if not st.session_state.data_df.empty and st.session_state.analysis_type and st.session_state.p_value is not None and st.session_state.analysis_type not in ["Non-linear Regression"]:
    st.subheader("Step 4: Statistical Significance and Conclusion")
    
    # Set significance level
    alpha = st.slider("Significance level (α)", min_value=0.01, max_value=0.10, value=0.05, step=0.01)
    
    # Determine statistical significance
    is_significant = st.session_state.p_value < alpha
    
    # Display conclusion
    st.markdown("### Statistical Conclusion")
    
    if is_significant:
        st.success(f"The result is statistically significant (p = {st.session_state.p_value:.4f} < α = {alpha}).")
        st.markdown("**Interpretation:** We reject the null hypothesis.")
        
        if 'null_hypothesis' in st.session_state and 'alternative_hypothesis' in st.session_state:
            if st.session_state.null_hypothesis and st.session_state.alternative_hypothesis:
                st.markdown(f"Based on the statistical analysis, we reject the null hypothesis: *{st.session_state.null_hypothesis}*")
                st.markdown(f"The data provides sufficient evidence to support the alternative hypothesis: *{st.session_state.alternative_hypothesis}*")
    else:
        st.info(f"The result is not statistically significant (p = {st.session_state.p_value:.4f} ≥ α = {alpha}).")
        st.markdown("**Interpretation:** We fail to reject the null hypothesis.")
        
        if 'null_hypothesis' in st.session_state and 'alternative_hypothesis' in st.session_state:
            if st.session_state.null_hypothesis and st.session_state.alternative_hypothesis:
                st.markdown(f"Based on the statistical analysis, we fail to reject the null hypothesis: *{st.session_state.null_hypothesis}*")
                st.markdown(f"The data does not provide sufficient evidence to support the alternative hypothesis: *{st.session_state.alternative_hypothesis}*")
    
    # Prompt for scientific conclusion
    st.markdown("### Scientific Conclusion")
    st.markdown("Write a scientific conclusion based on your results and hypothesis:")
    
    scientific_conclusion = st.text_area("Scientific Conclusion", height=150, 
                                      help="Explain what your results mean in terms of your original hypothesis and the chemistry principles involved")
    
    if scientific_conclusion:
        st.session_state.scientific_conclusion = scientific_conclusion
