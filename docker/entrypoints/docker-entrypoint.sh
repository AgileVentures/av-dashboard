#!/usr/bin/env bash
set -e

# add database migration before starting the service
alembic upgrade head --tag=docker_dev_db

exec "$@"