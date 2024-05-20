# import requests
#
# url = "https://calcus.ru/calculate/Customs"
#
# form_data = {
#     "owner": "1",
#     "age": "5-7",
#     "engine": "1",
#     "power": "150",
#     "power_unit": "1",
#     "value": "2500",
#     "price": "1300000",
#     "curr": "JPY",
#     "isEmbed": "1",
#     "lang": "ru"
# }
#
# response = requests.post(url, data=form_data)
#
# if response.status_code == 200:
#     print("Request successful!")
#     print("Response content:")
#     print(response.text)
# else:
#     print("Request failed with status code:", response.status_code)
from werkzeug.security import generate_password_hash, check_password_hash

users = [(1, 'admin', 'scrypt:32768:8:1$AAxzZXb4VjKf40LV$52fa371d588c2597442c218526d2dfdad2f06b73a08991a776ee7805c37c9b70758e3f775dcb2445f7dff1ef41c3ac73c2e54d6a5d95b29b9a27245e0fb78b71')]
username_input = input("Enter your username: ")
password_input = input("Enter your password: ")
for user in users:
    if username_input == user[1] and check_password_hash(user[2], password_input):
        print("True")
    else:
        print("False")
