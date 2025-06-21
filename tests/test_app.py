import pytest
from dash.testing.application_runners import import_app


@pytest.fixture
def dash_app():
    app = import_app("app_folder")  # imports app.py
    return app


def test_header_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    assert dash_duo.find_element("h1").text == "Pink Morsel Sales Dashboard"


def test_graph_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    graph = dash_duo.find_element("#sales-line-chart")
    assert graph is not None


def test_region_picker_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    radio = dash_duo.find_element("#region-selector")
    assert radio is not None
