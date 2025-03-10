import requests
from requests import Response
from json import loads


class AccountApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data: dict):
        """
        Register new user

        Args:
            json_data (dict)
        """
        response = requests.post(
            url=f'{self.host}/v1/account', json=json_data)
        return response

    def put_v1_account_email(self, json_data: dict):
        """
        Change registered user email

        Args:
            json_data (dict)
        """
        response = requests.put(
            url=f'{self.host}/v1/account/email', json=json_data)
        return response

    def put_v1_account_token(self, token: str):
        """
        Activate registered user

        Args:
            token (str)
        """
        response = requests.put(
            url=f'{self.host}/v1/account/{token}')
        return response

    def get_token_by_login(self, login: str, response: Response):
        """
        Get token from created user

        Args:
            login (str)
            response (Response)
        """
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']

            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/').pop()
                break
        assert token, f'Токен для пользователя: {login} не был получен'
        return token
