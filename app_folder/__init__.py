from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from utils.data_processing import load_and_process_data

# Load and prepare data
df = load_and_process_data("data")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")
df_grouped = (
    df.groupby(["region", "date"], as_index=False)["sales"].sum()
    .set_index("date")
    .groupby("region")["sales"]
    .resample("ME")
    .sum()
    .reset_index()
)

# Price change date
price_change = pd.Timestamp("2021-01-15")

# App setup
app = Dash(__name__)
app.title = "Soul Foods - Pink Morsel Sales"

# Styles
colors = {'background': '#111111', 'text': '#7FDBFF', 'card_bg': '#1E1E1E'}
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px', 'font-family': 'Arial'}, children=[
    html.H1("Pink Morsel Sales Dashboard", style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': '10px'}),
    html.P("Use the region selector below to filter the line chart. All = all regions.", style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': '30px'}),
    
    html.Div([
        dcc.RadioItems(
            id='region-selector',
            options=[{'label': r.title(), 'value': r} for r in ['all', 'north', 'east', 'south', 'west']],
            value='all',
            inline=True,
            inputStyle={'marginRight': '5px'},
            labelStyle={'color': colors['text'], 'marginRight': '15px'}
        ),
    ], style={'textAlign': 'center', 'backgroundColor': colors['card_bg'], 'padding': '10px', 'borderRadius': '5px', 'display': 'inline-block'}),
    
    html.Div(id='summary', style={'textAlign': 'center', 'color': colors['text'], 'fontSize': '18px', 'margin': '20px 0'}),
    
    dcc.Graph(id='sales-line-chart', config={'responsive': True})
])

# Callback for interactivity
@app.callback(
    [Output('sales-line-chart', 'figure'), Output('summary', 'children')],
    [Input('region-selector', 'value')]
)
def update_chart(region):
    # Filter data
    dff = df_grouped[df_grouped['region'] == region] if region != 'all' else df_grouped
    
    # Summaries
    before = dff[dff['date'] < price_change]['sales'].sum()
    after = dff[dff['date'] >= price_change]['sales'].sum()
    summary = f" Total sales BEFORE 2021-01-15: ${before:,.2f} • AFTER: ${after:,.2f} • {' After' if after > before else ' Before'} had higher sales"
    
    # Line chart
    fig = px.line(
        dff,
        x='date',
        y='sales',
        color='region' if region == 'all' else None,
        line_group='region',
        markers=False,
        title=f"Pink Morsel Sales by Date{' — ' + region.title() if region != 'all' else ''}",
        labels={'date':'Date', 'sales':'Sales ($)', 'region':'Region'}
    )
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        shapes=[{
            "type": "line",
            "x0": price_change,
            "x1": price_change,
            "y0": 0,
            "y1": 1,
            "xref": "x",
            "yref": "paper",
            "line": {"color": "red", "width": 2, "dash": "dash"}
        }],
        annotations=[{
            "x": price_change,
            "y": 1,
            "xref": "x",
            "yref": "paper",
            "showarrow": False,
            "xanchor": "left",
            "text": " Price Increase",
            "font": {"color": "red", "size": 12}
        }]
    )
    return fig, summary

if __name__ == '__main__':
    app.run(debug=True)
