import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import request, Flask, render_template, make_response,redirect,session
import jwt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from av_dashboard.database import db_connection
from io import StringIO
from sqlalchemy import create_engine
from pathlib import Path

def select_configuration_file():
    import os
    import pathlib
    if os.environ['FLASK_ENV'] == 'test':
        return str(pathlib.Path(".").absolute().joinpath(Path("config/testing.py")))
    if os.environ['FLASK_ENV'] == 'ci':
        return str(pathlib.Path(".").absolute().joinpath(Path("config/ci.py")))
    if os.environ['FLASK_ENV'] == 'dev':
        return str(pathlib.Path(".").absolute().joinpath(Path("config/dev.py")))
    if os.environ['FLASK_ENV'] == 'docker_dev':
        return str(pathlib.Path(".").absolute().joinpath(Path("config/docker_dev.py")))
    if os.environ['FLASK_ENV'] == 'production':
        return str(pathlib.Path(".").absolute().joinpath(Path("config/production.py")))

def configure_db_engine(app, test_config):
    if 'DATABASE_URL' in app.config:
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
    else:
        POSTGRES = {'user': app.config['POSTGRES_USER'], 'pw': app.config['POSTGRES_PASSWORD'], 'host': app.config['POSTGRES_HOST'], 'port': app.config['POSTGRES_PORT'], 'db': app.config['POSTGRES_DATABASE']}
        if POSTGRES['pw']:
            POSTGRES['pw'] = ':%(pw)s' % POSTGRES
        if POSTGRES['port']:
            POSTGRES['port'] = ':%(port)s' % POSTGRES
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s%(pw)s@%(host)s%(port)s/%(db)s' % POSTGRES
    app.db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'] , convert_unicode=True)

def add_webpack_filter(app):
    if os.environ['FLASK_ENV'] != 'production':
        from jinja2_webpack import Environment as WebpackEnvironment
        from jinja2_webpack.filter import WebpackFilter
        webpack_env = WebpackEnvironment(publicRoot = '/static', manifest='./av_dashboard/static/webpack-manifest.json')
        app.jinja_env.filters['webpack'] = WebpackFilter(webpack_env)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    add_webpack_filter(app)
    if os.environ['FLASK_ENV'] != 'production':
        app.config.from_pyfile('config.py')
    app.config.from_pyfile(select_configuration_file())
    configure_db_engine(app, test_config)
    if test_config is not None and 'session_key' in test_config:
        app.secret_key = test_config['session_key']
    else:
        app.secret_key = os.environ.get('session_key')
    if test_config is not None and 'jwt_key' in test_config:
        app.jwt_key = test_config['jwt_key']
    if 'JWT_KEY' in app.config:
        app.jwt_key = app.config['JWT_KEY']

    def generate_svg():
        app.db_connection = db_connection(app)
        query= """
        SELECT quarter_signed_up, year_signed_up, AVG(days_to_first_subscribe) as average_days_to_subscribe, quarter_signed_up - 1 + 4*(year_signed_up-2013) as quarters_counted_from_january_2013_to_user_signing_up
        FROM (SELECT result.user_signs_up, result.first_value as user_first_subscribes, EXTRACT(QUARTER FROM result.user_signs_up) as quarter_signed_up, EXTRACT(YEAR FROM result.user_signs_up) as year_signed_up,
        CASE WHEN result.user_signs_up::date > '2016-5-31'::date THEN result.first_value::date - result.user_signs_up::date
        ELSE result.first_value::date - '2016-5-31'::date
        END as days_to_first_subscribe
        FROM (SELECT users.id as user_id, users.created_at as user_signs_up, first_value(subscriptions.started_at) OVER (PARTITION BY user_id)
        FROM subscriptions
        INNER JOIN users on subscriptions.user_id = users.id
        WHERE subscriptions.sponsor_id = users.id OR subscriptions.sponsor_id IS null
        ORDER BY subscriptions.started_at ASC) as result) as resultant
        GROUP BY quarter_signed_up, year_signed_up
        ORDER BY year_signed_up, quarter_signed_up ASC
        """
        d = pd.read_sql(query, app.db_connection)
        d.plot.scatter(x='quarters_counted_from_january_2013_to_user_signing_up', y = 'average_days_to_subscribe', xticks = range(20))
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
        return render_template('index.html', environment = os.environ['FLASK_ENV'], graph = generate_svg())

    def force_authentication():
        return app.config['ENV'] not in ['dev', 'docker_dev']

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
