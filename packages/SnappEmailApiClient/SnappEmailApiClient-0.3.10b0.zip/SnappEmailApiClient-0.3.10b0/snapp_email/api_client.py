import json
import logging
import requests
from snapp_email import endpoints
from snapp_email.datacontract.utils import fill
from snapp_email.datacontract.classes import LogOnUser_14, Authentication_13, ClientApplication_14, AccessToken_14


DEFAULT_API_URL = 'https://api.4thoffice.com'
DEFAULT_USER_AGENT = 'ApiClient.py/0.3.9'
DEFAULT_CLIENT_CODENAME = 'SampleApp'
DEFAULT_CLIENT_VERSION = '0.1'
DEFAULT_ENABLE_COMPRESSION = True
DEFAULT_PER_PAGE = 10


class ApiClient(endpoints.ApiEndpoints):
    """
    Main class to be instantiated when accessing API.
    """

    def __init__(self, username, password, auth_type, impersonate_user_id=None, impersonate_only_once=False,
                 api_url=DEFAULT_API_URL, user_agent=DEFAULT_USER_AGENT,
                 client_codename=DEFAULT_CLIENT_CODENAME, client_version=DEFAULT_CLIENT_VERSION,
                 enable_compression=DEFAULT_ENABLE_COMPRESSION, per_page=DEFAULT_PER_PAGE):
        """
        :param username: str
        :param password: str
        :param auth_type: int
        :param api_url: str
        :param user_agent: str
        :param client_codename: str
        :param client_version: str
        :param enable_compression: bool
        :param per_page: int
        """

        # TODO Login with refresh token only?
        # TODO Use string (enum) instead of int for auth_type

        self.api_url = api_url
        self.user_agent = user_agent
        self.client_codename = client_codename
        self.client_version = client_version
        self.enable_compression = enable_compression
        self.paging_per_page = per_page

        self._token = None
        self._token_refresh_retry_count = 0
        self._login(username, password, auth_type)

        self.impersonate_user_id = impersonate_user_id
        self.impersonate_only_once = impersonate_only_once

    def _login(self, username, password, auth_type):
        # TODO Thread safe!
        logon_user = ApiClient.login(username, password, auth_type, self.api_url, self.user_agent,
                                     self.client_codename, self.client_version)
        self._token = logon_user.Token

    def _refresh_token(self):
        # TODO Check whether the access token expired and refresh it (once)
        # TODO Make this method thread-safe (so that two threads can't refresh it at the same time)
        print("Refreshing token")
        obj = self._token
        access_token_scope = ["Chat", "Stream", "Document"]
        self._token_refresh_retry_count += 1

        # Stash impersonate data
        old_impersonate_user_id = self.impersonate_user_id
        if self.impersonate_user_id:
            self.impersonate_user_id = None

        self._token = self.token.AccessToken_14.create(obj, access_token_scope)
        self._token_refresh_retry_count = 0

        # Stash pop impersonate data
        if old_impersonate_user_id:
            self.impersonate_user_id = old_impersonate_user_id

    def _get_headers_for_resource_type(self):
        pass

    def get_access_token(self):
        token = self._token.AccessToken
        return 'Bearer ' + token

    @staticmethod
    def login(auth_key, auth_secret, auth_type, api_url, user_agent, client_codename, client_version):
        """
        :param auth_key:
        :param auth_secret:
        :param auth_type:
        :param api_url:
        :param user_agent:
        :param client_codename:
        :param client_version:
        :return:
        :rtype: LogOnUser_14
        """
        # TODO How do I login without specifying logged in user?
        """
        obj = LogOnUser_14(
            Authentication=Authentication_13(auth_type, auth_key, auth_secret),
            ClientApplication=ClientApplication_14(0, client_version, client_codename)
        )
        c.user_session_logon.LogOnUser_14.create(obj)
        """

        endpoint = '{0}/{1}'.format(api_url, 'user/session/logon')
        response = requests.post(
            endpoint,
            headers={
                'Accept': 'application/vnd.4thoffice.logon.user-v4.0+json',
                'Content-Type': 'application/vnd.4thoffice.logon.user-v4.0+json',
                'User-Agent': user_agent,
            },
            data=json.dumps({
                "Authentication": {
                    "AuthenticationType": auth_type,
                    "AuthenticationId": auth_key,
                    "AuthenticationToken": auth_secret,
                },
                "ClientApplication": {
                    "Type": 0,
                    "Version": client_version,
                    "CodeName": client_codename,
                }
            })
        )
        response.raise_for_status()
        data = json.loads(response.text)
        return fill(LogOnUser_14, data)

    def api_call(self, http_verb, endpoint, url_parameters=None, additional_headers=None, data=None, token_refreshed=False):
        """
        :param self: ApiClient
        :param http_verb: str, get|post|put|delete|options
        :param endpoint: str
        :param url_parameters: dict
        :param additional_headers: dict
        :param data: dict
        :param token_refreshed: bool
        :return:
        """
        if url_parameters is None:
            url_parameters = {}
        if additional_headers is None:
            additional_headers = {}
        url = "{}/{}".format(self.api_url, endpoint)
        headers = {
            'User-Agent': self.user_agent,
            'Authorization': self.get_access_token(),
        }
        if self.enable_compression:
            headers['Accept-Encoding'] = 'gzip, deflate'
        for (k, v) in additional_headers.items():
            headers[k] = v
        if self.impersonate_user_id:  # TODO Do not impersonate for login/registration
            headers['X-Impersonate-User'] = self.impersonate_user_id
            if self.impersonate_only_once:
                self.impersonate_user_id = None
                self.impersonate_only_once = False

        method = getattr(requests, http_verb)

        try:
            response = method(url=url, params=url_parameters, headers=headers, data=data)
            response.raise_for_status()
        except requests.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401 and self._token_refresh_retry_count < 1:
                self._refresh_token()
                headers['Authorization'] = self.get_access_token()
                response = method(url=url, params=url_parameters, headers=headers, data=data)
                response.raise_for_status()
            else:
                raise

        return response

    def impersonate_user(self, user_id):
        self.impersonate_user_id = user_id
        self.impersonate_only_once = False

    def impersonate_once(self, user_id):
        self.impersonate_user_id = user_id
        self.impersonate_only_once = True

    def stop_impersonating_user(self):
        self.impersonate_user_id = None
        self.impersonate_only_once = False
