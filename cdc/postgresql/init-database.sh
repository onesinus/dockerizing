#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE USER cdc_user;
	CREATE DATABASE cdc_pg_db;
	GRANT ALL PRIVILEGES ON DATABASE cdc_pg_db TO cdc_user;
EOSQL