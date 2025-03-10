from pprint import pprint

import requests


def test_post_v1_account():
    login: str = 'pavel1'
    password: str = '12345678'
    email: str = f'{login}@mail.com'
    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }

    # Регистрация пользователя

    response = requests.post(
        'http://5.63.153.31:5051/v1/account', json=json_data)
    pprint(response.status_code)
    # Получить письма из почтового сервера

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages',
                            params=params, verify=False)

    pprint(response.status_code)
    # Получить активационный токен

    # Активация пользователя

    response = requests.put(
        'http://5.63.153.31:5051/v1/account/86bb6f4f-b27a-469f-8c52-2a057b180da9')

    pprint(response.status_code)
    # Авторизация

    json_data = {
        'login': 'pavel',
        'password': '12345678',
        'rememberMe': True,
    }

    response = requests.post(
        'http://5.63.153.31:5051/v1/account/login', json=json_data)
    pprint(response.status_code)
