from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from utils.data_processing import load_and_process_data

# Load and prepare data
df = load_and_process_data("data")
df["date"] = pd.to_datetime(df["date"])

# Group sales per region, resampled by MONTH to reduce noise
df_grouped = (
    df.groupby(["region", "date"], as_index=False)["sales"].sum()
    .set_index("date")
    .groupby("region")["sales"]
    .resample("M")
    .sum()
    .reset_index()
)

# Define price change date
price_change = pd.Timestamp("2021-01-15")

# Total sales before and after price change
before_sales = df_grouped[df_grouped["date"] < price_change]["sales"].sum()
after_sales = df_grouped[df_grouped["date"] >= price_change]["sales"].sum()
result_text = (
    f"Total sales BEFORE {price_change.date()}: ${before_sales:,.2f}  |  "
    f"AFTER: ${after_sales:,.2f}  |  "
    f"{'After' if after_sales > before_sales else 'Before'} had higher sales"
)

# Colors.
colors = {'background': '#111111', 'text': '#7FDBFF'}

# Create line chart.
fig = px.line(
    df_grouped,
    x="date",
    y="sales",
    color="region",
    line_group="region",
    markers=False,
    title="Pink Morsel Sales by Date and Region (Monthly Aggregated)",
    labels={"date": "Date", "sales": "Sales ($)", "region": "Region"}
)

# Add vertical price change marker.
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    xaxis_title="Date",
    yaxis_title="Total Sales ($)",
    shapes=[
        dict(
            type="line",
            x0=price_change,
            x1=price_change,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(color="red", width=2, dash="dash")
        )
    ],
    annotations=[
        dict(
            x=price_change,
            y=1,
            xref="x",
            yref="paper",
            showarrow=False,
            xanchor="left",
            text="Price Increase",
            font=dict(color="red", size=12)
        )
    ]
)

# Build Dash App.
app = Dash(__name__)
app.title = "Soul Foods - Pink Morsel Sales"

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1("Pink Morsel Sales Over Time", style={'textAlign': 'center', 'color': colors['text']}),

    html.Div("Visualizing the impact of the Jan 15, 2021 price increase",
             style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': '10px'}),

    html.Div(result_text,
             style={'textAlign': 'center', 'color': colors['text'], 'fontSize': '18px', 'marginBottom': '20px'}),

    dcc.Graph(id="sales-line-chart", figure=fig, config={'responsive': True})
])

if __name__ == "__main__":
    app.run(debug=True)
    