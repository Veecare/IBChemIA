import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

def perform_t_test(sample1, sample2):
    """
    Perform a two-sample t-test on the given samples.
    
    Parameters:
    -----------
    sample1 : array-like
        First sample of measurements
    sample2 : array-like
        Second sample of measurements
        
    Returns:
    --------
    result : scipy.stats._stats_py.Ttest_indResult
        The complete t-test result object
    p_value : float
        The p-value of the test
    """
    result = stats.ttest_ind(sample1, sample2, equal_var=False)
    return result, result.pvalue

def perform_anova(df, columns):
    """
    Perform a one-way ANOVA on the given columns of a dataframe.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    columns : list
        List of column names to include in the ANOVA
        
    Returns:
    --------
    result : pandas.DataFrame
        ANOVA table as a dataframe
    p_value : float
        The p-value of the ANOVA test
    """
    # Prepare data for ANOVA
    data = []
    for col in columns:
        data.append(df[col])
    
    # Perform ANOVA
    f_statistic, p_value = stats.f_oneway(*data)
    
    # Create ANOVA table
    ss_between = sum(len(x) * (np.mean(x) - np.mean(np.concatenate(data)))**2 for x in data)
    df_between = len(columns) - 1
    
    ss_within = sum(sum((x - np.mean(x))**2) for x in data)
    df_within = sum(len(x) for x in data) - len(columns)
    
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    
    f_statistic = ms_between / ms_within
    
    # Create the ANOVA table as a pandas DataFrame
    anova_table = pd.DataFrame({
        'Sum of Squares': [ss_between, ss_within, ss_between + ss_within],
        'df': [df_between, df_within, df_between + df_within],
        'Mean Square': [ms_between, ms_within, None],
        'F': [f_statistic, None, None],
        'p-value': [p_value, None, None]
    }, index=['Between Groups', 'Within Groups', 'Total'])
    
    return anova_table, p_value

def calculate_correlation(df, corr_type='pearson'):
    """
    Calculate correlation matrix and p-values for the given dataframe.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    corr_type : str
        Type of correlation to calculate ('pearson' or 'spearman')
        
    Returns:
    --------
    corr_matrix : pandas.DataFrame
        Correlation matrix
    p_matrix : pandas.DataFrame
        Matrix of p-values corresponding to correlations
    """
    # Calculate correlation matrix
    if corr_type.lower() == 'pearson':
        corr_matrix = df.corr(method='pearson')
        corr_func = stats.pearsonr
    else:
        corr_matrix = df.corr(method='spearman')
        corr_func = stats.spearmanr
    
    # Calculate p-values
    p_matrix = pd.DataFrame(np.zeros_like(corr_matrix), index=corr_matrix.index, columns=corr_matrix.columns)
    
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            if i != j:  # Skip diagonal (self-correlations)
                x = df.iloc[:, i]
                y = df.iloc[:, j]
                
                if corr_type.lower() == 'pearson':
                    _, p_value = corr_func(x, y)
                else:
                    # For spearman, we need to handle the return type differently
                    result = corr_func(x, y)
                    if hasattr(result, 'pvalue'):
                        p_value = result.pvalue
                    else:
                        _, p_value = result
                
                p_matrix.iloc[i, j] = p_value
            else:
                p_matrix.iloc[i, j] = 0.0  # Self-correlation has p=0
    
    return corr_matrix, p_matrix

def calculate_regression(df, y_var, x_vars):
    """
    Perform linear regression analysis.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Dataframe containing the data
    y_var : str
        Name of the dependent variable
    x_vars : list
        List of names of independent variables
        
    Returns:
    --------
    result : statsmodels.regression.linear_model.RegressionResults
        The complete regression results object
    """
    # Create the formula for regression
    formula = f"{y_var} ~ {' + '.join(x_vars)}"
    
    # Fit the model
    model = ols(formula, data=df).fit()
    
    return model
