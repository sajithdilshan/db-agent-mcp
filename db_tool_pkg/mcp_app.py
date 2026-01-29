"""MCP app and public entrypoint function."""
from __future__ import annotations
from typing import Dict, Optional
from rich.panel import Panel
from mcp.server.fastmcp import FastMCP

from .config import console, logger
from .agent import ChatDBAgent
from sqllite import get_db_conn

mcp = FastMCP("db-tool-agent", stateless_http=True)

@mcp.tool()
def db_tool_main(question: str) -> Dict[str, Optional[str]]:
    """Answer a natural-language question with SQL + summary.

    Returns dict with keys 'query' and 'summary'. Errors => summary message, query None.
    """
    console.print(Panel(f"Received question: {question}", style="green"))
    try:
        conn = get_db_conn()
    except Exception as init_err:
        logger.exception("Failed to create DB")
        return {"query": None, "summary": f"DB init error: {init_err}"}

    try:
        agent = ChatDBAgent(conn)
        result = agent.run(question)
        logger.info("Final Result: %s", result)
        return result
    finally:
        try:
            conn.close()
        except Exception as close_err:
            logger.warning("DB close failed: %s", close_err)

app = mcp.streamable_http_app()
