"""
Module used for connecting with the fetchr's notification service.
This module uses the request library extensively and the responses are
usually requests.Response objects
"""
import json
import uuid

import requests 
from requests.exceptions import HTTPError

from .constants import RETRY_COUNT, BASE_API_ENDPOINT, FIRE_ENDPOINT
from .exceptions import RefiferError
from .events import Event, EventRegistration

class Refifer(object):
    """
    Class used for making api calls to fetchr's notification service and
    also for registering and pushing events.

    Args:
        client_id(str): the client_id that uniquely identifies the client
            making the request.

        access_token(str): the access_token that was gotten from the
            authentication service.

    Kwargs:
        retry_count(int): the number of times a request will be retried on
            error.
        timeout(int): the number of seconds the request should wait before
            timing-out the request.
        proxies(dict): proxy configurations as used by the request lib
    """

    def __init__(self, client_id, access_token, retry_count=RETRY_COUNT, 
        timeout=None, proxies=None):

        self.client_id = client_id
        self.access_token = access_token
        self.timeout = timeout
        self.proxies = proxies
        self.retry_count = retry_count
        self.session = requests.Session()

    def _prepare_headers(self, content_type="application/json"):
        return {"Content-Type": content_type, 
            "X-Client-ID": self.client_id, 
            "Authorization": "Bearer " + str(self.access_token)}

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

    def __call__(self, event_name, payload={}, transaction_ref=None):
        return self.fire(event_name, payload=payload, 
            transaction_ref=transaction_ref)

    def request(self, endpoint, args=None, post_args=None, method=None):
        """
        Makes a request to the notifications api and returns the response.
        if post_args are available, it makes a post request to the server.

        Args:
            endpoint(str): the url endpoint to make the request on

        Kwargs:
            args(dict): url parameters structured as a dict

            post_args(dict): data to be submitted to the server as form data

            method(str): http method that will be used for the request
        
        Returns:
            response(requests.Response): a Response object that was the 
                result of the call to the server.
        """
        if post_args:
            method = "POST"

        try:
            headers = self._prepare_headers()
            return self.session.request(method, endpoint, params=args, 
                data=post_args, timeout=self.timeout, proxies=self.proxies,
                headers=headers)

        except HTTPError as e:
            response = json.loads(e.read())
            raise RefiferError(response)

    def client_registration_data(self, event_name):
        """
        Gets the events notification registration details for the client
        who owns the client_id used in instantiating this class.

        Args:
            event_name(str): the name of the event whose registration 
                details is to be gotten from the server.

        Returns:
            registration_data(dict): the registration data that was used
                in registering the event with the given name for the client.
        """
        endpoint = self._build_endpoint("notifications/" + str(self.client_id))
        reg_response = self.request(endpoint, method="GET").content
        reg_response = json.loads(reg_response)

        for data in reg_response["data"]:
            if data["event_name"] == event_name:
                return data


    def register_event(self, event_registration):
        """
        Registers an event with the server and provides a list of endpoints
        that are to broadcasted to when the event is fired.

        Args:
            event_regisration(EventRegistration): the object that encapsulates
                the registration of an event.

        Returns:
            response(requests.Response); the Response object which is the 
                result of registering an event.
        """
        data = event_registration.event_registration_data()

        try:
            return self.request(BASE_API_ENDPOINT + "/notifications",
                post_args=json.dumps(data), method="POST")
        except HTTPError as e:
            raise RefiferError(e)


    def fire_event(self, event, transaction_ref=None):
        """
        Publishes an event to the server providing the payload that should
        be broadcasted to the registed endpoints for the event.

        Args:
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
            return self.request(FIRE_ENDPOINT, post_args=data, 
                method="POST")
        except HTTPError as e:
            raise RefiferError(e)


    def fire(self, event_name, payload={}, transaction_ref=None):
        """
        Publishes an event but builds an event object for you.
        """
        ref = transaction_ref if transaction_ref else str(uuid.uuid4())
        event = Event(event_name, payload=payload, transaction_ref=ref)

        return self.fire_event(event)

    def unsubscribe_client(self):
        """
        Unsubscribes the client from events notifications.
        """
        return self.request(BASE_API_ENDPOINT + "/notifications", method="DELETE")
