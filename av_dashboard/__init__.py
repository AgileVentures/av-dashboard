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

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        token = None
        if 'token' in request.form:
            token = request.form['token']
        elif 'token' in session:
            token = session['token']
        else:
            return redirect("https://www.agileventures.org/get-token")
        try:
            jwt.decode(token, app.jwt_key, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            session['token'] = None
            return redirect("https://www.agileventures.org/get-token")
        session['token'] = token
        return render_template('index.html', graph = generate_svg())

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
