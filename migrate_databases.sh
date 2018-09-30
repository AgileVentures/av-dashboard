#!/bin/sh
alembic upgrade head --tag=test_db
alembic upgrade head --tag=dev_db
