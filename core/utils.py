from datetime import datetime

import requests

from database.utils import SQL

sql = SQL()


def calculate_offer(car_price):
    currencies = sql.get_currencies()
    jpy_rate = currencies[2][0]
    usd_rate = currencies[1][0]
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

    result = {
        'EUR': 1 / eur_rate,
        'USD': 1 / usd_rate,
        'JPY': 1 / jpy_rate,
        'CNY': 1 / cny_rate,
        'updated': date_time_db.strftime('%H:%M час. %d.%m.%Y')
    }
    return result
