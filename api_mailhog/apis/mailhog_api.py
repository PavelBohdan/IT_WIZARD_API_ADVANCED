import requests


class MailHogApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def get_api_v2_messages(self, limit: int = 50):
        """
        Get user emails

        Args:
            limit (int, optional): Defaults to 50.
        """
        params = {
            'limit': limit,
        }

        response = requests.get(url=f'{self.host}/api/v2/messages',
                                params=params, verify=False)
        return response
