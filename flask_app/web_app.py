from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/core')
def core():
    return render_template('core.html')


if __name__ == '__main__':
    app.run(debug=True)
