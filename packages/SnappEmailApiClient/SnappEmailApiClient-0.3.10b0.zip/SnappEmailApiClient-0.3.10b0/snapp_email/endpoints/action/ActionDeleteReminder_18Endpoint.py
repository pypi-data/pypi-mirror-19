"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ActionDeleteReminder_18
from snapp_email.datacontract.utils import export_dict, fill


class ActionDeleteReminder_18Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'ActionDeleteReminder_18'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ActionDeleteReminder_18
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'action'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.action.delete.reminder-v5.8+json',
            'Accept': 'application/vnd.4thoffice.action.delete.reminder-v5.8+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ActionDeleteReminder_18, response.json())
    
    def create(self, obj, accept_type=None):
        """
        Delete reminder on arbitrary resuource.
        
        :param obj: Object to be persisted
        :type obj: ActionDeleteReminder_18
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ActionDeleteReminder_18
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'action'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.action.delete.reminder-v5.8+json',
            'Accept': 'application/vnd.4thoffice.action.delete.reminder-v5.8+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(ActionDeleteReminder_18, response.json())
