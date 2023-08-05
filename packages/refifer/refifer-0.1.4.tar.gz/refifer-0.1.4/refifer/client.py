"""
Module used for connecting with the fetchr's notification service.
This module uses the request library extensively and the responses are
usually requests.Response objects
"""
import json
import uuid

import requests 
from requests.exceptions import HTTPError

from .constants import RETRY_COUNT, REGISTRATION_ENDPOINT, FIRE_ENDPOINT
from .exceptions import RefiferError
from .events import Event, EventRegistration

class Refifer(object):
    """
    Class used for making api calls to fetchr's notification service and
    also for registering and pushing events.

    Args:
        access_token(str): the access_token that was gotten from the
            authentication service.

    Kwargs:
        retry_count(int): the number of times a request will be retried on
            error.
        timeout(int): the number of seconds the request should wait before
            timing-out the request.
        proxies(dict): proxy configurations as used by the request lib
    """

    def __init__(self, access_token, retry_count=RETRY_COUNT, 
        timeout=None, proxies=None):

        self.access_token = access_token
        self.timeout = timeout
        self.proxies = proxies
        self.retry_count = retry_count
        self.session = requests.Session()

    def _prepare_headers(self, client_id, content_type="application/json", *args, **kwargs):
        headers =  {"Content-Type": content_type, 
            "X-Client-ID": client_id if client_id else "",
            "Authorization": "Bearer " + str(self.access_token)}
        headers.update(kwargs)
        return headers

    def _make_registration(self, event_name, event_codes):
        """
        register a client to recieve notification for the various event 
        codes
        """
        pass

    def _build_endpoint(self, resource_url=""):
        if resource_url[0] != "/":
            resource_url = "/" + resource_url
        return BASE_API_ENDPOINT + resource_url

    def __call__(self, client_id, event_name, payload={}, transaction_ref=None):
        return self.fire(client_id, event_name, payload=payload, 
            transaction_ref=transaction_ref)

    def request(self, endpoint, args=None, post_args=None, method=None, 
        client_id=None):
        """
        Makes a request to the notifications api and returns the response.
        if post_args are available, it makes a post request to the server.

        Args:
            endpoint(str): the url endpoint to make the request on

        Kwargs:
            args(dict): url parameters structured as a dict

            post_args(dict): data to be submitted to the server as form data

            method(str): http method that will be used for the request

            client_id(str): the client_id for the client making the request
        
        Returns:
            response(requests.Response): a Response object that was the 
                result of the call to the server.
        """
        if post_args:
            method = "POST"

        try:
            headers = self._prepare_headers(client_id)
            return self.session.request(method, endpoint, params=args, 
                data=post_args, timeout=self.timeout, proxies=self.proxies,
                headers=headers)

        except HTTPError as e:
            response = json.loads(e.read())
            raise RefiferError(response)

    def client_registration_data(self, client_id, event_name):
        """
        Gets the events notification registration details for the client
        who owns the client_id used in instantiating this class.

        Args:
            client_id(str): the client_id of the client
            event_name(str): the name of the event whose registration 
                details is to be gotten from the server.

        Returns:
            registration_data(dict): the registration data that was used
                in registering the event with the given name for the client.
        """
        endpoint = REGISTRATION_ENDPOINT + "/" + client_id
        reg_response = self.request(endpoint, method="GET", client_id=client_id).content
        reg_response = json.loads(reg_response)

        for data in reg_response["data"]:
            if data["event_name"] == event_name:
                return data


    def register_event(self, client_id, event_registration):
        """
        Registers an event with the server and provides a list of endpoints
        that are to broadcasted to when the event is fired.

        Args:
            client_id(str): the client_id of the client
            event_regisration(EventRegistration): the object that encapsulates
                the registration of an event.

        Returns:
            response(requests.Response); the Response object which is the 
                result of registering an event.
        """
        data = event_registration.event_registration_data()

        try:
            return self.request(REGISTRATION_ENDPOINT,
                post_args=json.dumps(data), method="POST", client_id=client_id)
        except HTTPError as e:
            raise RefiferError(e)


    def register(self, client_id, registration_payload):
        """
        Makes an event registration request with a raw payload

        Args:
            client_id(str): the client_id of the client
            registration_payload(dict): a json serializable dict containing
                the raw payload that will be submitted to the regostration
                endpoint
        """
        event_registraton = EventRegistration(registration_payload)
        return self.register_event(client_id, event_registration)


    def fire_event(self, client_id, event, transaction_ref=None):
        """
        Publishes an event to the server providing the payload that should
        be broadcasted to the registed endpoints for the event.

        Args:
            client_id(str): the client_id of the client
            event(Event): the event that should be fired

        kwargs:
            transaction_ref(str): transaction reference key

        Returns:
            response(requests.Response): response gotten from firing event
        """
        data = event.get_data()
        data_ref = data.get("transaction_reference", None)
        ref = data_ref if data_ref else transaction_ref
        if not ref:
            ref = str(uuid.uuid4())

        data["transaction_reference"] = ref

        data = json.dumps(data)

        try:
            return self.request(FIRE_ENDPOINT, client_id=client_id, post_args=data, 
                method="POST")
        except HTTPError as e:
            raise RefiferError(e)


    def fire(self, client_id, event_name, payload={}, transaction_ref=None):
        """
        Publishes an event but builds an event object for you.

        Args:
            client_id(str): the client_id of the client
            event_name(str): the name of the event

        Kwargs:
            payload(dict): the payload for the events being fired
            transaction_ref(str): the transaction reference for the event
        """
        ref = transaction_ref if transaction_ref else str(uuid.uuid4())
        event = Event(event_name, payload=payload, transaction_ref=ref)

        return self.fire_event(client_id, event)

    def unsubscribe_client(self, client_id):
        """
        Unsubscribes the client from events notifications.

        Args:
            client_id(str): the client_id of the client
        """
        return self.request(REGISTRATION_ENDPOINT, 
            client_id=client_id, method="DELETE")
