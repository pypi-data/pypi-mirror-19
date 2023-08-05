"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ListOfBoardsPage_22
from snapp_email.datacontract.utils import export_dict, fill


class ListOfBoardsPage_22Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'ListOfBoardsPage_22'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfBoardsPage_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'board'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.list.page-v5.18+json',
            'Accept': 'application/vnd.4thoffice.board.list.page-v5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ListOfBoardsPage_22, response.json())
    
    def get(self, size, offset, boardType=None, accept_type=None):
        """
        Retrieve list of board resources.
        
        :param size: Specify size of requested page.
        :type size: Int32
        
        :param offset: Specify offset of requested page.
        :type offset: Int32
        
        :param boardType: Filter by type of board.
            Available values:
            - UserGenerated
            - System
        :type boardType: String
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfBoardsPage_22
        """
        url_parameters = {
            'boardType': boardType,
            'size': size,
            'offset': offset,
        }
        endpoint_parameters = {
        }
        endpoint = 'board'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.list.page-v5.18+json',
            'Accept': 'application/vnd.4thoffice.board.list.page-v5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(ListOfBoardsPage_22, response.json())
