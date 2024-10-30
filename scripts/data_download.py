# data_download.py

import requests
import pandas as pd
import wbdata
from zipfile import ZipFile
from pathlib import Path
from datetime import datetime

# Create data directories
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# FAO data URL
FAO_URL = 'http://fenixservices.fao.org/faostat/static/bulkdownloads/datasets_E.json'

# World Bank indicators
WB_INDICATORS = {
    'population': 'SP.POP.TOTL',      # Population, total
    'rainfall': 'AG.LND.PRCP.MM',     # Average precipitation (mm per year)
    'agland': 'AG.LND.AGRI.K2'        # Agricultural land (sq. km)
}

def download_and_extract_fao(dataset_index, filename):
    """Download and extract FAO dataset."""
    try:
        response = requests.get(FAO_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        file_location = data['Datasets']['Dataset'][dataset_index]['FileLocation']
        
        # Download the zip file
        zip_response = requests.get(file_location)
        zip_response.raise_for_status()
        zip_path = RAW_DIR / f"{filename}.zip"
        
        with open(zip_path, 'wb') as f:
            f.write(zip_response.content)

        # Extract the zip file
        with ZipFile(zip_path, 'r') as zip_obj:
            zip_obj.extractall(RAW_DIR)

        # Find the extracted CSV file
        csv_filename = next((file for file in zip_obj.namelist() if file.endswith('.csv')), None)
        
        if csv_filename is None:
            raise FileNotFoundError("No CSV file found in the extracted contents.")
        
        # Read and return the CSV with proper options
        csv_path = RAW_DIR / csv_filename
        return pd.read_csv(csv_path, encoding='latin1', low_memory=False)
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error downloading data: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing FAO data: {str(e)}")


def get_world_bank_data():
    """Collect World Bank data using wbdata package."""
    try:
        dfs = {}
        
        for name, indicator in WB_INDICATORS.items():
            print(f"Fetching {name} data...")
            data = wbdata.get_dataframe({indicator: name}, 
                                      date=(datetime(1960, 1, 1), datetime(2023, 1, 1)))
            dfs[name] = data
        
        if not dfs:
            raise Exception("No data retrieved from World Bank")
            
        df_combined = pd.concat(dfs.values(), axis=1)
        df_combined = df_combined.loc[:, ~df_combined.columns.duplicated()]
        df_combined = df_combined.reset_index().rename(columns={'country': 'Area', 'date': 'Year'})
        df_combined['Year'] = pd.to_datetime(df_combined['Year']).dt.year
        
        # Save raw data
        df_combined.to_csv(RAW_DIR / "world_bank_raw.csv", index=False)
        
        return df_combined
        
    except Exception as e:
        raise Exception(f"Error fetching World Bank data: {str(e)}")


def process_crop_yield(df):
    """Process crop yield data."""
    try:
        crops = ['Rice, paddy', 'Potatoes', 'Yams', 'Soybeans', 
                'Wheat', 'Maize', 'Sorghum', 'Cassava']
        
        df = df.loc[df["Item"].isin(crops)].copy()
        df = df.drop(['Area Code', 'Item Code', 'Element Code', 'Year Code', 
                     'Flag', 'Element', 'Unit'], axis=1, errors='ignore')
        df = df.rename(columns={'Value': 'yield(tonnes)'})
        
        # Save processed data
        df.to_csv(PROCESSED_DIR / "crop_yield_processed.csv", index=False)
        return df
        
    except Exception as e:
        raise Exception(f"Error processing crop yield data: {str(e)}")


def process_pest_data(df):
    """Process pesticide and fertilizer data."""
    try:
        df = df.drop(['Area Code', 'Item Code', 'Element Code', 'Year Code', 
                     'Flag', 'Element', 'Unit'], axis=1, errors='ignore')
        df = df.groupby(['Area', 'Year'])['Value'].sum().reset_index()
        df = df.rename(columns={'Value': 'pestUse(kg/ha)'})
        
        # Save processed data
        df.to_csv(PROCESSED_DIR / "pesticide_processed.csv", index=False)
        return df
        
    except Exception as e:
        raise Exception(f"Error processing pesticide data: {str(e)}")


def process_temp_data(df):
    """Process temperature data."""
    try:
        df = df.drop(['Area Code', 'Element Code', 'Year Code', 'Flag', 
                     'Element', 'Unit'], axis=1, errors='ignore')
        df = df.groupby(['Area', 'Year'])['Value'].sum().reset_index()
        df['Value'] = df['Value'] / 12  # Convert to monthly average
        df = df.rename(columns={'Value': 'tempChange(C)'})
        
        # Save processed data
        df.to_csv(PROCESSED_DIR / "temperature_processed.csv", index=False)
        return df
        
    except Exception as e:
        raise Exception(f"Error processing temperature data: {str(e)}")


def merge_datasets(df_yield, df_pest, df_temp, df_world_bank):
    """Merge all datasets into a single DataFrame."""
    try:
        merged = df_yield.merge(df_pest, on=['Area', 'Year'], how='outer')
        merged = merged.merge(df_temp, on=['Area', 'Year'], how='outer')
        merged = merged.merge(df_world_bank, on=['Area', 'Year'], how='outer')
        
        # Save merged dataset
        merged.to_csv(PROCESSED_DIR / "merged_data.csv", index=False)
        
        return merged
    
    except Exception as e:
        raise Exception(f"Error merging datasets: {str(e)}")
