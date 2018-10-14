#!/bin/sh
FLASK_ENV=test python3 create_database.py
FLASK_ENV=dev python3 create_database.py
