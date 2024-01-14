import os

import dash
import pandas as pd
import psycopg2
from dash import html, dash_table, dcc
import plotly.express as px


def get_db_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def graph_trend_per_categories(dash_app):
    # Connect to your postgres DB
    conn = get_db_connection()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # execute a statement
    cur.execute("SELECT * FROM youtube_analysis")

    # Retrieve query results with fetchall
    results = cur.fetchall()

    # Fetch columns and convert query to DataFrame
    columns = [column[0] for column in cur.description]
    df = pd.DataFrame(results, columns=columns)

    # Close communication with the database
    cur.close()
    conn.close()

    dash_app.layout = html.Div([
        html.H1(children='Category count based on Trending videos', style={'textAlign': 'center'}),
        dash_table.DataTable(
            data=df.to_dict('records'),
            page_size=10
        ),
        dcc.Graph(figure=px.histogram(df, x='categoryId', y='count', histfunc='avg'))
    ])


if __name__ == '__main__':
    app = dash.Dash(__name__)
    graph_trend_per_categories(app)
    app.run_server(debug=True, host='0.0.0.0', port=9000)
