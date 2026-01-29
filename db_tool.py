
"""Thin wrapper delegating to modular package `db_tool_pkg`.

Keeps backward compatibility for imports of `db_tool_main` and `app`.
"""

from __future__ import annotations

from db_tool_pkg import db_tool_main, app  # noqa: F401

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
