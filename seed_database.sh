#!/bin/bash
FLASK_ENV=${FLASK_ENV:-dev}
FLASK_ENV=$FLASK_ENV python3 seed_database.py
