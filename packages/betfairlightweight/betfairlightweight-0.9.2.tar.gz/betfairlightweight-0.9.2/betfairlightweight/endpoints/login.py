from requests import ConnectionError

from .baseendpoint import BaseEndpoint
from ..exceptions import LoginError, APIError
from ..utils import check_status_code


class Login(BaseEndpoint):

    _error = LoginError

    def __call__(self, session=None):
        response = self.request(self.url, session=session)
        response_json = response.json()
        self.client.set_session_token(response_json.get('sessionToken'))
        return response_json

    def request(self, method=None, params=None, session=None):
        session = session or self.client.session
        try:
            response = session.post(self.url, data=self.data, headers=self.client.login_headers, cert=self.client.cert)
        except ConnectionError:
            raise APIError(None, exception='ConnectionError')
        except Exception as e:
            raise APIError(None, exception=e)

        check_status_code(response)
        if self._error_handler:
            self._error_handler(response.json())
        return response

    def _error_handler(self, response, method=None, params=None):
        if response.get('loginStatus') != 'SUCCESS':
            raise self._error(response)

    @property
    def url(self):
        return '%s%s' % (self.client.identity_uri, 'certlogin')

    @property
    def data(self):
        return 'username=%s&password=%s' % (self.client.username, self.client.password)
