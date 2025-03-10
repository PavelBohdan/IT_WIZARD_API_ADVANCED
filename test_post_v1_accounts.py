from pprint import pprint
from json import loads

import requests


def test_post_v1_account():
    login: str = 'pavel6'
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
    assert response.status_code == 201, 'Пользователь не был создан'

    # Получить письма из почтового сервера

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages',
                            params=params, verify=False)
    pprint(response.status_code)
    assert response.status_code == 200, 'Письма не были получены'
    # Получить активационный токен

    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']

        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/').pop()
            pprint(user_login)
            pprint(token)
            break
    assert token, f'Токен для пользователя: {login} не был получен'
    # Активация пользователя

    response = requests.put(
        f'http://5.63.153.31:5051/v1/account/{token}')

    pprint(response.json())
    assert response.status_code == 200, 'Пользователь не был активирован'

    # Авторизация

    json_data = {
        'login': 'pavel',
        'password': '12345678',
        'rememberMe': True,
    }

    response = requests.post(
        'http://5.63.153.31:5051/v1/account/login', json=json_data)
    pprint(response.status_code)
    assert response.status_code == 200, 'Пользователь не был авторизован'
