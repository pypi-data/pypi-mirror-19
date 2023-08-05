"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import UserSettingsNotification_20
from snapp_email.datacontract.utils import export_dict, fill


class UserSettingsNotification_20Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'UserSettingsNotification_20'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserSettingsNotification_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.settings.notification-5.15+json',
            'Accept': 'application/vnd.4thoffice.user.settings.notification-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(UserSettingsNotification_20, response.json())
    
    def get(self, accept_type=None):
        """
        Get user settings resource.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserSettingsNotification_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.settings.notification-5.15+json',
            'Accept': 'application/vnd.4thoffice.user.settings.notification-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(UserSettingsNotification_20, response.json())
    
    def update(self, obj, accept_type=None):
        """
        Update user settings resource.
        
        :param obj: Object to be persisted
        :type obj: UserSettingsNotification_20
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserSettingsNotification_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.settings.notification-5.15+json',
            'Accept': 'application/vnd.4thoffice.user.settings.notification-5.15+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(UserSettingsNotification_20, response.json())
