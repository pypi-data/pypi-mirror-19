import random
import string

import requests
from django.contrib.auth.models import User


class OAuthProvider:
    authorization_endpoint = "https://example.com/oauth/authorize"
    token_endpoint = "https://example.com/oauth/token"

    def __init__(self, app_id, app_secret):
        self.app_secret = app_secret
        self.app_id = app_id

    @property
    def authorization_url(self):
        return self.get_authorization_url()

    def retrieve_token(self, code, callback_url="", **params):
        r_params = self._get_token_request_params(callback_url, code)
        r_params.update(params)
        request = requests.post(self.token_endpoint, data=r_params)
        return request.json()

    def _get_token_request_params(self, callback_url, code):
        return {'client_id': self.app_id, 'grant_type': 'authorization_code', 'redirect_uri': callback_url,
                'code': code}

    def get_authorization_url(self, **params):
        r_params = self._get_authorization_params()
        r_params.update(params)
        return requests.Request(method='GET', url=self.authorization_endpoint, params=r_params).prepare().url

    def _get_authorization_params(self):
        return {'client_id': self.app_id, 'response_type': 'code'}

    @staticmethod
    def login_with_token(access_token, service):
        return None


class MicrosoftOAuthProvider(OAuthProvider):
    authorization_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    token_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    GRAPH_API = 'https://graph.microsoft.com/v1.0'

    def _get_token_request_params(self, callback_url, code):
        defaults = super()._get_token_request_params(callback_url, code)
        del defaults['redirect_uri']
        defaults['client_secret'] = self.app_secret
        return defaults

    def _get_authorization_params(self):
        default = super()._get_authorization_params()
        default['scope'] = 'User.Read'
        return default

    @staticmethod
    def graph(resource):
        return "{}{}".format(MicrosoftOAuthProvider.GRAPH_API, resource)

    @staticmethod
    def login_with_token(access_token, service):
        graph_user = requests.get(
            MicrosoftOAuthProvider.graph('/me'),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)
            }).json()

        from account.models import OAuthToken
        try:
            token = OAuthToken.objects.get(uuid=graph_user['id'], service=service)
            token.auth_token = access_token
            token.save()
            return token.user
        except OAuthToken.DoesNotExist:
            token = OAuthToken(uuid=graph_user['id'], service=service)
            token.auth_token = access_token
        try:
            user = User.objects.get(email=graph_user['mail'])
        except User.DoesNotExist:
            user = User(email=graph_user['mail'],
                        username=graph_user['mail'],
                        first_name=graph_user['givenName'],
                        last_name=graph_user['surname'],
                        password="".join(random.choice(string.printable) for _ in range(10))
                        )
            user.save()
        token.user = user
        token.save()
        return user
