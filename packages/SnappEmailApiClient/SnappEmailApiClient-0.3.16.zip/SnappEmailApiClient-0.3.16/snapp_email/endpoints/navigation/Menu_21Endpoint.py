"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import Menu_21
from snapp_email.datacontract.utils import export_dict, fill


class Menu_21Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, impersonate_user_id=None, accept_type=None):
        """
        Retrieve options available for resource 'Menu_21'.
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Menu_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'navigation'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.menu-v5.17+json',
            'Accept': 'application/vnd.4thoffice.menu-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id)
        
        return fill(Menu_21, response.json())
    
    def get(self, streamId, menuScope, size, offset, badgeUnreadVersion=None, streamReadFilter=None, groupStreamOnly=None, impersonate_user_id=None, accept_type=None):
        """
        Get menu.
        
        :param streamId: 
        :type streamId: 
        
        :param menuScope: Specify menu scope. Available values are: 'Important', 'Others'.
        :type menuScope: String
        
        :param size: Specify size of requested page.
        :type size: Int32
        
        :param offset: Specify offset of requested page.
        :type offset: Int32
        
        :param badgeUnreadVersion: Version string that defines which logic to use for setting of unread badge count value on menu items and unread separator on feed. Available values are: 'V18', 'V19'.
        :type badgeUnreadVersion: String
        
        :param streamReadFilter: Search filter by stream read status. Available values are: 'All', 'Read', 'Unread'.
        :type streamReadFilter: String
        
        :param groupStreamOnly: Return group streams only.
        :type groupStreamOnly: Boolean
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Menu_21
        """
        url_parameters = {
            'menuScope': menuScope,
            'badgeUnreadVersion': badgeUnreadVersion,
            'streamReadFilter': streamReadFilter,
            'groupStreamOnly': groupStreamOnly,
            'size': size,
            'offset': offset,
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'navigation/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.menu-v5.17+json',
            'Accept': 'application/vnd.4thoffice.menu-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id)
        
        return fill(Menu_21, response.json())
    
    def get_2(self, streamId, impersonate_user_id=None, accept_type=None):
        """
        Get menu with selected items.
        
        :param streamId: Specify stream id
        :type streamId: String
        
        :param impersonate_user_id: 
        :type impersonate_user_id: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Menu_21
        """
        url_parameters = {
            'streamId': streamId,
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'navigation/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.menu-v5.17+json',
            'Accept': 'application/vnd.4thoffice.menu-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers, impersonate_user_id=impersonate_user_id)
        
        return fill(Menu_21, response.json())
