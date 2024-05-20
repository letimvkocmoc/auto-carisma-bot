from datetime import datetime

import requests
from flask import redirect, session

from database.utils import SQL

sql = SQL()


def login_required(function):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return function(*args, **kwargs)
    return decorated_function


def calculate_offer(car_price):
    currencies = sql.get_currencies()
    jpy_rate = currencies['currency']['JPY']
    usd_rate = currencies['currency']['USD']
    fract = 400
    japan_consumptions = (fract * usd_rate) + (car_price * jpy_rate) + (100000 * jpy_rate) + ((car_price * 0.03) * jpy_rate)
    return round(japan_consumptions)


def update_currency_rate():
    exchange_rate_url = 'https://api.exchangerate-api.com/v4/latest/RUB'
    response = requests.get(exchange_rate_url)
    data = response.json()
    timestamp = data['time_last_updated']
    date_time_db = datetime.fromtimestamp(timestamp)
    eur_rate = data['rates']['EUR']
    usd_rate = data['rates']['USD']
    jpy_rate = data['rates']['JPY']
    cny_rate = data['rates']['CNY']
    sql.update(1, rate=round((1 / eur_rate), 2), updated=date_time_db, last_request=datetime.now())
    sql.update(2, rate=round((1 / usd_rate), 2), updated=date_time_db, last_request=datetime.now())
    sql.update(3, rate=round((1 / jpy_rate), 2), updated=date_time_db, last_request=datetime.now())
    sql.update(4, rate=round((1 / cny_rate), 2), updated=date_time_db, last_request=datetime.now())


def get_calculation(owner, age, engine, power, power_unit, value, price, curr):

    url = "https://calcus.ru/calculate/Customs"

    form_data = {
        "owner": owner,
        "age": age,
        "engine": engine,
        "power": power,
        "power_unit": power_unit,
        "value": value,
        "price": price,
        "curr": curr,
        "isEmbed": "1",
        "lang": "ru"
    }

    response = requests.post(url, data=form_data)
    return response.json()
