import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import request, Flask, render_template, make_response,redirect, session
import jwt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from av_dashboard.database import db_connection
from io import StringIO
from sqlalchemy import create_engine


def configure_db_engine(app, test_config):
    if test_config and 'postgres' in test_config:
        POSTGRES = test_config['postgres']
    else:
        POSTGRES = {'user': 'postgres', 'pw': 'password', 'host': 'localhost', 'port': '5432', 'db': 'db'}
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    app.db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'] , convert_unicode=True)

def create_app(test_config=None):
    app = Flask(__name__)
    configure_db_engine(app, test_config)
    if test_config is not None and 'session_key' in test_config:
        app.secret_key = test_config['session_key']
    else:
        app.secret_key = os.environ.get('session_key')
    if test_config is not None and 'jwt_key' in test_config:
        app.jwt_key = test_config['jwt_key']

    def generate_svg():
        app.db_connection = db_connection(app)
        query = """
        WITH subscription_records AS
        (SELECT users.created_at as join_date, subscriptions.user_id as user_id, subscriptions.started_at as started_at, subscriptions.ended_at as ended_at, plans.amount as amount, subscriptions.sponsor_id as sponsor_id
        FROM subscriptions
        INNER JOIN plans on subscriptions.plan_id = plans.id
        INNER JOIN users on subscriptions.user_id = users.id)

        SELECT COUNT(quarter_signed_up) as number_of_upgrades, quarter_signed_up - 1 + 4*(year_signed_up-2013) as quarters_counted_from_january_2013_to_user_signing_up
        FROM (SELECT EXTRACT(QUARTER FROM result.join_date) as quarter_signed_up, EXTRACT(YEAR FROM result.join_date) as year_signed_up
        FROM (SELECT t1.started_at::date as upgrade_date, t1.user_id as user_id, t1.join_date::date as join_date
        FROM subscription_records t1, subscription_records t2
        WHERE t1.user_id = t2.user_id
        AND t1.amount > t2.amount
        AND t1.started_at::date = t2.ended_at::date
        AND (t1.sponsor_id = t1.user_id OR t1.sponsor_id IS null)) as result) resultant
        GROUP BY quarter_signed_up, year_signed_up
        ORDER BY quarter_signed_up, year_signed_up ASC
        """
        d = pd.read_sql(query, app.db_connection)
        d.plot.scatter(x='quarters_counted_from_january_2013_to_user_signing_up', y = 'number_of_upgrades', xticks = range(20)).plot()
        figfile = StringIO()
        plt.savefig(figfile, format='svg')
        figfile.seek(0)
        figdata_svg = '<svg' + figfile.getvalue().split('<svg')[1]
        return figdata_svg

    def extract_raw_token():
        if 'token' in request.form:
            return request.form['token']
        elif 'token' in session:
            return session['token']

    def decode_token(token):
        decoded_token = None
        try:
            decoded_token = jwt.decode(token, app.jwt_key, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return
        return decoded_token

    def render_index():
        return render_template('index.html', graph = generate_svg())

    def force_authentication():
        return app.config['ENV'] != "development"

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not force_authentication():
                return f(*args, **kwargs)
            decoded_token = None
            token = extract_raw_token()
            if token is None:
                return redirect("https://www.agileventures.org/get-token")
            decoded_token = decode_token(token)
            if decoded_token is None:
                session['token'] = None
                return redirect("https://www.agileventures.org/get-token")
            session['token'] = token
            if decoded_token.get('authorized') == 'true':
                return f(*args, **kwargs)
            else:
                return "You are not authorized to view this resource"
        return decorated_function

    @app.route("/", methods=['GET', 'POST'])
    @login_required
    def hello():
        return render_index()
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if hasattr(app, 'db_connection'):
            app.db_connection.close()
            delattr(app, "db_connection")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
