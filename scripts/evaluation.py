from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def evaluate_model(model, scaler, X_test, y_test):
    """
    Evaluate the model's performance.

    Parameters:
    -----------
    model : Trained model
    scaler : StandardScaler
    X_test : pd.DataFrame
        Test features.
    y_test : pd.Series
        Test target.

    Returns:
    --------
    dict
        Dictionary with evaluation metrics.
    """
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    
    metrics = {
        'R2 Score': r2_score(y_test, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred))
    }
    return metrics
