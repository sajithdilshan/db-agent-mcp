"""Tool schema definition for database querying."""
from __future__ import annotations
from typing import Any, Dict

DB_TOOL: Dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "query_db",
        "description": (
            "Execute a SQL query against the current database connection to retrieve data needed to answer the user question."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "SQL query to execute (must include LIMIT)."}
            },
            "required": ["sql"],
        },
    },
}
