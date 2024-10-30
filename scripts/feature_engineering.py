import pandas as pd

def engineer_features(df):
    """
    Engineer new features for model training.

    Parameters:
    -----------
    df : pd.DataFrame
        The cleaned data frame.

    Returns:
    --------
    pd.DataFrame
        DataFrame with additional engineered features.
    """
    df['population_density'] = df['population'] / df['agland']
    df['yield_per_capita'] = df['yield(tonnes)'] / df['population']
    
    # Seasonal or climatic features
    if 'Year' in df.columns:
        df['decade'] = (df['Year'] // 10) * 10
    
    # Climate zone categorization based on latitude
    df['climate_zone'] = pd.cut(
        df['Latitude'].abs(),
        bins=[0, 23.5, 45, 66.5, 90],
        labels=['Tropical', 'Subtropical', 'Temperate', 'Polar']
    )
    return df
