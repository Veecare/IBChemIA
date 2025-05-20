import streamlit as st
import pandas as pd
import numpy as np
import base64
from datetime import datetime
import io
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from utils.pdf_generator import generate_pdf_report
import json

# Set page title
st.title("IA Report Generation")
st.markdown("### Generate a complete IB Chemistry Internal Assessment report")

# Initialize session state variables if they don't exist
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
if 'candidate_number' not in st.session_state:
    st.session_state.candidate_number = ""
if 'school_name' not in st.session_state:
    st.session_state.school_name = ""
if 'teacher_name' not in st.session_state:
    st.session_state.teacher_name = ""
if 'experiment_date' not in st.session_state:
    st.session_state.experiment_date = datetime.today().strftime('%Y-%m-%d')
if 'word_count' not in st.session_state:
    st.session_state.word_count = 0
if 'title' not in st.session_state:
    st.session_state.title = ""
if 'introduction' not in st.session_state:
    st.session_state.introduction = ""
if 'conclusion' not in st.session_state:
    st.session_state.conclusion = ""
if 'evaluation' not in st.session_state:
    st.session_state.evaluation = ""
if 'references_list' not in st.session_state:
    st.session_state.references_list = []
if 'citation_style' not in st.session_state:
    st.session_state.citation_style = "APA"
if 'references_text' not in st.session_state: # To store raw text area content
    st.session_state.references_text = ""


# Section 1: Report Information
st.subheader("Report Information")

col1, col2 = st.columns(2)

with col1:
    st.session_state.student_name = st.text_input("Student Name", value=st.session_state.student_name)
    st.session_state.school_name = st.text_input("School Name", value=st.session_state.school_name)
    # Handle the experiment date properly
    if isinstance(st.session_state.experiment_date, str):
        try:
            default_date = datetime.strptime(st.session_state.experiment_date, '%Y-%m-%d')
        except ValueError:
            default_date = datetime.today()
    elif hasattr(st.session_state.experiment_date, 'year'):  # Check if it's a date-like object
        default_date = st.session_state.experiment_date
    else:
        default_date = datetime.today()
        
    st.session_state.experiment_date = st.date_input("Experiment Date", value=default_date)

with col2:
    st.session_state.candidate_number = st.text_input("Candidate Number", value=st.session_state.candidate_number)
    st.session_state.teacher_name = st.text_input("Teacher Name", value=st.session_state.teacher_name)
    
    # Generate/Update IA title if experiment info exists
    if 'experiment_topic' in st.session_state and 'experiment_type' in st.session_state:
        if st.session_state.experiment_topic and st.session_state.experiment_type:
            # Generate a suggested title
            if not st.session_state.title:
                if 'independent_var' in st.session_state and 'dependent_var' in st.session_state:
                    suggested_title = f"Investigating the Effect of {st.session_state.independent_var} on {st.session_state.dependent_var}"
                else:
                    suggested_title = f"Investigation of {st.session_state.experiment_type} in {st.session_state.experiment_topic}"
                
                st.session_state.title = suggested_title

# IA Title
st.markdown("#### IA Title")
st.session_state.title = st.text_input("IA Title", value=st.session_state.title)

# Section 2: Report Structure
st.subheader("Report Structure")

# Show the IB Assessment Criteria
with st.expander("View IB Chemistry IA Assessment Criteria"):
    st.markdown("""
    ### IB Chemistry IA Assessment Criteria (24 marks total)

    #### Personal Engagement (2 marks)
    - Demonstrate personal significance, interest, or curiosity
    - Demonstrate ownership through individual approaches/ideas

    #### Exploration (6 marks)
    - Define focused research question and relevant variables
    - Develop methodologies appropriate to the research question
    - Demonstrate understanding of relevant scientific context

    #### Analysis (6 marks)
    - Record, process, and present data in ways relevant to the question
    - Interpret data and explain results using scientific understanding
    - Evaluate the validity of the method and reliability of data

    #### Evaluation (6 marks)
    - Discuss strengths, weaknesses, and limitations of the investigation
    - Suggest realistic improvements with justification
    - Describe the significance of the investigation within scientific context

    #### Communication (4 marks)
    - Structure the report coherently with appropriate terminology
    - Present information clearly with proper citations
    - Stay within the 12-page limit (not counting raw data)
    """)

# Report template selections
report_tab1, report_tab2, report_tab3, report_tab4, report_tab5, report_tab6 = st.tabs([
    "Introduction", "Methodology", "Results", "Conclusion", "Evaluation", "References"
])

# Tab 1: Introduction
with report_tab1:
    st.markdown("### Introduction")
    st.markdown("""
    Your introduction should include:
    - Background information on the chemistry topic
    - Relevance and significance of the investigation
    - Clear statement of the research question
    - Hypothesis and scientific basis for your prediction
    """)
    
    # Generate a template introduction if we have the necessary information
    intro_template = ""
    if 'experiment_topic' in st.session_state and 'hypothesis' in st.session_state:
        if st.session_state.experiment_topic and st.session_state.hypothesis:
            intro_template = f"""In this investigation, I will explore {st.session_state.experiment_topic} through an experiment designed to answer the research question: "{st.session_state.title.strip()}?"

Based on my research and understanding of chemical principles, I hypothesize that {st.session_state.hypothesis}

This investigation is significant because [explain why this topic is important in chemistry or real-world applications].

[Add relevant chemistry theory and background information here to support your hypothesis]
"""
    
    if not st.session_state.introduction and intro_template:
        st.session_state.introduction = intro_template
    
    st.session_state.introduction = st.text_area("Write your introduction", 
                                               value=st.session_state.introduction,
                                               height=300,
                                               help="Introduce your topic, state your research question, and provide scientific background")
    
    # Calculate and display word count
    word_count = len(st.session_state.introduction.split())
    st.markdown(f"Word count: {word_count} words")

# Tab 2: Methodology
with report_tab2:
    st.markdown("### Methodology")
    
    if 'methodology' in st.session_state and st.session_state.methodology:
        st.markdown("Your saved experimental procedure:")
        st.text_area("Methodology", value=st.session_state.methodology, height=200, disabled=True)
    else:
        st.warning("No methodology found. Please complete the Experiment Planning section first.")
    
    if 'materials' in st.session_state and st.session_state.materials:
        st.markdown("Your materials list:")
        materials_text = "\n".join([f"- {material}" for material in st.session_state.materials])
        st.markdown(materials_text)
    else:
        st.warning("No materials list found. Please complete the Experiment Planning section first.")
    
    if 'independent_var' in st.session_state and 'dependent_var' in st.session_state and 'controlled_vars' in st.session_state:
        if st.session_state.independent_var and st.session_state.dependent_var:
            st.markdown("### Variables")
            st.markdown(f"**Independent Variable:** {st.session_state.independent_var}")
            st.markdown(f"**Dependent Variable:** {st.session_state.dependent_var}")
            
            if st.session_state.controlled_vars:
                st.markdown("**Controlled Variables:**")
                for var in st.session_state.controlled_vars:
                    st.markdown(f"- {var}")
    
    if 'safety_considerations' in st.session_state and st.session_state.safety_considerations:
        st.markdown("### Safety Considerations")
        st.markdown(st.session_state.safety_considerations)

# Tab 3: Results
with report_tab3:
    st.markdown("### Results")
    
    if 'data_df' in st.session_state and not st.session_state.data_df.empty:
        st.markdown("#### Raw Data")
        st.dataframe(st.session_state.data_df)
        
        st.markdown("#### Data Visualization")
        
        # If we have visualizations from the data analysis section, display them
        if 'data_df' in st.session_state and not st.session_state.data_df.empty:
            # Select columns for visualization
            if len(st.session_state.data_df.columns) >= 2:
                x_col = st.selectbox("Select X-axis", options=st.session_state.data_df.columns)
                y_col = st.selectbox("Select Y-axis", 
                                  options=[col for col in st.session_state.data_df.columns if col != x_col],
                                  index=1 if len(st.session_state.data_df.columns) > 1 else 0)
                
                # Create graph
                fig = px.scatter(st.session_state.data_df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                
                # Add regression line
                add_trendline = st.checkbox("Add trendline", value=True)
                if add_trendline:
                    fig = px.scatter(st.session_state.data_df, x=x_col, y=y_col, 
                                   trendline="ols", title=f"{y_col} vs {x_col}")
                    
                    # Calculate regression statistics
                    import statsmodels.api as sm
                    from statsmodels.formula.api import ols
                    
                    # Create regression model
                    formula = f"{y_col} ~ {x_col}"
                    model = ols(formula, data=st.session_state.data_df).fit()
                    
                    # Display regression summary
                    st.markdown("#### Regression Analysis")
                    st.text(model.summary().tables[1].as_text())
                    
                    # Display equation
                    equation = f"y = {model.params[1]:.4f}x + {model.params[0]:.4f}"
                    r_squared = f"R² = {model.rsquared:.4f}"
                    st.markdown(f"**Equation:** {equation}")
                    st.markdown(f"**{r_squared}**")
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Save this visualization for the report
                st.session_state.results_visualization = {
                    'x_col': x_col,
                    'y_col': y_col,
                    'add_trendline': add_trendline
                }
        else:
            st.warning("No data available for visualization.")
        
        # Statistical results
        if 'stat_result' in st.session_state and st.session_state.stat_result is not None:
            st.markdown("#### Statistical Analysis")
            
            if 'analysis_type' in st.session_state:
                st.markdown(f"**Analysis Type:** {st.session_state.analysis_type}")
                
                if st.session_state.analysis_type == "T-test":
                    st.markdown(f"**T-statistic:** {st.session_state.stat_result.statistic:.4f}")
                    st.markdown(f"**P-value:** {st.session_state.p_value:.4f}")
                    
                    if st.session_state.p_value < 0.05:
                        st.success("The difference between means is statistically significant (p < 0.05).")
                    else:
                        st.info("The difference between means is not statistically significant (p ≥ 0.05).")
                
                elif st.session_state.analysis_type == "ANOVA":
                    st.dataframe(st.session_state.stat_result)
                    st.markdown(f"**P-value:** {st.session_state.p_value:.4f}")
                    
                    if st.session_state.p_value < 0.05:
                        st.success("There are statistically significant differences between group means (p < 0.05).")
                    else:
                        st.info("There are no statistically significant differences between group means (p ≥ 0.05).")
                
                elif st.session_state.analysis_type == "Linear Regression":
                    st.text(st.session_state.stat_result.summary().as_text())
        
        # Error analysis
        if 'calculated_abs_uncertainty' in st.session_state and 'calculated_percentage_uncertainty' in st.session_state:
            st.markdown("#### Uncertainty Analysis")
            st.markdown(f"**Absolute Uncertainty:** ±{st.session_state.calculated_abs_uncertainty:.6g}")
            st.markdown(f"**Percentage Uncertainty:** {st.session_state.calculated_percentage_uncertainty:.4g}%")
    else:
        st.warning("No data found. Please complete the Data Analysis section first.")

# Tab 4: Conclusion
with report_tab4:
    st.markdown("### Conclusion")
    st.markdown("""
    Your conclusion should include:
    - Summary of key findings
    - Interpretation of results in relation to your hypothesis
    - Discussion of whether your hypothesis was supported or rejected
    - Explanation of results using chemistry principles
    """)
    
    # Generate a template conclusion if we have the necessary information
    conclusion_template = ""
    if 'hypothesis' in st.session_state and 'p_value' in st.session_state:
        if st.session_state.hypothesis and st.session_state.p_value is not None:
            hypothesis_supported = st.session_state.p_value < 0.05
            
            if hypothesis_supported:
                conclusion_template = f"""Based on the data and statistical analysis (p-value = {st.session_state.p_value:.4f}), there is sufficient evidence to support my hypothesis that {st.session_state.hypothesis}

The results show [describe key patterns or trends in your data].

This can be explained by the chemistry principle that [explain the chemistry behind your results].

[Discuss how your findings connect to the broader scientific context]
"""
            else:
                conclusion_template = f"""Based on the data and statistical analysis (p-value = {st.session_state.p_value:.4f}), there is insufficient evidence to support my hypothesis that {st.session_state.hypothesis}

The results show [describe key patterns or trends in your data].

This unexpected outcome may be explained by [propose reasons for why your hypothesis wasn't supported].

[Discuss how your findings still contribute to understanding the chemistry concept]
"""
    
    if not st.session_state.conclusion and conclusion_template:
        st.session_state.conclusion = conclusion_template
    
    st.session_state.conclusion = st.text_area("Write your conclusion", 
                                             value=st.session_state.conclusion,
                                             height=300,
                                             help="Interpret your results in relation to your hypothesis")
    
    # Calculate and display word count
    word_count = len(st.session_state.conclusion.split())
    st.markdown(f"Word count: {word_count} words")

# Tab 5: Evaluation
with report_tab5:
    st.markdown("### Evaluation")
    st.markdown("""
    Your evaluation should include:
    - Discussion of strengths and limitations of your methodology
    - Analysis of experimental errors and their impact on results
    - Suggestions for improvements with specific details
    - Discussion of further research questions that arose
    """)
    
    # Generate a template evaluation if we have the necessary information
    evaluation_template = ""
    if 'random_errors' in st.session_state and 'systematic_errors' in st.session_state:
        if st.session_state.random_errors or st.session_state.systematic_errors:
            evaluation_template = "#### Strengths and Limitations\n\nStrengths of this investigation include [list key strengths of your methodology].\n\n"
            
            evaluation_template += "Limitations of this investigation include:\n\n"
            
            # Add random errors
            if st.session_state.random_errors:
                evaluation_template += "Random Errors:\n"
                for error in st.session_state.random_errors:
                    evaluation_template += f"- {error}\n"
                evaluation_template += "\n"
            
            # Add systematic errors
            if st.session_state.systematic_errors:
                evaluation_template += "Systematic Errors:\n"
                for error in st.session_state.systematic_errors:
                    evaluation_template += f"- {error}\n"
                evaluation_template += "\n"
            
            evaluation_template += "#### Improvements\n\nTo improve this investigation, I would make the following changes:\n\n"
            evaluation_template += "1. [Specific improvement 1 with detailed explanation]\n"
            evaluation_template += "2. [Specific improvement 2 with detailed explanation]\n"
            evaluation_template += "3. [Specific improvement 3 with detailed explanation]\n\n"
            
            evaluation_template += "#### Further Research\n\nBased on this investigation, the following questions emerged that could be investigated further:\n\n"
            evaluation_template += "1. [New research question 1]\n"
            evaluation_template += "2. [New research question 2]\n"
    
    if not st.session_state.evaluation and evaluation_template:
        st.session_state.evaluation = evaluation_template
    
    st.session_state.evaluation = st.text_area("Write your evaluation", 
                                             value=st.session_state.evaluation,
                                             height=300,
                                             help="Evaluate your investigation and suggest improvements")
    
    # Calculate and display word count
    word_count = len(st.session_state.evaluation.split())
    st.markdown(f"Word count: {word_count} words")

# Tab 6: References
with report_tab6:
    st.markdown("### References")
    st.markdown("Enter each reference on a new line. Ensure consistent formatting according to your chosen style.")
    
    st.session_state.references_text = st.text_area(
        "List of References",
        value=st.session_state.references_text,
        height=200,
        help="Enter each reference on a new line."
    )
    # Update references_list based on text_area input
    if st.session_state.references_text:
        st.session_state.references_list = [ref.strip() for ref in st.session_state.references_text.split("\n") if ref.strip()]
    else:
        st.session_state.references_list = []

    st.session_state.citation_style = st.selectbox(
        "Select Citation Style",
        options=["APA", "MLA", "Chicago"],
        index=["APA", "MLA", "Chicago"].index(st.session_state.citation_style) # Set current style
    )
    st.markdown(f"You have chosen **{st.session_state.citation_style}** style. Please format your references accordingly above.")
    # Note: Actual formatting according to APA/MLA/Chicago is not automatically applied by this tool;
    # the user is responsible for formatting the references correctly in the text area.
    # The selected style is for documentation purposes in the generated report.

# Total word count
total_words = len(st.session_state.introduction.split()) + len(st.session_state.conclusion.split()) + len(st.session_state.evaluation.split())
st.session_state.word_count = total_words

st.markdown(f"**Total Word Count:** {total_words} words (excluding references, methodology, and raw data)")


# --- Report Generation and Export ---
st.subheader("Generate and Export Report")

col_pdf, col_md = st.columns(2)

with col_pdf:
    if st.button("Generate IA Report (PDF)"):
        # Check if essential sections are completed
        if not st.session_state.student_name:
            st.error("Please enter your name before generating the report.")
        elif not st.session_state.title:
            st.error("Please enter a title for your IA before generating the report.")
        elif not st.session_state.introduction:
            st.error("Please write an introduction before generating the report.")
        elif 'data_df' not in st.session_state or st.session_state.data_df.empty:
            st.error("Please add data in the Data Analysis section before generating the report.")
        elif not st.session_state.conclusion:
            st.error("Please write a conclusion before generating the report.")
        else:
            try:
                # Create a dictionary with all report data
                report_data = {
                    "student_name": st.session_state.student_name,
                    "candidate_number": st.session_state.candidate_number,
                    "school_name": st.session_state.school_name,
                    "teacher_name": st.session_state.teacher_name,
                    "experiment_date": st.session_state.experiment_date.strftime('%Y-%m-%d') if isinstance(st.session_state.experiment_date, datetime) else st.session_state.experiment_date,
                    "title": st.session_state.title,
                    "word_count": st.session_state.word_count,
                    "introduction": st.session_state.introduction,
                    "methodology": st.session_state.get('methodology', ""), # Use .get for safety
                    "materials": st.session_state.get('materials', []),
                    "independent_var": st.session_state.get('independent_var', ""),
                    "dependent_var": st.session_state.get('dependent_var', ""),
                    "controlled_vars": st.session_state.get('controlled_vars', []),
                    "safety_considerations": st.session_state.get('safety_considerations', ""),
                    "hypothesis": st.session_state.get('hypothesis', ""),
                    "data_df": st.session_state.get('data_df', pd.DataFrame()), # Pass dataframe directly
                    "results_visualization": st.session_state.get('results_visualization', {}), # For plot regeneration
                    "conclusion": st.session_state.conclusion,
                    "evaluation": st.session_state.evaluation,
                    "random_errors": st.session_state.get('random_errors', []),
                    "systematic_errors": st.session_state.get('systematic_errors', []),
                    "references_list": st.session_state.get('references_list', []),
                    "citation_style": st.session_state.get('citation_style', "APA")
                }
                
                # Generate PDF report
                pdf_bytes = generate_pdf_report(report_data)
                
                # Create a download button for the PDF
                b64_pdf = base64.b64encode(pdf_bytes).decode()
                pdf_filename = f"{st.session_state.student_name.replace(' ', '_')}_Chemistry_IA.pdf"
                href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_filename}">Download PDF Report</a>'
                st.markdown(href, unsafe_allow_html=True)
                
                st.success("IA report generated successfully!")
                
                # Also allow downloading the report data as JSON for future use
                # Convert dataframe to dict for JSON serialization
                report_data_json = report_data.copy()
                if isinstance(report_data_json['data_df'], pd.DataFrame):
                    report_data_json['data_df'] = report_data_json['data_df'].to_dict(orient='list')

                report_json_str = json.dumps(report_data_json, indent=2)
                b64_json = base64.b64encode(report_json_str.encode()).decode()
                json_filename = f"{st.session_state.student_name.replace(' ', '_')}_Chemistry_IA_Data.json"
                href_json = f'<a href="data:application/json;base64,{b64_json}" download="{json_filename}">Download Report Data (JSON)</a>'
                st.markdown(href_json, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error generating PDF report: {e}")
                st.exception(e) # show full traceback for debugging

# Generate Report Button
if st.button("Generate IA Report"):
    # Check if essential sections are completed
    if not st.session_state.student_name:
        st.error("Please enter your name before generating the report.")
    elif not st.session_state.title:
        st.error("Please enter a title for your IA before generating the report.")
    elif not st.session_state.introduction:
        st.error("Please write an introduction before generating the report.")
    elif 'data_df' not in st.session_state or st.session_state.data_df.empty:
        st.error("Please add data in the Data Analysis section before generating the report.")
    elif not st.session_state.conclusion:
        st.error("Please write a conclusion before generating the report.")
    else:
        try:
# Placeholder for Markdown generation logic, will be filled in next step
def generate_markdown_report(report_data):
    """
    Generates a Markdown string representation of the IA report.

    Args:
        report_data (dict): A dictionary containing all the necessary data
                            for the report, mirroring the structure used for PDF generation.
                            Includes sections like title, student_name, introduction,
                            methodology, data (as DataFrame), conclusion, evaluation,
                            references, etc.

    Returns:
        str: A string formatted in Markdown containing the entire report content.
    """
    md_content = []
    md_content.append(f"# {report_data.get('title', 'Untitled Report')}")
    
    # Basic Information
    md_content.append(f"**Student:** {report_data.get('student_name', 'N/A')}")
    if report_data.get('candidate_number'):
        md_content.append(f"**Candidate Number:** {report_data.get('candidate_number')}")
    md_content.append(f"**School:** {report_data.get('school_name', 'N/A')}")
    if report_data.get('teacher_name'):
        md_content.append(f"**Teacher:** {report_data.get('teacher_name')}")
    md_content.append(f"**Experiment Date:** {report_data.get('experiment_date', 'N/A')}")
    md_content.append(f"**Word Count (main sections):** {report_data.get('word_count', 0)}")

    # Introduction
    md_content.append("\n## Introduction")
    md_content.append(f"**Research Question (from title):** {report_data.get('title', 'N/A')}") # Assuming title is RQ
    md_content.append(f"**Hypothesis (Scientific):** {report_data.get('hypothesis', 'N/A')}")
    md_content.append("\n" + report_data.get('introduction', 'No introduction provided.'))
    
    # Methodology
    md_content.append("\n## Methodology")
    if report_data.get('materials'):
        md_content.append("### Materials")
        for item in report_data.get('materials', []):
            md_content.append(f"- {item}")
    
    md_content.append("\n### Variables")
    md_content.append(f"- **Independent Variable:** {report_data.get('independent_var', 'N/A')}")
    md_content.append(f"- **Dependent Variable:** {report_data.get('dependent_var', 'N/A')}")
    if report_data.get('controlled_vars'):
        md_content.append("- **Controlled Variables:**")
        for item in report_data.get('controlled_vars', []):
            md_content.append(f"  - {item}")
            
    md_content.append("\n### Procedure")
    md_content.append(report_data.get('methodology', 'No procedure provided.'))
    
    if report_data.get('safety_considerations'):
        md_content.append("\n### Safety Considerations")
        md_content.append(report_data.get('safety_considerations', 'No safety considerations provided.'))

    # Results and Data Analysis
    md_content.append("\n## Results and Data Analysis")
    # Raw Data Table
    if 'data_df' in report_data and not report_data['data_df'].empty:
        md_content.append("### Raw Data Table")
        try:
            # Convert DataFrame to Markdown table. `index=False` avoids writing DataFrame index.
            if isinstance(report_data['data_df'], pd.DataFrame):
                 md_content.append(report_data['data_df'].to_markdown(index=False))
            elif isinstance(report_data['data_df'], dict): # Handles data loaded from JSON (e.g. from progress file)
                df_for_md = pd.DataFrame(report_data['data_df'])
                if not df_for_md.empty:
                    md_content.append(df_for_md.to_markdown(index=False))
                else:
                    md_content.append("*Data table is empty or could not be converted.*")
            else:
                md_content.append("*Data table format not recognized for Markdown export.*")
        except Exception as e:
            md_content.append(f"*Could not render data table for Markdown: {e}*")
    else:
        md_content.append("*No raw data table provided or data is empty.*")

    # Processed Data and Visualizations (Placeholder - visualizations are not directly embedded in Markdown)
    md_content.append("\n### Data Visualization")
    md_content.append("*Refer to generated plots. Markdown export does not embed interactive plots directly. Consider attaching image files separately or using the PDF report for figures.*")
    if 'results_visualization' in report_data and report_data['results_visualization']:
        viz_info = report_data['results_visualization']
        md_content.append(f"A plot of '{viz_info.get('y_col')}' vs '{viz_info.get('x_col')}' was generated" + 
                          (" with a trendline." if viz_info.get('add_trendline') else "."))

    # Statistical Analysis Summary (Simplified for Markdown)
    md_content.append("\n### Statistical Analysis")
    if 'analysis_type' in report_data and report_data.get('stat_result') is not None:
        md_content.append(f"**Analysis Type:** {report_data['analysis_type']}")
        # Specific details would depend on how stat_result is structured for each type.
        # This is a simplified representation.
        md_content.append(f"*Statistical results were obtained. Refer to the application or PDF report for detailed tables and values (e.g., T-statistic, P-value, R-squared, ANOVA table).*")
        if 'p_value' in report_data and report_data['p_value'] is not None:
             md_content.append(f"**Overall P-value (if applicable):** {report_data['p_value']:.4f}")
    else:
        md_content.append("*No detailed statistical analysis results were found in the report data for Markdown export.*")

    # Uncertainty Analysis
    if report_data.get('calculated_abs_uncertainty') is not None:
        md_content.append("\n### Uncertainty Analysis")
        md_content.append(f"- **Calculated Absolute Uncertainty:** ±{report_data.get('calculated_abs_uncertainty'):.6g}")
        md_content.append(f"- **Calculated Percentage Uncertainty:** {report_data.get('calculated_percentage_uncertainty'):.4g}%")
    if report_data.get('propagated_error') is not None:
        md_content.append(f"- **Propagated Error (if calculated):** ±{report_data.get('propagated_error'):.6g}")
        if report_data.get('percentage_error') is not None:
             md_content.append(f"- **Propagated Percentage Error:** {report_data.get('percentage_error'):.4g}%")
    
    # Conclusion
    md_content.append("\n## Conclusion")
    md_content.append(report_data.get('conclusion', 'No conclusion provided.'))

    # Evaluation
    md_content.append("\n## Evaluation")
    md_content.append(report_data.get('evaluation', 'No evaluation provided.'))
    # Identified Errors
    if report_data.get('random_errors'):
        md_content.append("\n### Identified Random Errors:")
        for error in report_data.get('random_errors', []):
            md_content.append(f"- {error}")
    if report_data.get('systematic_errors'):
        md_content.append("\n### Identified Systematic Errors:")
        for error in report_data.get('systematic_errors', []):
            md_content.append(f"- {error}")

    # References
    md_content.append("\n## References")
    md_content.append(f"**Desired Citation Style:** {report_data.get('citation_style', 'APA')}")
    if report_data.get('references_list'):
        for ref in report_data.get('references_list', []):
            md_content.append(f"- {ref}")
    else:
        md_content.append("*No references provided.*")
    
    # Join all parts of the Markdown content with double newlines for paragraph separation.
    return "\n\n".join(md_content)

with col_md:
    if st.button("Export Report as Markdown"):
        # Re-use the same data dictionary as for PDF
        report_data_md = {
            "student_name": st.session_state.student_name,
            "candidate_number": st.session_state.candidate_number,
            "school_name": st.session_state.school_name,
            "teacher_name": st.session_state.teacher_name,
            "experiment_date": st.session_state.experiment_date.strftime('%Y-%m-%d') if isinstance(st.session_state.experiment_date, datetime) else st.session_state.experiment_date,
            "title": st.session_state.title,
            "word_count": st.session_state.word_count,
            "introduction": st.session_state.introduction,
            "methodology": st.session_state.get('methodology', ""),
            "materials": st.session_state.get('materials', []),
            "independent_var": st.session_state.get('independent_var', ""),
            "dependent_var": st.session_state.get('dependent_var', ""),
            "controlled_vars": st.session_state.get('controlled_vars', []),
            "safety_considerations": st.session_state.get('safety_considerations', ""),
            "hypothesis": st.session_state.get('hypothesis', ""),
            "data_df": st.session_state.get('data_df', pd.DataFrame()), # Pass dataframe
            "conclusion": st.session_state.conclusion,
            "evaluation": st.session_state.evaluation,
            "random_errors": st.session_state.get('random_errors', []),
            "systematic_errors": st.session_state.get('systematic_errors', []),
            "references_list": st.session_state.get('references_list', []),
            "citation_style": st.session_state.get('citation_style', "APA")
        }
        markdown_output = generate_markdown_report(report_data_md)
        md_filename = f"{st.session_state.student_name.replace(' ', '_')}_Chemistry_IA.md"
        st.download_button(
            label="Download Markdown Report",
            data=markdown_output,
            file_name=md_filename,
            mime="text/markdown"
        )
        st.success("Markdown report generated!")
