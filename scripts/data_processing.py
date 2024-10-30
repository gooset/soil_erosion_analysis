import pandas as pd
import geopandas as gpd

def load_data(data_path, coords_path):
    """
    Load and merge the main dataset with geographic coordinates.
    
    Parameters:
    -----------
    data_path : str
        Path to the main data file.
    coords_path : str
        Path to the coordinates file.

    Returns:
    --------
    pd.DataFrame
        Merged DataFrame with all relevant columns.
    """
    df = pd.read_csv(data_path)
    coords_df = pd.read_csv(coords_path)
    coords_df = coords_df.rename(columns={"Country": "Area"})
    
    # Merge on Area
    data = df.merge(coords_df, on="Area", how="left")
    return data

def clean_data(df):
    """
    Clean the DataFrame by handling missing values, data types, and basic imputation.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The raw data frame.

    Returns:
    --------
    pd.DataFrame
        Cleaned data frame.
    """
    # Drop irrelevant columns and rows with missing key values
    df.dropna(subset=['Latitude', 'Longitude', 'population', 'yield(tonnes)'], inplace=True)
    df['yield(tonnes)'] = pd.to_numeric(df['yield(tonnes)'], errors='coerce')
    return df
