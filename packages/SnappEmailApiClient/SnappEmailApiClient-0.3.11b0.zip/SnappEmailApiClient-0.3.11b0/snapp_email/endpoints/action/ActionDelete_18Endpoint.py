"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ActionDelete_18
from snapp_email.datacontract.utils import export_dict, fill


class ActionDelete_18Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'ActionDelete_18'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ActionDelete_18
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'action'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.action.delete-v5.8+json',
            'Accept': 'application/vnd.4thoffice.action.delete-v5.8+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ActionDelete_18, response.json())
    
    def create(self, obj, accept_type=None):
        """
        Action to delete arbitrary resource.
        
        :param obj: Object to be persisted
        :type obj: ActionDelete_18
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ActionDelete_18
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'action'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.action.delete-v5.8+json',
            'Accept': 'application/vnd.4thoffice.action.delete-v5.8+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(ActionDelete_18, response.json())
