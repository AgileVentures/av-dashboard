from av_dashboard import create_app
from sqlalchemy import create_engine
from av_dashboard import our_base, user, plan, subscription
import contextlib
from sqlalchemy.orm import sessionmaker

app = create_app()

def clear_db(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI']  , convert_unicode=True)
    meta = our_base.Base.metadata
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()
    print("Cleared tables")

def basic_fixture(app):
    some_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=some_engine)
    session = Session()
    try:
        usr = user.User()
        pln = plan.Plan(amount=1000)
        sub = subscription.Subscription(user=usr,sponsor=usr,plan=pln)
        session.add(sub)
        session.commit()
        some_engine.dispose()
    finally:
        session.close()
    print("And seeded")

clear_db(app)
basic_fixture(app)
