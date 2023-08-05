from .Appointment_20Endpoint import Appointment_20Endpoint
from .Appointment_22Endpoint import Appointment_22Endpoint


class AppointmentEndpoint:
    def __init__(self, api_client):
        self._api_client = api_client

    @property
    def Appointment_20(self):
        """
        :return: Appointment_20Endpoint
        """
        return Appointment_20Endpoint(self._api_client)
        
    @property
    def Appointment_22(self):
        """
        :return: Appointment_22Endpoint
        """
        return Appointment_22Endpoint(self._api_client)
        