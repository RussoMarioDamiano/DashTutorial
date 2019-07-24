import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd

# Load the iris dataset
df = pd.read_csv("https://raw.githubusercontent.com/RussoMarioDamiano/DashTutorial/master/iris.csv?")
df.head()

# Download a CSS template from the internet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Create the Dash app component
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define a layout for our app
app.layout = html.Div([
    html.Div("Hello, World!")
])

if __name__ == "__main__":
    app.run_server(debug=True)
