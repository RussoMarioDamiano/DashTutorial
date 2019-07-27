import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output, State
from sklearn.linear_model import LinearRegression

# Load the iris dataset
df = pd.read_csv("https://raw.githubusercontent.com/RussoMarioDamiano/DashTutorial/master/iris.csv?")

# Download a CSS template from the internet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Create the Dash app component
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define a layout for our app
app.layout = html.Div(children=[

    #Our title goes here
    html.Div(children=[
        # Main title
        html.H1(children="Our amazing dashboard",
                style={"textAlign": "center", "font-weight": "bold"}),
        # Description
        html.Div(children="Our amazing description",
                style={"textAlign": "center", "font-style": "italic"})
        ]),

    # Filter
    html.Div(children=[
        html.Div([
            # Iris species selector div
            html.Div([
                html.H4("Restrict Iris Species"),
                # Dropdown selector to filter flower specie
                dcc.Dropdown(
                    id="dropdown_selector",
                    options=[{"label": specie, "value": specie} for specie in df.species.unique()],
                    value=df.species.to_list()[0],
                    multi=True)
                ], style={"width": "45%", "display": "table-cell", "padding-right": "5%"}),

            # Regression show Block
            html.Div([
                html.H4("Show Linear Regression"),
                html.Div([
                    html.Div("Off", style={"display": "inline-block", "verticalAlign": "top", "padding-top": "2px"}),
                    # Switch
                    daq.BooleanSwitch(
                        id="RegressionSwitch",
                        on=True,
                        style={"display": "inline-block"}),
                    html.Div("On", style={"display": "inline-block", "verticalAlign": "top", "padding-top": "2px"})
                    ])
                ], style={"width": "45%", "display": "table-cell", "padding-left": "5%"})
            ], style={"display": "table", "width": "100%"}),

        #sliders restrictor
        html.Div([
            html.Div([
                html.H4("Restrict Sepal Length"),
                dcc.RangeSlider(id="slider_length",
                                min=df.sepal_length.min(),
                                max=df.sepal_length.max(),
                                marks=dict(zip(
                                    [df.sepal_length.min() - 1e-9, round((df.sepal_length.min() + df.sepal_length.max())/2, 1), df.sepal_length.max() + 1e-9],
                                    [str(df.sepal_length.min()), str(round((df.sepal_length.min() + df.sepal_length.max())/2, 1)), str(df.sepal_length.max())]
                                    )),
                                step=0.1,
                                value=[df.sepal_length.min(), df.sepal_length.max()]
                            )
                    ],style={"width": "45%", "display": "inline-block", "padding-right": "5%"}),
            html.Div([
                html.H4("Restrict Sepal Width"),
                dcc.RangeSlider(id="slider_width",
                                min=df.sepal_width.min(),
                                max=df.sepal_width.max(),
                                marks=dict(zip(
                                    [df.sepal_width.min() - 1e-9, round((df.sepal_width.min() + df.sepal_width.max())/2, 1), df.sepal_width.max()+ 1e-9],
                                    [str(df.sepal_width.min()), str(round((df.sepal_width.min() + df.sepal_width.max())/2, 1)), str(df.sepal_width.max())]
                                    )),
                                step=0.1,
                                value=[df.sepal_width.min(), df.sepal_width.max()]
                            )
                ],style={"width": "45%", "display": "inline-block", "padding-left": "5%"}),
            ], style = {"padding-top": "10px"})
        ], style={"padding-top": "15px", "position": "relative", "zIndex": "999"}),

    # Our graph goes here - it will appear as the Div's "children" argument through the callback
    html.Div(id="graph", style={"padding-top": "50px"})
], style={"padding-left": "15px", "padding-right":"15px"})

# Callback decorator - makes our dashboard dynamic!
@app.callback(
    Output(component_id="graph", component_property="children"),
    [Input(component_id="dropdown_selector", component_property="value"),
    Input(component_id="slider_length", component_property="value"),
    Input(component_id="slider_width", component_property="value"),
    Input(component_id="RegressionSwitch", component_property="on")]
    )
# This is our callback's function - it will be activated whenever the Input(s)'s property changes
def update_graph(species_list, length_range, width_range, show_reg):
    # ensure that species_list is always a list (it could be a string if only 1 specie is selected)
    if type(species_list) != list:
        species_list = [species_list]

    # filter df based on: species, length, width
    df_filtered = df[
        (df.species.isin(species_list)) &
        (df.sepal_length.apply(lambda x: x * 10).isin(range(int(length_range[0] * 10), int(length_range[1] * 10)))) & # we need to multiply by 10 because Python's range does not work with floats
        (df.sepal_width.apply(lambda x: x * 10).isin(range(int(width_range[0] * 10), int(width_range[1] * 10))))] # we need to multiply by 10 because Python's range does not work with floats

    data = [{"x":df_filtered[df_filtered.species == specie].loc[:, "sepal_length"],
             "y":df_filtered[df_filtered.species == specie].loc[:, "sepal_width"],
             "name": specie,
             "type": "scatter",
             "mode": "markers"} for specie in df_filtered.species.unique()]

    if show_reg:
        lin_reg = LinearRegression()
        X = np.array(df_filtered.sepal_length.values).reshape((-1, 1))
        y = np.array(df_filtered.sepal_width.values).reshape((-1, 1))
        lin_reg.fit(X=X, y=y)
        predicted_values = lin_reg.predict(X)
        data += [{"x": df_filtered.sepal_length.to_list(),
                 "y": [e for sl in predicted_values.tolist() for e in sl],
                 "name": "forecast",
                 "type": "scatter"}]

    # return the children property containing the graph
    return [dcc.Graph(
        figure={
            # Data (list of dictionaries)
            "data": data,
            # Add title and axis labels
            "layout": {"title": "The Iris Dataset",
                        "xaxis": {"title": "sepal length"},
                        "yaxis": {"title": "sepal width"}
                        }
        }
    )]

if __name__ == "__main__":
    app.run_server(debug=False)
