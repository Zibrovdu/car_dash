import dash_html_components as html
import dash_core_components as dcc


def serve_layout():
    layout = html.Div([
        html.Div([
            html.H2('HONDA The power of dreams'),
            # html.Img(src="assets/logo.png")
            html.A([
                html.Img(src="assets/pixlr-bg-result.png")
            ], href='#modal-1', className='js-modal-open link')
        ], className="banner"),
        html.Div([
            html.Div([
                dcc.Tabs(
                    id='',
                    value='',
                    children=[
                        dcc.Tab(
                            id='fuel_tab',
                            label='Топливо',
                            value='fuel',
                            children=[]
                        ),
                        dcc.Tab(
                            id='repair_tab',
                            value='repair',
                            label='Запчасти и работы',
                            children=[]
                        )
                    ])
            ])
        ])
    ])
    return layout
