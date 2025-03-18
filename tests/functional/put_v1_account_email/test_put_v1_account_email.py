from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailHogApi
from faker import Faker

fake = Faker()


def test_put_v1_account_email():

    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailHogApi(host='http://5.63.153.31:5025')

    # Регистрация пользователя
    login: str = fake.name_nonbinary()
    password: str = '12345678'
    email: str = f'{login.replace(" ", "")}@mail.com'
    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }
    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, 'Пользователь не был создан'

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, 'Письма не были получены'

    # Получить активационный токен
    token = account_api.get_token_by_login(login=login, response=response)

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, 'Пользователь не был активирован'

    # Авторизация
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, 'Пользователь не был авторизован'

    # Изменение адреса электронной почты
    json_data['email'] = f'{login}_changed@mail.com'
    response = account_api.put_v1_account_email(json_data=json_data)
    assert response.status_code == 200, 'Адрес электронной почты не был изменен'

    # Пытаемся войти, получаем 403
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403

    # На почте находим токен по новому емейлу для подтверждения смены емейла
    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, 'Письма не были получены'

    # Получить активационный токен
    token = account_api.get_token_by_login(login=login, response=response)
    assert token, f'Токен для пользователя: {login} не был получен'

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, 'Пользователь не был активирован'

    # Авторизация
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, 'Пользователь не был авторизован'
