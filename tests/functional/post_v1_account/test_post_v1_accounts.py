from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailHogApi


def test_post_v1_account():

    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailHogApi(host='http://5.63.153.31:5025')

    # Регистрация пользователя
    login: str = 'pavel10'
    password: str = '12345678'
    email: str = f'{login}@mail.com'
    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }
    response = account_api.post_v1_account(json_data=json_data)

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()

    # Получить активационный токен
    token = account_api.get_token_by_login(login=login, response=response)

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)

    # Авторизация
    response = login_api.post_v1_account_login(json_data=json_data)
