from flask import Flask, render_template
from database.utils import SQL


app = Flask(__name__)


sql = SQL()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/orders')
def core():
    orders = sql.get_orders()
    return render_template('orders.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True)