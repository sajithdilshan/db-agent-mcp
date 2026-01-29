#!/usr/bin/env zsh

# Name of the LLM model to use
export LLM_MODEL="gpt-5"
#API base URL
export API_BASE_URL="https://api.langdock.com/v1"
# API key for the LLM (e.g: OpenAI, Anthropic)
export API_KEY=
# Database user name
export DB_USER=
# RDS host name (e.g: mydb.xxxxxxxxxxxx.eu-central-1.rds.amazonaws.com)
export RDS_HOST=
export RDS_PORT=5432
# AWS profile name configured in aws-vault
export AWS_PROFILE=
export AWS_REGION="eu-central-1"
export DB_PASSWORD="$(aws-vault exec $AWS_PROFILE -- aws rds generate-db-auth-token --hostname $RDS_HOST --port $RDS_PORT --region $AWS_REGION --username $DB_USER)"

# Verify required environment variables are set and non-empty
for var in DB_USER RDS_HOST AWS_PROFILE API_KEY; do
	if [ -z "${(P)var}" ]; then
		echo "Error: $var is not set or is empty" >&2
		exit 1
	fi
done

exec uv run python3 db_tool.py
