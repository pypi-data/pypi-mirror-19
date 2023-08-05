"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import StreamGroup_22
from snapp_email.datacontract.utils import export_dict, fill


class StreamGroup_22Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'StreamGroup_22'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamGroup_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'stream'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.group-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.group-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(StreamGroup_22, response.json())
    
    def get(self, streamId, accept_type=None):
        """
        Get stream resource.
        
        :param streamId: 
        :type streamId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamGroup_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'stream/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.group-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.group-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(StreamGroup_22, response.json())
    
    def create(self, obj, accept_type=None):
        """
        Create stream resource.
        
        :param obj: Object to be persisted
        :type obj: StreamGroup_22
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamGroup_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'stream'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.group-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.group-5.18+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(StreamGroup_22, response.json())
    
    def update(self, obj, streamId, accept_type=None):
        """
        Update stream resource.
        
        :param obj: Object to be persisted
        :type obj: StreamGroup_22
        
        :param streamId: 
        :type streamId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamGroup_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'stream/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.group-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.group-5.18+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(StreamGroup_22, response.json())
