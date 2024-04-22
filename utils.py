from database.utils import SQL

sql = SQL()


def calculate_offer(car_price):
    currencies = sql.get_currencies()
    jpy_rate = currencies[2][0]
    usd_rate = currencies[1][0]
    fract = 400
    japan_consumptions = (fract * usd_rate) + (car_price * jpy_rate) + (100000 * jpy_rate) + ((car_price * 0.03) * jpy_rate)
    return round(japan_consumptions)
