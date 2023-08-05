"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ListOfNotificationsPage_15
from snapp_email.datacontract.utils import export_dict, fill


class ListOfNotificationsPage_15Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'ListOfNotificationsPage_15'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfNotificationsPage_15
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'notification'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.notification.list.page-v5.0+json',
            'Accept': 'application/vnd.4thoffice.notification.list.page-v5.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ListOfNotificationsPage_15, response.json())
    
    def get(self, size, offset, longPolling, sinceId=None, accept_type=None):
        """
        Get notification list.
        
        :param size: Specify size of requested page.
        :type size: Int32
        
        :param offset: Specify offset of requested page.
        :type offset: Int32
        
        :param longPolling: Perform long polling while reading the resource.
        :type longPolling: Boolean
        
        :param sinceId: Specify since id. That is an id of a resource from which incremental list load should take place.
        :type sinceId: String
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfNotificationsPage_15
        """
        url_parameters = {
            'sinceId': sinceId,
            'size': size,
            'offset': offset,
            'longPolling': longPolling,
        }
        endpoint_parameters = {
        }
        endpoint = 'notification'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.notification.list.page-v5.0+json',
            'Accept': 'application/vnd.4thoffice.notification.list.page-v5.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(ListOfNotificationsPage_15, response.json())
