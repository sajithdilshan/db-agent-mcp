"""ChatDBAgent encapsulating model loop and tool execution."""
from __future__ import annotations
import json
from typing import Any, Dict, List
from rich.panel import Panel

from .config import MODEL, client, console, logger
from .schema import DB_TOOL
from .introspection import get_table_names
from .prompt import build_system_prompt
from spinner import Spinner
from sqllite import call_database_query

class ChatDBAgent:
    def __init__(self, conn) -> None:
        self.conn = conn
        self.messages: List[Dict[str, Any]] = []

    def _call_model(self) -> Any:
        return client.chat.completions.create(
            model=MODEL,
            messages=self.messages,
            tools=[DB_TOOL],
        )

    def _append(self, role: str, **kwargs) -> None:
        entry: Dict[str, Any] = {"role": role}
        entry.update(kwargs)
        self.messages.append(entry)

    def run(self, user_input: str) -> Dict[str, Any]:
        tables = get_table_names(self.conn)
        system_prompt = build_system_prompt(tables)
        self._append("system", content=system_prompt)
        self._append("user", content=user_input)

        try:
            while True:
                with Spinner("Thinking..."):
                    response = self._call_model()
                choice = response.choices[0]
                message = choice.message

                tool_calls = getattr(message, "tool_calls", None)
                if tool_calls:
                    self._append(
                        "assistant",
                        tool_calls=[
                            {"id": tc.id, "type": tc.type, "function": tc.function}
                            for tc in tool_calls
                        ],
                    )
                    for tc in tool_calls:
                        sql = None
                        try:
                            args = json.loads(tc.function.arguments)
                            sql = args.get("sql", "")
                            result = call_database_query(console, self.conn, sql)
                            console.print(Panel(f"Result: {result}", style="magenta"))
                            self._append(
                                "tool",
                                content=json.dumps(result),
                                tool_call_id=tc.id,
                            )
                        except Exception as exec_err:
                            logger.exception("Tool execution failed")
                            return {"query": sql, "summary": f"Tool error: {exec_err}"}
                else:
                    content = message.content or "{}"
                    console.print(Panel(f"Assistant: {content}", style="green"))
                    try:
                        parsed = json.loads(content)
                        if "query" not in parsed or "summary" not in parsed:
                            parsed = {"query": parsed.get("query"), "summary": parsed.get("summary", content)}
                        return parsed
                    except json.JSONDecodeError:
                        return {"query": None, "summary": content}
        except Exception as e:
            logger.exception("Unhandled agent error")
            return {"query": None, "summary": f"Agent error: {e}"}
