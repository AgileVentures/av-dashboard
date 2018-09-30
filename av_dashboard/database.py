def db_connection(app):
    return app.db_engine.connect()
