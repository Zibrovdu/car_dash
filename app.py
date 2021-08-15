import dash

from car_dash.layouts import serve_layout
from car_dash.callbacks import register_callbacks


app = dash.Dash(__name__,
                title='Honda The power of dream')
server = app.server

app.layout = serve_layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server()
