"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import Appointment_20
from snapp_email.datacontract.utils import export_dict, fill


class Appointment_20Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'Appointment_20'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Appointment_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'appointment'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.appointment-v5.15+json',
            'Accept': 'application/vnd.4thoffice.appointment-v5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(Appointment_20, response.json())
    
    def get(self, appointmentId, accept_type=None):
        """
        Retrieve appointment resource.
        
        :param appointmentId: 
        :type appointmentId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Appointment_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'appointmentId': appointmentId,
        }
        endpoint = 'appointment/{appointmentId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.appointment-v5.15+json',
            'Accept': 'application/vnd.4thoffice.appointment-v5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(Appointment_20, response.json())
