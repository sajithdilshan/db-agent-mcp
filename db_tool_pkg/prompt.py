"""System prompt construction for the chat agent."""
from __future__ import annotations
from typing import List

def build_system_prompt(tables: List[str]) -> str:
    if tables:
        table_block = "\n".join(f"- {name}" for name in tables)
    else:
        table_block = "(No tables discovered)"
    return (
        "You are a data assistant that answers using a SQL tool for live data.\n"
        "Rules:\n"
        "- Only read from allowlisted tables/views listed below.\n"
        "- All SQL must be valid for the underlying engine (SQLite now; Postgres style acceptable if compatible).\n"
        "- Never guess columns; if unsure, ask a clarifying question.\n"
        "- Use information_schema (if available) to discover columns.\n"
        "- Every query MUST include a LIMIT clause (add LIMIT 50 if user omitted).\n"
        "- Use ISO8601 dates and assume UTC unless specified.\n"
        "- After executing SQL, summarize clearly with units and time range.\n"
        "- If no rows returned, state that and propose next steps.\n"
        "- If the user query is unrelated to the database, explain limitation.\n"
        "- Respond STRICTLY as JSON with keys 'query' and 'summary'.\n\n"
        "Allowlisted tables:\n"
        f"{table_block}\n"
    )
