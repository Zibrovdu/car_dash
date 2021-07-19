import dash_html_components as html
import dash_core_components as dcc


def serve_layout():
    layout = html.Div([
        dcc.Dropdown(id='1',
                     options=[
                         {'name': 'qwe', 'value': 1},
                         {'name': 'asd', 'value': 2}
                     ])
    ])
    return layout
