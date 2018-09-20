from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from av_dashboard import create_app


app = create_app()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(engine.url):
    create_database(engine.url)
    print("Created db")
else:
    print("DB already existed")
