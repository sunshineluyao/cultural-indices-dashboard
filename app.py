import dash
from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd

# Load the dataset
file_path = 'updated_merged_data.csv'  # Ensure this file exists in the same directory as app.py
merged_data = pd.read_csv(file_path)

# Assign distinct colors for each region
region_colors = {
    'African-Islamic': 'blue',
    'Confucian': 'orange',
    'Latin America': 'green',
    'Catholic Europe': 'red',
    'English-Speaking': 'purple',
    'Orthodox Europe': 'brown',
    'Protestant Europe': 'cyan',
    'West & South Asia': 'pink'
}

# Create Dash app
app = dash.Dash(__name__)
server = app.server  # Expose the Flask server instance for Gunicorn

# Create Plotly figure
optimized_fig = go.Figure()

for region, color in region_colors.items():
    region_data = merged_data[merged_data["Cultural_Region"] == region]

    # Add Survey data
    optimized_fig.add_trace(go.Scatter(
        x=region_data["Survival_vs_SelfExpression_Survey"],
        y=region_data["Traditional_vs_Secular_Survey"],
        mode="markers",
        hovertext=region_data["Country"],
        name=f"Survey - {region}",
        marker=dict(size=8, color=color),
        hoverinfo="text"
    ))

    # Add ChatGPT data
    optimized_fig.add_trace(go.Scatter(
        x=region_data["Survival_vs_SelfExpression_ChatGPT"],
        y=region_data["Traditional_vs_Secular_ChatGPT"],
        mode="markers",
        hovertext=region_data["Country"],
        name=f"ChatGPT - {region}",
        marker=dict(size=8, color=color, symbol="circle-open"),
        hoverinfo="text"
    ))

# Add dropdown menu for interactivity
buttons = [
    dict(label="Select All", method="update", args=[{"visible": [True] * len(optimized_fig.data)}, {"title": "All Regions"}]),
    dict(label="Unselect All", method="update", args=[{"visible": [False] * len(optimized_fig.data)}, {"title": "No Data Visible"}])
]

for region, color in region_colors.items():
    visibility = [trace.name.endswith(region) for trace in optimized_fig.data]
    buttons.append(dict(
        label=f"Focus on {region}",
        method="update",
        args=[{"visible": visibility}, {"title": f"Cultural Indices ({region})"}]
    ))

# Update figure layout
optimized_fig.update_layout(
    updatemenus=[
        dict(
            type="dropdown",
            showactive=True,
            buttons=buttons,
            x=0.1,
            xanchor="left",
            y=1.2,
            yanchor="top"
        )
    ],
    title="Cultural Indices Comparison (Survey vs ChatGPT)",
    xaxis_title="Survival vs. Self-Expression",
    yaxis_title="Traditional vs. Secular",
    legend_title="Region and Dataset",
    template="plotly_white",
    height=900,
    width=1600,
    hovermode="closest"
)

# Define the app layout
app.layout = html.Div([
    html.H1("Cultural Indices Dashboard"),
    dcc.Graph(figure=optimized_fig)
])

# Run the app locally
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8080)
