import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats

def create_scatter_plot(df, x_col, y_col):
    """
    Create a scatter plot with the given data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    x_col : str
        Name of the column to use for x-axis
    y_col : str
        Name of the column to use for y-axis
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        The generated scatter plot
    """
    fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    return fig

def create_bar_chart(df, x_col, y_col):
    """
    Create a bar chart with the given data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    x_col : str
        Name of the column to use for x-axis
    y_col : str
        Name of the column to use for y-axis
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        The generated bar chart
    """
    fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
    return fig

def create_box_plot(df, x_col, y_col):
    """
    Create a box plot with the given data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    x_col : str
        Name of the column to use for categories (x-axis)
    y_col : str
        Name of the column to use for values (y-axis)
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        The generated box plot
    """
    fig = px.box(df, x=x_col, y=y_col, title=f"Distribution of {y_col} by {x_col}")
    return fig

def create_line_plot(df, x_col, y_col):
    """
    Create a line plot with the given data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    x_col : str
        Name of the column to use for x-axis
    y_col : str
        Name of the column to use for y-axis
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        The generated line plot
    """
    fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}", markers=True)
    return fig

def create_histogram(df, col, bins=None):
    """
    Create a histogram with the given data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    col : str
        Name of the column to visualize
    bins : int, optional
        Number of bins for the histogram
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        The generated histogram
    """
    fig = px.histogram(df, x=col, nbins=bins, title=f"Distribution of {col}")
    return fig

def create_regression_plot(df, x_col, y_col):
    """
    Create a scatter plot with regression line.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    x_col : str
        Name of the column to use for x-axis
    y_col : str
        Name of the column to use for y-axis
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        The generated scatter plot with regression line
    """
    # Create scatter plot with regression line
    fig = px.scatter(df, x=x_col, y=y_col, trendline="ols", title=f"{y_col} vs {x_col}")
    
    # Calculate regression statistics
    x = df[x_col].values
    y = df[y_col].values
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Add regression equation and R² to the plot
    equation = f"y = {slope:.4f}x + {intercept:.4f}"
    r_squared = f"R² = {r_value**2:.4f}"
    p_val_text = f"p-value = {p_value:.4g}"
    
    annotation_text = f"{equation}<br>{r_squared}<br>{p_val_text}"
    
    fig.add_annotation(
        x=max(x) * 0.8,
        y=min(y) * 1.2,
        text=annotation_text,
        showarrow=False,
        bgcolor="rgba(255, 255, 255, 0.8)"
    )
    
    return fig

def create_residual_plot(df, x_col, y_col):
    """
    Create a residual plot for regression analysis.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    x_col : str
        Name of the column used as independent variable
    y_col : str
        Name of the column used as dependent variable
        
    Returns:
    --------
    fig : plotly.graph_objects.Figure
        The generated residual plot
    """
    # Calculate regression
    x = df[x_col].values
    y = df[y_col].values
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    # Calculate predicted values and residuals
    y_pred = slope * x + intercept
    residuals = y - y_pred
    
    # Create residual plot
    residual_df = pd.DataFrame({
        'Independent Variable': x,
        'Residuals': residuals
    })
    
    fig = px.scatter(residual_df, x='Independent Variable', y='Residuals', 
                   title=f"Residual Plot for {y_col} vs {x_col}")
    
    # Add horizontal line at y=0
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    
    return fig
