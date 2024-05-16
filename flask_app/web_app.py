import os

from flask import Flask, make_response, render_template, request, jsonify, session, redirect, url_for

from core.utils import get_calculation
from database.utils import SQL
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)


sql = SQL()

app.secret_key = os.getenv('FLASK_SECRET_KEY')


@app.route('/')
def index_page():
    return render_template('index1.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        #username = request.form.get('username')
        #password = request.form.get('password')
        #remember = request.form.get('remember')
        users = sql.get_users_from_website()

        for user in users:
            if username == user[1] and check_password_hash(user[2], password):
                session['username'] = username
                #if remember:
                response = make_response(redirect('/orders'))
                    #response.set_cookie('username', username, max_age=2592000)
                return response
            else:
                return render_template('login.html', error='Неверный логин или пароль')

    return render_template('login.html', error='')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return render_template('register.html')


def login_required(function):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return function(*args, **kwargs)
    return decorated_function


@app.route('/orders')
@login_required
def orders_page():
    orders = sql.get_users_from_website()
    return render_template('orders.html', orders=orders)


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    required_fields = ['owner', 'age', 'engine', 'power', 'power_unit', 'value', 'price', 'curr']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    result = get_calculation(data['owner'], data['age'], data['engine'], data['power'], data['power_unit'], data['value'], data['price'], data['curr'])

    return jsonify(result)


@app.route('/new_order')
def new_order_page():
    currencies = sql.get_currencies()
    return render_template('new_order.html', currency=currencies)


@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    sql.new_order(
        data['client_first_name'],
        data['client_last_name'],
        data['client_id'],
        data['client_phonenumber'],
        data['model_auto'],
        data['rating'],
        data['auto_price'],
        data['status'],
        data['picture'],
        data['link'],
        data['is_paid']
    )

    result = {'status': 'ok'}
    return result


@app.route('/edit/<int:id>')
def edit_order_page(id):
    order = sql.get_order(id)
    currencies = sql.get_currencies()
    return render_template('order.html', order=order, currency=currencies, id=id)


@app.route('/edit/<int:id>/update', methods=['POST'])
def update_order(id):
    data = request.get_json()
    sql.update_order(
        id,
        data['client_firstname'],
        data['client_lastname'],
        data['client_id'],
        data['client_phonenumber'],
        data['model_auto'],
        data['rating'],
        data['price'],
        data['status'],
        data['picture'],
        data['link'],
        int(data['is_paid'])
    )

    result = {'status': 'ok'}
    return result


@app.route('/edit/<int:id>/delete', methods=['POST'])
def delete_order(id):
    sql.delete_order(id)

    result = {'status': 'ok'}
    return result


if __name__ == '__main__':
    app.run(debug=True)
