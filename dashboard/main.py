import dash
import pandas as pd
import psycopg2
from dash import html, dash_table


def get_db_connection():
    return psycopg2.connect(database='postgres',
                            user="user",
                            password="user")


def graph_trend_per_categories(dash_app):
    # Connect to your postgres DB
    conn = get_db_connection()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # execute a statement
    cur.execute("SELECT * FROM youtube_videos")

    # Retrieve query results with fetchall
    results = cur.fetchall()

    # Fetch columns and convert query to DataFrame
    columns = [column[0] for column in cur.description]
    df = pd.DataFrame(results, columns=columns)

    # Close communication with the database
    cur.close()
    conn.close()

    dash_app.layout = html.Div([
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'categoryId': c, 'count': c} for c in df.columns]
        )
    ])


if __name__ == '__main__':
    app = dash.Dash(__name__)
    app.run_server(debug=True)
    graph_trend_per_categories(app)
