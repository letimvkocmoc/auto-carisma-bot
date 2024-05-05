import requests

url = "https://calcus.ru/calculate/Customs"

form_data = {
    "owner": "1",
    "age": "5-7",
    "engine": "1",
    "power": "150",
    "power_unit": "1",
    "value": "2500",
    "price": "1300000",
    "curr": "JPY",
    "isEmbed": "1",
    "lang": "ru"
}

response = requests.post(url, data=form_data)

if response.status_code == 200:
    print("Request successful!")
    print("Response content:")
    print(response.text)
else:
    print("Request failed with status code:", response.status_code)
