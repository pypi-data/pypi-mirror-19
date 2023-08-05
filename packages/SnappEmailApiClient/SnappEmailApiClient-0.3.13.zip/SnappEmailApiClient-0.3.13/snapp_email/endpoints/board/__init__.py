from .ListOfBoardsPage_22Endpoint import ListOfBoardsPage_22Endpoint
from .ListOfBoardsPage_21Endpoint import ListOfBoardsPage_21Endpoint
from .ListOfBoardsPage_20Endpoint import ListOfBoardsPage_20Endpoint
from .ListOfBoardsPage_15Endpoint import ListOfBoardsPage_15Endpoint
from .ListOfBoards_15Endpoint import ListOfBoards_15Endpoint


class BoardEndpoint:
    def __init__(self, api_client):
        self._api_client = api_client

    @property
    def ListOfBoardsPage_22(self):
        """
        :return: ListOfBoardsPage_22Endpoint
        """
        return ListOfBoardsPage_22Endpoint(self._api_client)
        
    @property
    def ListOfBoardsPage_21(self):
        """
        :return: ListOfBoardsPage_21Endpoint
        """
        return ListOfBoardsPage_21Endpoint(self._api_client)
        
    @property
    def ListOfBoardsPage_20(self):
        """
        :return: ListOfBoardsPage_20Endpoint
        """
        return ListOfBoardsPage_20Endpoint(self._api_client)
        
    @property
    def ListOfBoardsPage_15(self):
        """
        :return: ListOfBoardsPage_15Endpoint
        """
        return ListOfBoardsPage_15Endpoint(self._api_client)
        
    @property
    def ListOfBoards_15(self):
        """
        :return: ListOfBoards_15Endpoint
        """
        return ListOfBoards_15Endpoint(self._api_client)
        