def calculate_offer_1(car_price: int):
    currency_yen = 0.61
    currency_usd = 100
    fract = 400
    japan_consumptions = (fract * currency_usd) + (car_price * currency_yen) + (100000 * currency_yen) + (
                (car_price * 0.03) * currency_yen)
    return round(japan_consumptions)
