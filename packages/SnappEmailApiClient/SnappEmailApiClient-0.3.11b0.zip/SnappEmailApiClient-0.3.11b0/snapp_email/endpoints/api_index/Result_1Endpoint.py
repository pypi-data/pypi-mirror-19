"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import Result_1
from snapp_email.datacontract.utils import export_dict, fill


class Result_1Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'Result_1'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Result_1
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = ''.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.result-v1.9+json',
            'Accept': 'application/vnd.marg.bcsocial.result-v1.9+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(Result_1, response.json())
