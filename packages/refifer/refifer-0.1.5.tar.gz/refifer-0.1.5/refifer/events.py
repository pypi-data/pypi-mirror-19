"""
Module which contains classes and other functionalities for handling 
events
"""
import uuid

from .exceptions import ValidationError

class Event(object):
    """
    Represents an event that will be sent to the notification service.
    This class uses validators to validate the payload of its instances.

    Validators are callables which takes an event as
    input and raises an exception if the payload could not
    be validated by the callable.
    """

    def __init__(self, name, payload={}, client_id=None, transaction_ref=None):
        self.name = name
        self.client_id = client_id
        self.payload = payload

        ref = transaction_ref if transaction_ref else str(uuid.uuid4())
        self.transaction_ref = ref

        self._validators = []

    def add_payload_validator(self, validator):
        self._validators.append(validator)

    def clear_validators(self):
        self._validators = []

    def get_data(self):
        data = {
            "client_id": self.client_id,
            "event_name": self.name,
            "transaction_reference": str(self.transaction_ref), 
            "payload": self.payload
        }

        return data

    def validate(self):
        try:
            for validator in self._validators:
                validator(self)
        except Exception as e:
            raise ValidationError(e)

class EventRegistration(object):
    """
    Class that represents the data used for registering events notification
    on the service.

    The registration payload can be set by users but the payload can also
    be build by adding events to the registration object using the 
    exposed methods.

    keyword Args:
        registration_payload(dict): an optional keyword arguement that 
            contains the payload that will be posted to the server.
        client_id(str): the id of the client the event is being registered
            for
    """

    def __init__(self, registration_payload={}, client_id=None):
        self._registration_payload = registration_payload
        self.client_id = client_id

    def set_registration_info(self, event_name, urls=None, emails=None, 
        sms_numbers=None):
        """
        Adds an event to the list of events that are to be registered, 
        including the url, email, or sms number that are to recieve 
        notifications about the event for a given client.

        Args:
            event_name(str): the code that uniquely identifies the event.

        Keyword Args:
            urls(list): (optional) a list of url for the endpoint that 
                will recieve the event.
            emails(list): (optional) a list of email that will be sent a 
                notification hen the event is fired.
            phone_numbers(list): (optional) a list of phone number that will be sent 
                a notification when the event is fired.
        """
        self._registration_payload = {}
        self._registration_payload["event_name"] = event_name
        self._registration_payload["callback_urls"] = urls
        self._registration_payload["emails"] = emails
        self._registration_payload["sms"] = sms_numbers

    def event_registration_data(self):
        """
        Prepares the data that will be posted to the notification
        service given the event codes that have been added to the
        instance.
        """
        return self._registration_payload

def picked_event_validator(event):
    """
    validator used for validating the fields of a `picked` event

    Args:
        event(Event): the event that is to be validated.
    """
    payload = event.payload
    if payload["status_code"] != "PCK":
        raise ValidationError("Status code for payload should be PCK.")

    if payload["status_name"] != "Picked":
        raise ValidationError("Status name is incorrect")