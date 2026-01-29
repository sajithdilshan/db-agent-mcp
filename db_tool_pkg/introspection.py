"""Database introspection utilities."""
from __future__ import annotations
from typing import List

def get_table_names(conn) -> List[str]:
    """Return a list of table names for the connected database.

    Tries SQLite first; falls back to Postgres public schema if available.
    """
    cur = conn.cursor()
    tables: List[str] = []
    try:
        try:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            rows = cur.fetchall()
            if rows:
                tables = [r[0] for r in rows]
        except Exception:
            pass
        if not tables:
            try:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
                rows = cur.fetchall()
                tables = [r[0] for r in rows]
            except Exception:
                pass
    finally:
        cur.close()
    return tables
