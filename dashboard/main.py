import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
import pandas as pd

# Connect to your postgres DB
conn = psycopg2.connect("dbname=test user=postgres password=secret")

# Open a cursor to perform database operations
cur = conn.cursor()

# execute a statement
cur.execute("SELECT * FROM my_table")

# Retrieve query results with fetchall
results = cur.fetchall()

# Fetch columns and convert query to DataFrame
columns = [column[0] for column in cur.description]
df = pd.DataFrame(results,columns=columns)

# Close communication with the database
cur.close()
conn.close()

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
