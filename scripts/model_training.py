from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd

def train_model(df, target_column='yield(tonnes)', test_size=0.2, random_state=42):
    """
    Train a model for predicting soil erosion risk.

    Parameters:
    -----------
    df : pd.DataFrame
        The data frame with features and target.
    target_column : str
        The target variable to predict.
    test_size : float
        Split ratio for train/test.
    random_state : int
        Seed for reproducibility.

    Returns:
    --------
    model : Trained model
    scaler : Feature scaler
    """
    feature_columns = ['Latitude', 'Longitude', 'population_density', 'yield_per_capita']
    X = df[feature_columns]
    y = df[target_column]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model training
    model = RandomForestRegressor(n_estimators=100, random_state=random_state)
    model.fit(X_train_scaled, y_train)
    
    # Save model and scaler
    joblib.dump(model, './models/soil_erosion_model.pkl')
    joblib.dump(scaler, './models/scaler.pkl')
    
    return model, scaler
