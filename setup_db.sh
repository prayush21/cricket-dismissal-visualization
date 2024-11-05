#!/bin/bash

# Set database connection parameters
DB_NAME="player_stats_db"
DB_USER="postgres"  # Replace with your PostgreSQL username
DB_PASSWORD=""  # Replace with your PostgreSQL password
DB_HOST="localhost"

# Export the password to avoid password prompt
export PGPASSWORD=$DB_PASSWORD

# Run the SQL scripts
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f apps/db/migrations/001_initial_tables.sql
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f apps/db/migrations/002_populate_formats.sql

# Unset the password variable
unset PGPASSWORD