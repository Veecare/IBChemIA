import io
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
from fpdf import FPDF
import base64

class ChemistryIAReport(FPDF):
    """Custom PDF class for IB Chemistry IA reports"""
    
    def header(self):
        """Define the header for all pages"""
        # Set font and size
        self.set_font('Arial', 'B', 12)
        # Title
        self.cell(0, 10, 'IB Chemistry HL Internal Assessment', 0, 1, 'C')
        # Line break
        self.ln(5)

    def footer(self):
        """Define the footer for all pages"""
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Set font
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        """Add a chapter title"""
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(220, 220, 220) # Light gray background
        self.cell(0, 10, title, 0, 1, 'L', 1)
        # Line break
        self.ln(5)

    def section_title(self, title):
        """Add a section title"""
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, title, 0, 1, 'L')
        # Line break
        self.ln(3)

    def body_text(self, text):
        """Add body text, handling line breaks"""
        self.set_font('Arial', '', 11)
        
        # Split text into paragraphs based on newlines
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            if paragraph.strip():  # Check if paragraph is not just whitespace
                self.multi_cell(0, 6, paragraph.strip())
                self.ln(3)  # Add small spacing between paragraphs

    def add_table(self, data, headers=None, col_widths=None):
        """Add a table to the report
        
        Parameters:
        -----------
        data : list of lists
            Table data as a list of rows
        headers : list, optional
            Column headers
        col_widths : list, optional
            List of column widths
        """
        self.set_font('Arial', '', 10)
        line_height = 7
        
        # Calculate column widths if not provided
        if col_widths is None:
            col_widths = [self.w / len(data[0])] * len(data[0])
        
        # Add headers if provided
        if headers:
            self.set_font('Arial', 'B', 10)
            for i, header in enumerate(headers):
                self.cell(col_widths[i], line_height, str(header), 1, 0, 'C')
            self.ln(line_height)
            self.set_font('Arial', '', 10)
        
        # Add data
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], line_height, str(cell), 1, 0, 'C')
            self.ln(line_height)
        
        self.ln(5)

    def add_image(self, img_path, w=None, h=None, caption=None):
        """Add an image to the report
        
        Parameters:
        -----------
        img_path : str
            Path to the image file
        w : float, optional
            Width of the image
        h : float, optional
            Height of the image
        caption : str, optional
            Caption for the image
        """
        if w is None:
            w = self.w * 0.8  # 80% of page width
        
        # Center the image horizontally
        x = (self.w - w) / 2
        
        self.image(img_path, x=x, w=w, h=h)
        
        if caption:
            self.set_font('Arial', 'I', 10)
            self.ln(3)
            self.cell(0, 5, caption, 0, 1, 'C')
        
        self.ln(5)

def generate_pdf_report(report_data):
    """
    Generate a PDF report for an IB Chemistry IA
    
    Parameters:
    -----------
    report_data : dict
        Dictionary containing all report data
        
    Returns:
    --------
    pdf_bytes : bytes
        The generated PDF as bytes
    """
    # Create PDF object
    pdf = ChemistryIAReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Cover page
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 20, '', 0, 1)  # Add some space at the top
    pdf.cell(0, 10, report_data["title"], 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Student Name: {report_data["student_name"]}', 0, 1, 'C')
    
    if report_data.get("candidate_number"):
        pdf.cell(0, 10, f'Candidate Number: {report_data["candidate_number"]}', 0, 1, 'C')
    
    if report_data.get("school_name"):
        pdf.cell(0, 10, f'School: {report_data["school_name"]}', 0, 1, 'C')
    
    if report_data.get("teacher_name"):
        pdf.cell(0, 10, f'Teacher: {report_data["teacher_name"]}', 0, 1, 'C')
    
    if report_data.get("experiment_date"):
        pdf.cell(0, 10, f'Date: {report_data["experiment_date"]}', 0, 1, 'C')
    
    pdf.ln(15)
    
    if report_data.get("word_count"):
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, f'Word Count: {report_data["word_count"]} words', 0, 1, 'C')
    
    # Table of Contents page
    pdf.add_page()
    pdf.chapter_title("Table of Contents")
    
    toc_items = [
        "1. Introduction",
        "2. Methodology",
        "   2.1 Materials",
        "   2.2 Variables",
        "   2.3 Procedure",
        "   2.4 Safety Considerations",
        "3. Results and Data Analysis",
        "4. Conclusion",
        "5. Evaluation"
    ]
    
    for item in toc_items:
        pdf.body_text(item)
    
    # Introduction
    pdf.add_page()
    pdf.chapter_title("1. Introduction")
    
    if report_data.get("introduction"):
        pdf.body_text(report_data["introduction"])
    else:
        pdf.body_text("Introduction content not provided.")
    
    # Methodology
    pdf.add_page()
    pdf.chapter_title("2. Methodology")
    
    # Materials
    pdf.section_title("2.1 Materials")
    
    if report_data.get("materials") and len(report_data["materials"]) > 0:
        for material in report_data["materials"]:
            pdf.body_text(f"• {material}")
    else:
        pdf.body_text("Materials list not provided.")
    
    # Variables
    pdf.section_title("2.2 Variables")
    
    if report_data.get("independent_var"):
        pdf.body_text(f"Independent Variable: {report_data['independent_var']}")
    
    if report_data.get("dependent_var"):
        pdf.body_text(f"Dependent Variable: {report_data['dependent_var']}")
    
    if report_data.get("controlled_vars") and len(report_data["controlled_vars"]) > 0:
        pdf.body_text("Controlled Variables:")
        for var in report_data["controlled_vars"]:
            pdf.body_text(f"• {var}")
    
    # Procedure
    pdf.section_title("2.3 Procedure")
    
    if report_data.get("methodology"):
        pdf.body_text(report_data["methodology"])
    else:
        pdf.body_text("Procedure not provided.")
    
    # Safety Considerations
    if report_data.get("safety_considerations"):
        pdf.section_title("2.4 Safety Considerations")
        pdf.body_text(report_data["safety_considerations"])
    
    # Results and Data Analysis
    pdf.add_page()
    pdf.chapter_title("3. Results and Data Analysis")
    
    # Data table
    if report_data.get("data") and isinstance(report_data["data"], dict):
        try:
            df = pd.DataFrame(report_data["data"])
            
            if not df.empty:
                pdf.section_title("3.1 Raw Data")
                
                # Convert DataFrame to list for table
                headers = df.columns.tolist()
                data_rows = df.values.tolist()
                
                # Format data to 3 decimal places if numeric
                formatted_data = []
                for row in data_rows:
                    formatted_row = []
                    for val in row:
                        if isinstance(val, (int, float)):
                            formatted_row.append(f"{val:.3f}")
                        else:
                            formatted_row.append(str(val))
                    formatted_data.append(formatted_row)
                
                # Calculate column widths based on content
                col_widths = []
                for i in range(len(headers)):
                    max_width = len(str(headers[i])) * 2
                    for row in formatted_data:
                        if i < len(row):  # Make sure the index is valid
                            max_width = max(max_width, len(str(row[i])) * 2)
                    col_widths.append(min(max_width, 30))  # Limit to 30 pts
                
                # Adjust widths to fit page
                total_width = sum(col_widths)
                if total_width > pdf.w - 20:  # Ensure it fits within page margins
                    scale_factor = (pdf.w - 20) / total_width
                    col_widths = [w * scale_factor for w in col_widths]
                
                pdf.add_table(formatted_data, headers, col_widths)
        except Exception as e:
            pdf.body_text(f"Error rendering data table: {str(e)}")
    
    # Add a placeholder for data visualization
    pdf.section_title("3.2 Data Visualization")
    pdf.body_text("Graphs and charts from your data analysis are integrated into your report. These visual representations help illustrate the relationships between variables and the trends observed in your experiment.")
    
    # Statistical analysis
    pdf.section_title("3.3 Statistical Analysis")
    
    if report_data.get("hypothesis"):
        pdf.body_text(f"Hypothesis: {report_data['hypothesis']}")
    
    # Create placeholder for statistical results
    pdf.body_text("The statistical analysis results from your experiment are discussed here, including measures of central tendency, dispersion, and any hypothesis tests performed.")
    
    # Error analysis
    pdf.section_title("3.4 Error Analysis")
    
    # Add random and systematic errors if available
    if report_data.get("random_errors") and len(report_data["random_errors"]) > 0:
        pdf.body_text("Random Errors:")
        for error in report_data["random_errors"]:
            pdf.body_text(f"• {error}")
    
    if report_data.get("systematic_errors") and len(report_data["systematic_errors"]) > 0:
        pdf.body_text("Systematic Errors:")
        for error in report_data["systematic_errors"]:
            pdf.body_text(f"• {error}")
    
    # Conclusion
    pdf.add_page()
    pdf.chapter_title("4. Conclusion")
    
    if report_data.get("conclusion"):
        pdf.body_text(report_data["conclusion"])
    else:
        pdf.body_text("Conclusion not provided.")
    
    # Evaluation
    pdf.add_page()
    pdf.chapter_title("5. Evaluation")
    
    if report_data.get("evaluation"):
        pdf.body_text(report_data["evaluation"])
    else:
        pdf.body_text("Evaluation not provided.")
    
    # Get the PDF as bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    
    return pdf_bytes


def generate_matplotlib_figure(df, x_col, y_col, add_trendline=False):
    """
    Generate a Matplotlib figure for inclusion in the PDF
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the data
    x_col : str
        Column name for x-axis
    y_col : str
        Column name for y-axis
    add_trendline : bool
        Whether to add a trendline to the plot
        
    Returns:
    --------
    fig_bytes : bytes
        The figure as bytes in PNG format
    """
    # Create figure
    plt.figure(figsize=(8, 6))
    
    # Create scatter plot
    plt.scatter(df[x_col], df[y_col], color='blue')
    
    # Add labels and title
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{y_col} vs {x_col}")
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Add trendline if requested
    if add_trendline:
        # Calculate linear regression
        x = df[x_col].values
        y = df[y_col].values
        
        m, b = np.polyfit(x, y, 1)
        plt.plot(x, m*x + b, color='red', linestyle='--')
        
        # Add equation and R^2
        correlation = np.corrcoef(x, y)[0, 1]
        r_squared = correlation**2
        
        equation = f"y = {m:.4f}x + {b:.4f}"
        plt.text(0.05, 0.95, f"{equation}\nR² = {r_squared:.4f}", 
                 transform=plt.gca().transAxes, 
                 verticalalignment='top', 
                 bbox=dict(facecolor='white', alpha=0.8))
    
    # Save figure to bytes buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    
    # Close the figure to free memory
    plt.close()
    
    return buf.getvalue()
