import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

# Load the dataset
file_path = 'updated_merged_data.json'  # Ensure this file exists in the same directory as app.py
merged_data = pd.read_json(file_path)

# Assign distinct region colors for the figure
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
server = app.server  # Expose the Flask server instance for Render

# Create the interactive figure
def create_figure(region_colors):
    fig = go.Figure()

    # Add traces for each region
    for region, color in region_colors.items():
        region_data = merged_data[merged_data["Cultural_Region"] == region]

        # Survey data
        fig.add_trace(go.Scatter(
            x=region_data["Survival_vs_SelfExpression_Survey"],
            y=region_data["Traditional_vs_Secular_Survey"],
            mode="markers",
            hovertext=region_data["Country"],
            name=f"Survey - {region}",
            marker=dict(size=8, color=color),
            hoverinfo="text"
        ))

        # ChatGPT data
        fig.add_trace(go.Scatter(
            x=region_data["Survival_vs_SelfExpression_ChatGPT"],
            y=region_data["Traditional_vs_Secular_ChatGPT"],
            mode="markers",
            hovertext=region_data["Country"],
            name=f"ChatGPT - {region}",
            marker=dict(size=8, color=color, symbol="circle-open"),
            hoverinfo="text"
        ))

    # Add dropdown menu for interactive filtering
    buttons = [
        dict(label="Select All", method="update", args=[{"visible": [True] * len(fig.data)}, {"title": "All Regions"}]),
        dict(label="Unselect All", method="update", args=[{"visible": [False] * len(fig.data)}, {"title": "No Data Visible"}])
    ]

    for region, color in region_colors.items():
        visibility = [trace.name.endswith(region) for trace in fig.data]
        buttons.append(dict(
            label=f"Focus on {region}",
            method="update",
            args=[{"visible": visibility}, {"title": f"Cultural Indices ({region})"}]
        ))

    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                showactive=True,
                buttons=buttons,
                x=1.6,  # Positioned to the right of the legend
                xanchor="right",
                y=1,
                yanchor="top"
            )
        ],
        title="Cultural Values Comparison: Survey vs ChatGPT",
        xaxis_title="Survival vs. Self-Expression",
        yaxis_title="Traditional vs. Secular",
        legend=dict(x=1.3, y=1, xanchor="right", yanchor="top"),
        template="plotly_white",
        height=800,
        width=1400,
        hovermode="closest"
    )

    return fig

# App Layout
app.layout = html.Div(
    id="main-container",
    style={
        'background-color': '#2d00f7',  # Background color of the app
        'color': '#ffffff',
        'padding': '30px',
        'min-height': '100vh',
    },
    children=[
        # Title Section
        html.H1(
            "Cultural Values Comparison: Survey vs ChatGPT",
            style={
                'text-align': 'center',
                'font-family': 'Arial, sans-serif',
                'margin-bottom': '20px',
                'padding': '10px',
                'border-radius': '10px',
                'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.5)',  # Shadow for 3D effect
                'background-color': '#2d00f7',  # Updated title color
                'color': '#ffffff',  # White text for title
            }
        ),

        # Description Section
        html.Div(
            children=[
                html.P(
                    "This dashboard compares cultural indices derived from two sources:",
                    style={'font-size': '16px', 'font-weight': 'bold'}
                ),
                html.Ul([
                    html.Li("Original survey data by Haerpfer et al.(2022)."),
                    html.Li("ChatGPT's responses when prompted to simulate an average individual in a country/region.")
                ]),
                html.P(
                    "Key details about the figure:",
                    style={'font-size': '16px', 'font-weight': 'bold'}
                ),
                html.Ul([
                    html.Li("Data covers 107 countries/territories that belong to 8 regions as in Inglehart R. (2005)."),
                    html.Li("X-axis: Survival values (negative) to self-expression values (positive)."),
                    html.Li("Y-axis: Traditional values (negative) to secular values (positive)."),
                    html.Li("Values are normalized z-scores."),
                    html.Li("Users can filter by region, country, or data source (Survey/ChatGPT).")
                ])
            ],
            style={
                'margin': '20px auto',
                'max-width': '900px',
                'background-color': '#ffffff',  # Updated to #6a00f4 for description
                'padding': '20px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'font-family': 'Arial, sans-serif',
                'color': '#2d00f7',  # White text
            }
        ),

        # Loading and Graph Section
        html.Div(
            children=[
                dcc.Loading(
                    id="loading-1",
                    type="circle",
                    children=[
                        html.Div(id="countdown", style={'text-align': 'center', 'margin': '20px'}),
                        dcc.Interval(id='interval-countdown', interval=1000, n_intervals=0, max_intervals=5),
                    ]
                ),
                html.Div(
                    dcc.Graph(id='main-graph', figure=create_figure(region_colors)),
                    style={
                        'box-shadow': '0 8px 16px rgba(0, 0, 0, 0.5)',  # Shadow for 3D effect
                        'border-radius': '10px',
                    }
                ),
            ],
            style={
                'margin-top': '30px',
                'padding': '20px',
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)'
            }
        ),

        # References Section
        html.Div(
            children=[
                html.H3("References", style={'text-align': 'left', 'font-weight': 'bold'}),
                html.Ul([
                    html.Li(
                        [
                            "Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., "
                            "M. Lagos, P. Norris, E. Ponarin & B. Puranen (eds.). 2022. World Values Survey: Round Seven - "
                            "Country-Pooled Datafile Version 5.0. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA "
                            "Secretariat. DOI: 10.14281/18241.24"
                        ]
                    ),
                    html.Li(
                        "Inglehart R., Welzel C. (2005). Modernization, cultural change, and democracy: the human development "
                        "sequence. Vol. 333. Cambridge University Press."
                    )
                ])
            ],
            style={
                'margin-top': '20px',
                'padding': '10px',
                'background-color': '#2d00f7',  # Updated to #6a00f4 for references
                'border-radius': '10px',
                'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                'font-family': 'Arial, sans-serif',
                'color': '#ffffff',  # White text
            }
        )
    ]
)

# Countdown Callback
@app.callback(
    Output('countdown', 'children'),
    Input('interval-countdown', 'n_intervals')
)
def update_countdown(n_intervals):
    countdown_value = 5 - n_intervals
    if countdown_value > 0:
        return f"Loading data... {countdown_value} seconds remaining."
    return html.Span([
        "Loading complete. Rendering graph... ",
        html.Span("\u23F3", style={'margin-left': '5px', 'font-size': '16px'})  # Clock icon
    ])

# Run the app locally
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8080)
