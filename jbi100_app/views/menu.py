from dash import dcc, html
from ..config import color_list1, color_list2


def generate_description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Visualisation Project Group 37"),
            html.Div(
                id="intro",
                children="This Dashboard helps coaches and players of the upcoming World Cup 2026.",
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Choose visualisation:"),
            dcc.Dropdown(
                id='menu-dropdown',
                options=[
                    {'label': 'Penalty Shootouts', 'value': 'penalty'},
                    {'label': 'Teams Formation', 'value': 'formation'}
                ],
                value='penalty'  # Set a default value if needed
            ),
        ], style={"textAlign": "float-left"}
    )

def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
