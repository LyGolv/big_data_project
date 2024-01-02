import pandas as pd
import plotly.express as px

from dash import Dash, dash_table
from dash import dcc
from dash import html

# Assuming your DataFrame or CSV file is called 'df'
# df = pd.read_csv("your_data.csv", sep="\t")
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv")

app = Dash(__name__)

# fig = px.line(df, x='Time', y='Views', title='YouTube Video Views Over Time')

# app.layout = html.Div(children=[
#     html.H1(children="YouTube Video Analysis"),
#
#     dcc.Graph(
#         id='youtube-graph',
#         figure=fig
#     )
# ])

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

if __name__ == '__main__':
    app.run_server(debug=True)
