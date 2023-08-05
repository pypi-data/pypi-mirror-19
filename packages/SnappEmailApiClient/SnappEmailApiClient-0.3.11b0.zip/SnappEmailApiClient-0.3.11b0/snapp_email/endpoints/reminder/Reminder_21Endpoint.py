"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import Reminder_21
from snapp_email.datacontract.utils import export_dict, fill


class Reminder_21Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'Reminder_21'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Reminder_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'reminder'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.base-v5.17+json',
            'Accept': 'application/vnd.4thoffice.reminder.base-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(Reminder_21, response.json())
    
    def get(self, reminderId, accept_type=None):
        """
        Get reminder
        
        :param reminderId: 
        :type reminderId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Reminder_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'reminderId': reminderId,
        }
        endpoint = 'reminder/{reminderId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.base-v5.17+json',
            'Accept': 'application/vnd.4thoffice.reminder.base-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(Reminder_21, response.json())
    
    def create(self, obj, accept_type=None):
        """
        Create reminder
        
        :param obj: Object to be persisted
        :type obj: Reminder_21
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Reminder_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'reminder'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.base-v5.17+json',
            'Accept': 'application/vnd.4thoffice.reminder.base-v5.17+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(Reminder_21, response.json())
    
    def delete(self, reminderId, accept_type=None):
        """
        Delete reminder
        
        :param reminderId: 
        :type reminderId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: True if object was deleted, otherwise an exception is raised
        :rtype: bool
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'reminderId': reminderId,
        }
        endpoint = 'reminder/{reminderId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.base-v5.17+json',
            'Accept': 'application/vnd.4thoffice.reminder.base-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('delete', endpoint, url_parameters, add_headers)
        
        return True
