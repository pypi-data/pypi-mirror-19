from .Menu_22Endpoint import Menu_22Endpoint
from .Menu_21Endpoint import Menu_21Endpoint
from .Menu_20Endpoint import Menu_20Endpoint


class NavigationEndpoint:
    def __init__(self, api_client):
        self._api_client = api_client

    @property
    def Menu_22(self):
        """
        :return: Menu_22Endpoint
        """
        return Menu_22Endpoint(self._api_client)
        
    @property
    def Menu_21(self):
        """
        :return: Menu_21Endpoint
        """
        return Menu_21Endpoint(self._api_client)
        
    @property
    def Menu_20(self):
        """
        :return: Menu_20Endpoint
        """
        return Menu_20Endpoint(self._api_client)
        