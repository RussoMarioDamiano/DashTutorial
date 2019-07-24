import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd

# Load the iris dataset
df = pd.read_csv("https://raw.githubusercontent.com/RussoMarioDamiano/DashTutorial/master/iris.csv?")

# Download a CSS template from the internet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Create the Dash app component
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define a layout for our app
app.layout = html.Div([
    dcc.Graph(
        figure={
            "data":[{"x":df[df.species == specie].loc[:, "sepal_length"],
                     "y":df[df.species == specie].loc[:, "sepal_width"],
                     "name": specie,
                     "type": "scatter",
                     "mode": "markers"} for specie in df.species.unique()]
            }
        )
])

if __name__ == "__main__":
    app.run_server(debug=True)
