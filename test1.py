import pandas as pd


def get_currency_exchange_rates(date=None):
    if date is None:
        # Если дата не указана, используем текущую дату
        date = pd.Timestamp.now().strftime('%d/%m/%Y')

    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    try:
        # Чтение данных из XML
        page = pd.read_xml(url, encoding='cp1251')
        # Преобразование данных в словарь для удобного доступа к курсам валют
        exchange_rates = {}
        for index, row in page.iterrows():
            currency_code = row['CharCode']
            exchange_rate = float(row['Value'].replace(',', '.'))  # Преобразование строки в число
            exchange_rates[currency_code] = exchange_rate
        return exchange_rates
    except Exception as e:
        # Обработка ошибок, если запрос не удался или данные не удалось обработать
        print(f'Ошибка при получении курса валют: {e}')
        return None


def get_currency_rate():
    try:
        # Получаем курсы валют
        currencies = get_currency_exchange_rates()

        # Выводим информацию пользователю
        admin_ids = [367150414]
        for admin in admin_ids:
            print(f'Текущий курс валют:\n\n'
                  f'🇪🇺 Евро: {currencies.get("EUR")} ₽\n'
                  f'🇺🇸 Доллар США: {currencies.get("USD")} ₽\n'
                  f'🇯🇵 Японская Иена: {currencies.get("JPY") / 100} ₽\n'
                  f'🇨🇳 Китайский Юань: {currencies.get("CNY")} ₽\n')
    except Exception as e:
        # Обработка ошибок
        print(f'Ошибка при обновлении курса валют: {e}')


get_currency_rate()