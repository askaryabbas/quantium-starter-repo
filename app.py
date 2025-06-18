import dash
from dash import html, dcc
import plotly.express as px
from utils.data_processing import load_and_process_data

app = dash.Dash(__name__)
df = load_and_process_data("data")  # Processed data

app.layout = html.Div([
    html.H1("Soul Foods Sales Dashboard"),
    html.P("Showing Pink Morsel Sales Data"),
    dcc.Graph(
        figure=px.line(df, x="date", y="sales", color="region", title="Sales Over Time by Region")
    )
])

if __name__ == "__main__":
    app.run(debug=True)
    