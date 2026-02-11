#!/usr/bin/env zsh
export DB_USER=sajith.edirisinghe@lemon.markets
export RDS_HOST=apps-dev-live-db-core.cluster-cnhpc3ersdtn.eu-central-1.rds.amazonaws.com
export DB_PASSWORD="$(aws-vault exec apps-dev-live -- aws rds generate-db-auth-token --hostname $RDS_HOST --port 5432 --region eu-central-1 --username $DB_USER)"
export API_KEY=$LANGDOCK_API_KEY

exec uv run python3 db_tool.py
