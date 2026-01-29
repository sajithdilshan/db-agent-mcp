# DB Querying Agent MCP Server

## Overview
This project exposes a database querying AI agent as a Model Context Protocol (MCP) server over HTTP on `http://127.0.0.1:8000`. The agent accepts natural language questions about the (sample / in‑memory) database and returns:
1. The exact SQL query executed
2. A concise, human‑readable summary of the results (or an error message)

The implementation wraps an AI model (configured via `API_KEY`) which uses a function/tool calling interface to generate safe, syntactically correct PostgreSQL queries, execute them, and summarize outcomes. It is designed to be integrated by MCP‑aware clients (e.g. IDE extensions, automation agents) that can call the tool `db_tool_main`.

## Key Components
- `db_tool.py`: Defines the MCP tool and HTTP app (`FastMCP` + Uvicorn) and the agent loop calling the LLM.
- `sqllite.py`: Creates and queries an in‑memory database used for demonstration (can be swapped for a real DB).
- `spinner.py`: Simple CLI spinner for user feedback during LLM thinking.
- `example_run.sh`: Template environment setup script (to be completed and renamed as run.sh).

## MCP Tool: `db_tool_main`
The MCP tool is registered via a decorator and exposed over HTTP. It accepts one required argument:

Input JSON:
```
{
	"question": "How many users signed up this week?"
}
```

Output JSON (success):
```
{
	"query": "SELECT COUNT(*) FROM users WHERE signup_date >= '2025-11-09'",
	"summary": "42 users signed up since 2025-11-09 (UTC)."
}
```

Output JSON (error):
```
{
	"query": null,
	"summary": "Error occurred: <details>"
}
```

### Behavior & Guarantees
- Adds `LIMIT` automatically if missing (per system rules).
- Only reads from allow‑listed tables (enumerated dynamically).
- Will ask clarifying questions rather than guessing schema details.
- Returns structured JSON only; MCP clients can rely on the `query` + `summary` fields.

## How the Agent Works Internally
1. Receives the natural language `question`.
2. Sends context + tool schema (`query_db`) to the LLM.
3. LLM may produce tool calls with arguments containing an SQL statement.
4. The SQL is executed against the in‑memory database (or future real DB) and results appended to the conversation.
5. Once the model stops calling tools, its final message must be valid JSON with `query` and `summary`.
6. Errors anywhere yield a consistent error JSON structure.

## Environment Variables
For a real database / auth flow, these variables are expected (template shows them):
-  LLM_MODEL: Model name (default: `gpt-4o`).
-  API_BASE_URL: Base URL for the LLM provider.
- `API_KEY`: Key for the upstream LLM provider.
- `DB_USER`: Database username (esp. for RDS IAM auth flows).
- `RDS_HOST`: Host of the target Postgres instance.
- `RDS_PORT`: Port (default: `5432`).
- `AWS_PROFILE`: Local AWS profile name (used by `aws-vault`).
- `AWS_REGION`: AWS region of the RDS instance.
- `DB_PASSWORD`: Generated auth token (IAM) or password, produced in script.

## Completing and Renaming the Startup Script
The file `example_run.sh` is a template with empty values:
```bash
export LLM_MODEL=
export API_BASE_URL=
export API_KEY=
export DB_USER=
export RDS_HOST=
export RDS_PORT=5432
export AWS_PROFILE=
export AWS_REGION="eu-central-1"
export DB_PASSWORD="$(aws-vault exec $AWS_PROFILE -- aws rds generate-db-auth-token --hostname $RDS_HOST --port $RDS_PORT --region $AWS_REGION --username $DB_USER)"
```
Steps:
1. Fill in the missing values (`API_KEY`, `DB_USER`, `RDS_HOST`, `AWS_PROFILE`).
2. (Optional) Adjust region or port.
3. Rename the file to `run.sh` (if `run.sh` already exists, replace or merge as needed).
4. Make it executable: `chmod +x run.sh`.
5. Execute: `./run.sh`.

Upon execution it will export variables and start the MCP HTTP server with Uvicorn.

## Starting the MCP Server
Prerequisites:
1. Install dependencies (uses `uv` & `pyproject.toml`).
2. Ensure environment variables are set (via `run.sh`).

Commands:
```bash
uv sync          # install Python dependencies
./run.sh         # start server (runs db_tool.py)
```

Server availability:
- Host: `http://127.0.0.1:8000/mcp`
- Exposes the MCP tool endpoint via FastMCP's HTTP interface (MCP clients discover tools automatically).

## Example MCP Invocation (Conceptual)
If a client sends (pseudo‑request):
```
POST /tools/db_tool_main
{
	"question": "Show the latest 5 users by signup date"
}
```
Response:
```
{
	"query": "SELECT id, email, signup_date FROM users ORDER BY signup_date DESC LIMIT 5",
	"summary": "Returned 5 most recent users with signup timestamps (UTC)."
}
```

## Quick Start Summary
```bash
uv sync
cp example_run.sh run.sh   # if not yet renamed
vim run.sh                  # fill env vars
chmod +x run.sh
./run.sh                    # starts MCP server at 127.0.0.1:8000
```
