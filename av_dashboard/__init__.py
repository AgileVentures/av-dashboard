import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import request, Flask, render_template, make_response,redirect, session
import jwt

def create_app(test_config=None):
    app = Flask(__name__)
    from io import StringIO
    if test_config is not None and 'session_key' in test_config:
        app.secret_key = test_config['session_key']
    else:
        app.secret_key = os.environ.get('session_key')
    if test_config is not None and 'jwt_key' in test_config:
        app.jwt_key = test_config['jwt_key']

    def generate_svg():
        d = {'temperature': [70, 80, 95], 'ice_cream_sales': [10, 25, 40]}
        df = pd.DataFrame(data=d)
        df.plot.scatter(x='temperature', y = 'ice_cream_sales', xticks = range(65,100)).plot()
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

    def formulate_response(decoded_token):
        if decoded_token.get('authorized') == 'true':
            return render_template('index.html', graph = generate_svg())
        else:
            return "You are not authorized to view this resource"

    def force_authentication():
        return app.config['ENV'] != "development"

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        if not force_authentication():
            return render_index()
        decoded_token = None
        token = extract_raw_token()
        if token is None:
            return redirect("https://www.agileventures.org/get-token")
        decoded_token = decode_token(token)
        if decoded_token is None:
            session['token'] = None
            return redirect("https://www.agileventures.org/get-token")
        session['token'] = token
        return formulate_response(decoded_token)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
