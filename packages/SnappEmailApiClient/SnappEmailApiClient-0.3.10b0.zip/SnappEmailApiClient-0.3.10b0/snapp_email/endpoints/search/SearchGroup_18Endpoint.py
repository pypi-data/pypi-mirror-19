"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import SearchGroup_18
from snapp_email.datacontract.utils import export_dict, fill


class SearchGroup_18Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'SearchGroup_18'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: SearchGroup_18
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'search'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.search.group-v5.8+json',
            'Accept': 'application/vnd.4thoffice.search.group-v5.8+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(SearchGroup_18, response.json())
    
    def get(self, searchGroupId, size, offset, searchQuery=None, searchScope=None, sort=None, sortDirection=None, accept_type=None):
        """
        Retrieve grouped search results.
        
        :param searchGroupId: Specify search scope
        :type searchGroupId: String
        
        :param size: Specify size of requested page.
        :type size: Int32
        
        :param offset: Specify offset of requested page.
        :type offset: Int32
        
        :param searchQuery: Specify search query.
        :type searchQuery: String
        
        :param searchScope: Specify search scope. Available values are: 'All', 'Hidden', 'Important'.
        :type searchScope: String
        
        :param sort: Specify sort id.
        :type sort: String
        
        :param sortDirection: Specify sort direction.
            Available values:
            - Ascending
            - Descending
        :type sortDirection: String
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: SearchGroup_18
        """
        url_parameters = {
            'searchQuery': searchQuery,
            'searchScope': searchScope,
            'searchGroupId': searchGroupId,
            'sort': sort,
            'sortDirection': sortDirection,
            'size': size,
            'offset': offset,
        }
        endpoint_parameters = {
        }
        endpoint = 'search'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.search.group-v5.8+json',
            'Accept': 'application/vnd.4thoffice.search.group-v5.8+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(SearchGroup_18, response.json())
