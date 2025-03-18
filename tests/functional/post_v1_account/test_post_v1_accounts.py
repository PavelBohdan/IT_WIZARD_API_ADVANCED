from dm_api_account.apis.account_api import AccountApi
from faker import Faker

fake = Faker()


def test_post_v1_account():

    account_api = AccountApi(host='http://5.63.153.31:5051')

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
