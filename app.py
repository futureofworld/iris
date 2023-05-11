import pandas as pd

from dash import Dash, html, dcc, Input, Output
import plotly.express as px


data = pd.read_csv('https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv')

species = data['species'].unique()

features = data.drop('species', axis=1).columns


app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.Div(  # graph div
            children= dcc.Graph(
                id="iris-chart",
                config={"displayModeBar": False}
            )
        ),
        html.Div(  # dropdown for x and y
            children=[
                dcc.Dropdown(
                    options=features,
                    value="sepal_length",
                    clearable=False,
                    id='x'
                ),
                dcc.Dropdown(
                    options=features,
                    value="petal_length",
                    clearable=False,
                    id='y'
                )
            ],
            className="selector"
        ),
        html.Div(  # multi select dropdown for species
            children=[
                dcc.Dropdown(
                    id='species',
                    options=species,
                    value=species,
                    multi=True,
                    clearable=False,
                )
            ]
        )
    ]
)


@app.callback(
    Output('iris-chart', 'figure'),
    Input('x', 'value'),  # take the x value from user
    Input('y', 'value'),  # take the y value from the user
    Input('species', 'value')  # take the species from the user
)
def update_graph(x_value, y_value, species):
    figure = px.scatter(
        data[data['species'].isin(species)],
        x=x_value,
        y=y_value,
        color='species',
        title='Comparision between sepal and petal',
    ),
    return figure[0]  # figure is of tuple type but graph needs figure type


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=True)