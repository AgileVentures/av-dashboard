import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import request, Flask, render_template, make_response

def create_app(test_config=None):
    app = Flask(__name__)
    from io import StringIO

    def generate_svg():
        d = {'temperature': [70, 80, 95], 'ice_cream_sales': [10, 25, 40]}
        df = pd.DataFrame(data=d)
        df.plot.scatter(x='temperature', y = 'ice_cream_sales', xticks = range(65,100)).plot()
        figfile = StringIO()
        plt.savefig(figfile, format='svg')
        figfile.seek(0)
        figdata_svg = '<svg' + figfile.getvalue().split('<svg')[1]
        return figdata_svg

    @app.route("/")
    def hello():
        return render_template('index.html', graph = generate_svg())

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
