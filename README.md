# IB Chemistry IA Lab Tool

IBChemIA Lab Tool is a comprehensive Streamlit web application designed to assist IB Chemistry students throughout their Internal Assessment (IA) process, from initial planning to final report generation.

## Overview

The IB Chemistry IA is a significant component of the course, requiring students to design, execute, analyze, and evaluate their own scientific investigation. This tool aims to streamline this process by providing structured guidance, calculation utilities, and report generation features tailored to IB requirements.

## Features

The application is organized into several modules, accessible via the sidebar navigation:

*   **Experiment Planning:**
    *   Select from a predefined list of IB Chemistry topics.
    *   Choose an experiment type relevant to the selected topic (e.g., Titration, Kinetics, Calorimetry).
    *   Receive experiment templates with suggested independent/dependent variables, controlled variables, materials, and basic methodology.
    *   Define and customize independent, dependent, and controlled variables.
    *   List required materials and equipment.
    *   Outline the experimental procedure step-by-step.
    *   Document safety considerations with suggestions based on experiment type.
    *   Save the experiment plan to proceed to other sections.

*   **Hypothesis Testing:**
    *   Formulate a clear scientific hypothesis based on the planned experiment (using "If...then...because..." format).
    *   Define corresponding null (H₀) and alternative (H₁) statistical hypotheses.
    *   Provide a detailed scientific rationale for the hypothesis based on chemical principles.
    *   Evaluate the formulated hypothesis against IB criteria (testable, specific, etc.).
    *   Save the hypothesis details.

*   **Data Analysis:**
    *   Input experimental data manually or by uploading a CSV file.
    *   Perform various statistical analyses:
        *   **Descriptive Statistics**: Mean, standard deviation, range.
        *   **T-tests**: Compare means of two groups.
        *   **ANOVA**: Compare means across multiple groups.
        *   **Correlation Analysis**: Pearson and Spearman correlation with p-values.
        *   **Linear Regression**: Model linear relationships.
        *   **Non-linear Regression**: Includes Polynomial and Exponential regression models.
    *   **Assumption Checking**: Optional checks for T-tests (Shapiro-Wilk for normality, Levene's for homogeneity of variances) and ANOVA (Levene's, Shapiro-Wilk on residuals).
    *   Visualize data with various plot types (Scatter, Line, Bar, Box).
    *   **Plot Customization**: Modify plot titles, axis labels, and marker/line colors.
    *   Interpret statistical results and p-values in the context of the hypothesis.

*   **Error Analysis:**
    *   Identify and list potential random and systematic errors.
    *   Calculate absolute and percentage uncertainty from experimental data (Range Method, Standard Deviation, Standard Error) or instrument precision.
    *   **Equipment Uncertainty Database**: Select common lab equipment (e.g., volumetric flasks, pipettes, balances) to get typical absolute uncertainties, which can then be used in calculations.
    *   Propagate errors for calculations involving multiple measurements:
        *   Basic operations (addition, subtraction, multiplication, division, powers).
        *   **Complex Functions**: Input a custom mathematical expression, define variables with their values, uncertainties, and **units**. The tool uses SymPy for symbolic differentiation to calculate propagated error. The overall unit for the result can also be specified.
    *   Suggest strategies to minimize identified errors.

*   **Report Generation:**
    *   Compile a complete IA report based on the information entered in previous sections.
    *   Sections include: Title Page, Introduction, Methodology, Results, Conclusion, Evaluation, and References.
    *   **Reference Management**: Input a list of references and select a citation style (APA, MLA, Chicago) to be noted in the report.
    *   **Export Options**:
        *   **PDF**: Generate a formatted PDF report suitable for submission. Includes data tables and embedded plots (from Data Analysis).
        *   **Markdown**: Export the report content as a Markdown (`.md`) file for easy editing or version control.
        *   **JSON (Report Data)**: Download all entered report data as a JSON file, allowing for data backup or external use.

*   **Chemistry Tools:**
    *   **Chemical Equation Balancer**: Input an unbalanced chemical equation (e.g., "H2 + O2 -> H2O") and get the balanced equation using `chempy`.

*   **Save/Load Full Progress:**
    *   **Download Progress**: Save the entire application's current state (all inputs, data, selections across all pages) into a JSON file. This allows users to save their work and resume later.
    *   **Upload Progress**: Load a previously saved progress JSON file to restore the application to that state.

## Getting Started

1.  **Navigate the App**: Use the sidebar on the left to move between the different sections of the IA process (Experiment Planning, Hypothesis Testing, etc.).
2.  **Start with Planning**: It is highly recommended to begin with "Experiment Planning" as information from this section (like variables and methodology) is used to populate subsequent sections.
3.  **Enter Data Sequentially**: Fill in the required information in each section. The tool uses data from earlier steps to provide context and suggestions in later steps.
4.  **Save Your Work**:
    *   Each page typically has a "Save" button (e.g., "Save Experiment Plan", "Save Hypothesis") that confirms the current inputs for that specific section.
    *   Use the "Download Full Progress" feature in the sidebar ("Manage Progress") to save your entire session across all pages. This is crucial for taking breaks and resuming work.
5.  **Generate Your Report**: Once all sections are complete, navigate to "Report Generation" to compile and download your IA report.

## Installation and Usage (Local)

To run this application locally, you need Python and pip installed.

1.  **Clone the repository (if applicable) or download the source files.**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application should open in your web browser.

## Technology Stack

*   **Streamlit**: For creating the interactive web application.
*   **Pandas**: For data manipulation and analysis.
*   **NumPy**: For numerical operations.
*   **Plotly**: For interactive data visualizations.
*   **SciPy**: For statistical tests (e.g., t-tests, ANOVA).
*   **Statsmodels**: For regression analysis.
*   **SymPy**: For symbolic mathematics, particularly error propagation with partial derivatives.
*   **FPDF (fpdf2)**: For generating PDF reports.
*   **ChemPy**: For balancing chemical equations.
*   **Kaleido**: For exporting Plotly figures to static images for PDF inclusion.

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request if you have suggestions for improvement.

## Disclaimer

This tool is intended to guide and assist students with their IB Chemistry Internal Assessment. It does not guarantee a high grade, as the quality of the experimental design, execution, analysis, and critical thinking remains the responsibility of the student. Always consult your teacher for guidance and ensure your work adheres to all IB academic integrity policies.
