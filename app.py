import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from utils.data_processing import load_and_process_data

# Load the processed data
df = load_and_process_data("data")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Group by region and date to get daily totals.
df_grouped = df.groupby(["region", "date"], as_index=False)["sales"].sum()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Soul Foods - Pink Morsel Sales"

# Layout with Line Chart
app.layout = html.Div(children=[
    html.H1("Pink Morsel Sales Over Time", style={"textAlign": "center"}),

    dcc.Graph(
        id='sales-line-chart',
        figure=px.line(
            df_grouped,
            x="date",
            y="sales",
            color="region",
            title="Pink Morsel Sales by Date and Region",
            labels={"date": "Date", "sales": "Sales ($)", "region": "Region"}
        ).update_layout(
            xaxis=dict(title='Date'),
            yaxis=dict(title='Total Sales ($)'),
            shapes=[
                dict(
                    type='line',
                    x0='2021-01-15', x1='2021-01-15',
                    y0=0, y1=1,
                    xref='x', yref='paper',
                    line=dict(color='red', width=2, dash='dash')
                )
            ],
            annotations=[
                dict(
                    x='2021-01-15',
                    y=1,
                    xref='x',
                    yref='paper',
                    showarrow=False,
                    xanchor='left',
                    text="Price Increase",
                    font=dict(color="red", size=12)
                )
            ]
        )
    )
])

if __name__ == "__main__":
    app.run(debug=True)
    