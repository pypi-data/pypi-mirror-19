"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ListOfBoards_15
from snapp_email.datacontract.utils import export_dict, fill


class ListOfBoards_15Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'ListOfBoards_15'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfBoards_15
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'board'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.list-v5.0+json',
            'Accept': 'application/vnd.4thoffice.board.list-v5.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ListOfBoards_15, response.json())
    
    def update(self, obj, accept_type=None):
        """
        Batch update of board list.
        
        :param obj: Object to be persisted
        :type obj: ListOfBoards_15
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfBoards_15
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'board'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.list-v5.0+json',
            'Accept': 'application/vnd.4thoffice.board.list-v5.0+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(ListOfBoards_15, response.json())
