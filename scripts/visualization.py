import plotly.express as px
import plotly.graph_objects as go

def plot_geographic_distribution(df):
    """
    Create a scatter plot for geographic distribution of yield.

    Parameters:
    -----------
    df : pd.DataFrame
        Data frame with 'Latitude', 'Longitude', and 'yield(tonnes)' columns.
    """
    fig = px.scatter_geo(
        df,
        lat='Latitude', lon='Longitude',
        color='yield(tonnes)',
        hover_name='Area',
        title='Geographic Distribution of Yield'
    )
    fig.show()

def plot_feature_importance(feature_importances):
    """
    Plot feature importance from model.

    Parameters:
    -----------
    feature_importances : pd.DataFrame
        DataFrame with features and importance values.
    """
    fig = go.Figure(
        go.Bar(
            x=feature_importances['importance'],
            y=feature_importances['feature'],
            orientation='h'
        )
    )
    fig.update_layout(title='Feature Importance')
    fig.show()
