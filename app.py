import dash
from dash import html

app = dash.Dash(__name__)
app.layout = html.Div("Dash App Setup Complete")

if __name__ == "__main__":
    app.run(debug=True)
