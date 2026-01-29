import os

import psycopg2
from rich.panel import Panel


def get_db_conn():
    conn = psycopg2.connect(
        host=os.environ["RDS_HOST"],
        port=5432,
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        dbname="postgres",
        sslmode="require"
    )

    print("Connected to the database successfully.")

    return conn


def call_database_query(console, conn, query: str):
    try:
        cur = conn.cursor()
        console.print(Panel(f"[bold cyan]Query:[/] {query}", style="magenta"))
        cur.execute(query)
        result = cur.fetchall()
    except Exception as e:
        result = f"Error: {e}"
    return result
