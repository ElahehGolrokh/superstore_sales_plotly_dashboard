from typing import Any, Dict, Hashable, List

from dash import dash_table, dcc, html


def create_dropdown(options: List,
                    label: str,
                    id_prefix: str,) -> html.Div:
    """Creates a good-looking dropdown

    Args:
        options: drop-down's options
        label: drop-down's label
        id_prefix: will be used in drop-down's id -> id of the drop-down
        component will be {id_prefix}-dropdown

    Returns:
        html.Div to put in the ``app.layout``
    """
    return html.Div(
        children=[
            html.Label(
                label,
                id=f"{id_prefix}-label",
            ),
            dcc.Dropdown(
                options=options,
                id=f"{id_prefix}-dropdown",
                value=[options[0]],
                searchable=False,
                clearable=False,
                multi=True
            ),
        ],
        style={"padding": 10, "flex": 1},
    )


def create_barchart(id_prefix: str,) -> html.Div:
    return html.Div(
        children=[dcc.Graph(figure={}, id='{}-barchart'.format(id_prefix))]
    )
