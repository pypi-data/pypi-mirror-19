import uuid
import json
import datetime
import unittest2

import pytest
import requests
from mock import patch

from .helper import DUMMY_CUSTOMER, DUMMY_DESTINATION, DUMMY_FLEET, DUMMY_DRIVER
from .helper import DUMMY_HUB, DUMMY_TASK, DUMMY_TRIP, DUMMY_GPSLOG, DUMMY_EVENT
from .helper import DUMMY_NEIGHBORHOOD

from hypertrack.resource import HyperTrackObject
from hypertrack.resource import Trip, GPSLog, Event, APIResource, Neighborhood
from hypertrack.resource import Customer, Destination, Fleet, Driver, Hub, Task
from hypertrack.exceptions import InvalidRequestException, RateLimitException
from hypertrack.exceptions import APIConnectionException, APIException
from hypertrack.exceptions import AuthenticationException


class MockResponse(object):
    '''
    Mock API responses
    '''
    def __init__(self, status_code, content, headers=None):
        self.status_code = status_code
        self.content = content
        self.headers = None

    def json(self):
        return json.loads(self.content)


class HyperTrackObjectTests(unittest2.TestCase):
    '''
    Test the base hypertrack object
    '''
    def test_hypertrack_id(self):
        hypertrack_id = str(uuid.uuid4())
        ht = HyperTrackObject(id=hypertrack_id)
        self.assertEqual(ht.hypertrack_id, hypertrack_id)

    def test_str_representation(self):
        hypertrack_id = str(uuid.uuid4())
        ht = HyperTrackObject(id=hypertrack_id)
        self.assertEqual(str(ht), json.dumps({'id': hypertrack_id}, sort_keys=True, indent=2))

    def test_raise_attribute_error_for_private_attribute(self):
        hypertrack_id = str(uuid.uuid4())
        ht = HyperTrackObject(id=hypertrack_id, _blah='blah')

        with pytest.raises(AttributeError):
            ht._blah

    def test_raise_attribute_error_for_non_existing_key(self):
        hypertrack_id = str(uuid.uuid4())
        ht = HyperTrackObject(id=hypertrack_id)

        with pytest.raises(AttributeError):
            ht.blah

    def test_object_representation(self):
        hypertrack_id = str(uuid.uuid4())
        ht = HyperTrackObject(id=hypertrack_id)
        self.assertEqual(repr(ht), ht.__repr__())


class APIResourceTests(unittest2.TestCase):
    '''
    Test base resource methods
    '''
    def test_make_request_successful(self):
        response = MockResponse(200, json.dumps({}))
        method = 'get'
        url = 'http://example.com'
        headers = APIResource._get_headers()
        data = {'test_data': 'data123'}
        params = {'test_params': 'params123'}
        files = None
        timeout = 20

        with patch.object(requests, 'request', return_value=response) as mock_request:
            APIResource._make_request(method, url, data, params, files)
            mock_request.assert_called_once_with(method, url, headers=headers,
                                                 data=json.dumps(data),
                                                 params=params, files=files,
                                                 timeout=timeout)

    def test_make_request_connection_error(self):
        response = MockResponse(200, json.dumps({}))
        method = 'get'
        url = 'http://example.com'
        headers = APIResource._get_headers()
        data = {'test_data': 'data123'}
        params = {'test_params': 'params123'}
        files = None
        timeout = 20

        with patch.object(requests, 'request', return_value=response) as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError

            with pytest.raises(APIConnectionException):
                APIResource._make_request(method, url, data, params, files)

            mock_request.assert_called_once_with(method, url, headers=headers,
                                                 data=json.dumps(data),
                                                 params=params, files=files,
                                                 timeout=timeout)

    def test_make_request_timeout(self):
        response = MockResponse(200, json.dumps({}))
        method = 'get'
        url = 'http://example.com'
        headers = APIResource._get_headers()
        data = {'test_data': 'data123'}
        params = {'test_params': 'params123'}
        files = None
        timeout = 20

        with patch.object(requests, 'request', return_value=response) as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout

            with pytest.raises(APIConnectionException):
                APIResource._make_request(method, url, data, params, files)

            mock_request.assert_called_once_with(method, url, headers=headers,
                                                 data=json.dumps(data),
                                                 params=params, files=files,
                                                 timeout=timeout)

    def test_make_request_invalid_request(self):
        response = MockResponse(400, json.dumps({}))
        method = 'post'
        url = 'http://example.com'
        headers = APIResource._get_headers()
        data = {'test_data': 'data123'}
        params = {'test_params': 'params123'}
        files = None
        timeout = 20

        with patch.object(requests, 'request', return_value=response) as mock_request:

            with pytest.raises(InvalidRequestException):
                APIResource._make_request(method, url, data, params, files)

            mock_request.assert_called_once_with(method, url, headers=headers,
                                                 data=json.dumps(data),
                                                 params=params, files=files,
                                                 timeout=timeout)

    def test_make_request_resource_does_not_exist(self):
        response = MockResponse(404, json.dumps({}))
        method = 'post'
        url = 'http://example.com'
        headers = APIResource._get_headers()
        data = {'test_data': 'data123'}
        params = {'test_params': 'params123'}
        files = None
        timeout = 20

        with patch.object(requests, 'request', return_value=response) as mock_request:

            with pytest.raises(InvalidRequestException):
                APIResource._make_request(method, url, data, params, files)

            mock_request.assert_called_once_with(method, url, headers=headers,
                                                 data=json.dumps(data),
                                                 params=params, files=files,
                                                 timeout=timeout)

    def test_make_request_authentication_error(self):
        response = MockResponse(401, json.dumps({}))
        method = 'post'
        url = 'http://example.com'
        headers = APIResource._get_headers()
        data = {'test_data': 'data123'}
        params = {'test_params': 'params123'}
        files = None
        timeout = 20

        with patch.object(requests, 'request', return_value=response) as mock_request:

            with pytest.raises(AuthenticationException):
                APIResource._make_request(method, url, data, params, files)

            mock_request.assert_called_once_with(method, url, headers=headers,
                                                 data=json.dumps(data),
                                                 params=params, files=files,
                                                 timeout=timeout)

    def test_make_request_rate_limit_exception(self):
        response = MockResponse(429, json.dumps({}))
        method = 'post'
        url = 'http://example.com'
        headers = APIResource._get_headers()
        data = {'test_data': 'data123'}
        params = {'test_params': 'params123'}
        files = None
        timeout = 20

        with patch.object(requests, 'request', return_value=response) as mock_request:

            with pytest.raises(RateLimitException):
                APIResource._make_request(method, url, data, params, files)

            mock_request.assert_called_once_with(method, url, headers=headers,
                                                 data=json.dumps(data),
                                                 params=params, files=files,
                                                 timeout=timeout)

    def test_make_request_unhandled_exception(self):
        response = MockResponse(500, json.dumps({}))
        method = 'post'
        url = 'http://example.com'
        headers = APIResource._get_headers()
        data = {'test_data': 'data123'}
        params = {'test_params': 'params123'}
        files = None
        timeout = 20

        with patch.object(requests, 'request', return_value=response) as mock_request:

            with pytest.raises(APIException):
                APIResource._make_request(method, url, data, params, files)

            mock_request.assert_called_once_with(method, url, headers=headers,
                                                 data=json.dumps(data),
                                                 params=params, files=files,
                                                 timeout=timeout)


class CustomerTests(unittest2.TestCase):
    '''
    Test customer methods
    '''
    def test_create_customer(self):
        response = MockResponse(201, json.dumps(DUMMY_CUSTOMER))

        with patch.object(Customer, '_make_request', return_value=response) as mock_request:
            customer = Customer.create(**DUMMY_CUSTOMER)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/customers/', data=DUMMY_CUSTOMER, files=None)

    def test_retrieve_customer(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_CUSTOMER))

        with patch.object(Customer, '_make_request', return_value=response) as mock_request:
            customer = Customer.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/customers/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_update_customer(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_CUSTOMER))

        with patch.object(Customer, '_make_request', return_value=response) as mock_request:
            customer = Customer(id=hypertrack_id, **DUMMY_CUSTOMER)
            customer.name = 'Arjun'
            customer.save()
            mock_request.assert_called_once_with('patch', 'https://app.hypertrack.io/api/v1/customers/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id), data={'name': customer.name}, files=None)

    def test_list_customer(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_CUSTOMER]}))

        with patch.object(Customer, '_make_request', return_value=response) as mock_request:
            customers = Customer.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/customers/', params={})

    def test_delete_customer(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(204, json.dumps({}))

        with patch.object(Customer, '_make_request', return_value=response) as mock_request:
            customer = Customer(id=hypertrack_id, **DUMMY_CUSTOMER)
            customer.delete()
            mock_request.assert_called_once_with('delete', 'https://app.hypertrack.io/api/v1/customers/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))


class DestinationTests(unittest2.TestCase):
    '''
    Test destination methods
    '''
    def test_create_destination(self):
        response = MockResponse(201, json.dumps(DUMMY_DESTINATION))

        with patch.object(Destination, '_make_request', return_value=response) as mock_request:
            destination = Destination.create(**DUMMY_DESTINATION)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/destinations/', data=DUMMY_DESTINATION, files=None)

    def test_retrieve_destination(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_DESTINATION))

        with patch.object(Destination, '_make_request', return_value=response) as mock_request:
            destination = Destination.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/destinations/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_update_destination(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_DESTINATION))

        with patch.object(Destination, '_make_request', return_value=response) as mock_request:
            destination = Destination(id=hypertrack_id, **DUMMY_DESTINATION)
            destination.city = 'New York'
            destination.save()
            mock_request.assert_called_once_with('patch', 'https://app.hypertrack.io/api/v1/destinations/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id), data={'city': destination.city}, files=None)

    def test_list_destination(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_DESTINATION]}))

        with patch.object(Destination, '_make_request', return_value=response) as mock_request:
            destinations = Destination.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/destinations/', params={})

    def test_delete_destination(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(204, json.dumps({}))

        with patch.object(Destination, '_make_request', return_value=response) as mock_request:
            destination = Destination(id=hypertrack_id, **DUMMY_DESTINATION)
            destination.delete()
            mock_request.assert_called_once_with('delete', 'https://app.hypertrack.io/api/v1/destinations/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))


class FleetTests(unittest2.TestCase):
    '''
    Test fleet methods
    '''
    def test_create_fleet(self):
        response = MockResponse(201, json.dumps(DUMMY_FLEET))

        with patch.object(Fleet, '_make_request', return_value=response) as mock_request:
            fleet = Fleet.create(**DUMMY_FLEET)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/fleets/', data=DUMMY_FLEET, files=None)

    def test_retrieve_fleet(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_FLEET))

        with patch.object(Fleet, '_make_request', return_value=response) as mock_request:
            fleet = Fleet.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/fleets/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_update_fleet(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_FLEET))

        with patch.object(Fleet, '_make_request', return_value=response) as mock_request:
            fleet = Fleet(id=hypertrack_id, **DUMMY_FLEET)
            fleet.name = 'New York'
            fleet.save()
            mock_request.assert_called_once_with('patch', 'https://app.hypertrack.io/api/v1/fleets/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id), data={'name': fleet.name}, files=None)

    def test_list_fleet(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_FLEET]}))

        with patch.object(Fleet, '_make_request', return_value=response) as mock_request:
            fleets = Fleet.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/fleets/', params={})

    def test_delete_fleet(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(204, json.dumps({}))

        with patch.object(Fleet, '_make_request', return_value=response) as mock_request:
            fleet = Fleet(id=hypertrack_id, **DUMMY_FLEET)
            fleet.delete()
            mock_request.assert_called_once_with('delete', 'https://app.hypertrack.io/api/v1/fleets/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))


class DriverTests(unittest2.TestCase):
    '''
    Test driver methods
    '''
    def test_create_driver(self):
        response = MockResponse(201, json.dumps(DUMMY_DRIVER))

        with patch.object(Driver, '_make_request', return_value=response) as mock_request:
            driver = Driver.create(**DUMMY_DRIVER)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/drivers/', data=DUMMY_DRIVER, files=None)
            self.assertEqual(driver.name, DUMMY_DRIVER.get('name'))

    def test_retrieve_driver(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_DRIVER))

        with patch.object(Driver, '_make_request', return_value=response) as mock_request:
            driver = Driver.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/drivers/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_update_driver(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_DRIVER))

        with patch.object(Driver, '_make_request', return_value=response) as mock_request:
            driver = Driver(id=hypertrack_id, **DUMMY_DRIVER)
            driver.city = 'New York'
            driver.save()
            mock_request.assert_called_once_with('patch', 'https://app.hypertrack.io/api/v1/drivers/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id), data={'city': driver.city}, files=None)

    def test_list_driver(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_DRIVER]}))

        with patch.object(Driver, '_make_request', return_value=response) as mock_request:
            drivers = Driver.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/drivers/', params={})

    def test_driver_end_trip(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_DRIVER))
        data = {}

        with patch.object(Driver, '_make_request', return_value=response) as mock_request:
            driver = Driver(id=hypertrack_id, **DUMMY_DRIVER)
            driver.end_trip()
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/drivers/{hypertrack_id}/end_trip/'.format(hypertrack_id=hypertrack_id), data=data)

    def test_driver_assign_tasks(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_DRIVER))
        data = {'task_ids': [str(uuid.uuid4())]}

        with patch.object(Driver, '_make_request', return_value=response) as mock_request:
            driver = Driver(id=hypertrack_id, **DUMMY_DRIVER)
            driver.assign_tasks(**data)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/drivers/{hypertrack_id}/assign_tasks/'.format(hypertrack_id=hypertrack_id), data=data)

    def test_delete_driver(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(204, json.dumps({}))

        with patch.object(Driver, '_make_request', return_value=response) as mock_request:
            driver = Driver(id=hypertrack_id, **DUMMY_DRIVER)
            driver.delete()
            mock_request.assert_called_once_with('delete', 'https://app.hypertrack.io/api/v1/drivers/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))


class HubTests(unittest2.TestCase):
    '''
    Test hub methods
    '''
    def test_create_hub(self):
        response = MockResponse(201, json.dumps(DUMMY_HUB))

        with patch.object(Hub, '_make_request', return_value=response) as mock_request:
            hub = Hub.create(**DUMMY_HUB)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/hubs/', data=DUMMY_HUB, files=None)

    def test_retrieve_hub(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_HUB))

        with patch.object(Hub, '_make_request', return_value=response) as mock_request:
            hub = Hub.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/hubs/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_update_hub(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_HUB))

        with patch.object(Hub, '_make_request', return_value=response) as mock_request:
            hub = Hub(id=hypertrack_id, **DUMMY_HUB)
            hub.city = 'New York'
            hub.save()
            mock_request.assert_called_once_with('patch', 'https://app.hypertrack.io/api/v1/hubs/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id), data={'city': hub.city}, files=None)

    def test_list_hub(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_HUB]}))

        with patch.object(Hub, '_make_request', return_value=response) as mock_request:
            hubs = Hub.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/hubs/', params={})

    def test_delete_hub(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(204, json.dumps({}))

        with patch.object(Hub, '_make_request', return_value=response) as mock_request:
            hub = Hub(id=hypertrack_id, **DUMMY_HUB)
            hub.delete()
            mock_request.assert_called_once_with('delete', 'https://app.hypertrack.io/api/v1/hubs/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))


class TaskTests(unittest2.TestCase):
    '''
    Test task methods
    '''
    def test_create_task(self):
        response = MockResponse(201, json.dumps(DUMMY_TASK))

        with patch.object(Task, '_make_request', return_value=response) as mock_request:
            task = Task.create(**DUMMY_TASK)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/tasks/', data=DUMMY_TASK, files=None)

    def test_retrieve_task(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TASK))

        with patch.object(Task, '_make_request', return_value=response) as mock_request:
            task = Task.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/tasks/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_update_task(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TASK))

        with patch.object(Task, '_make_request', return_value=response) as mock_request:
            task = Task(id=hypertrack_id, **DUMMY_TASK)
            task.city = 'New York'
            task.save()
            mock_request.assert_called_once_with('patch', 'https://app.hypertrack.io/api/v1/tasks/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id), data={'city': task.city}, files=None)

    def test_list_task(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_TASK]}))

        with patch.object(Task, '_make_request', return_value=response) as mock_request:
            tasks = Task.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/tasks/', params={})

    def test_task_completed(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TASK))
        completion_location = {'type': 'Point', 'coordinates': [72, 19]}
        data = {'completion_location': completion_location}

        with patch.object(Task, '_make_request', return_value=response) as mock_request:
            task = Task(id=hypertrack_id, **DUMMY_TASK)
            task.complete(**data)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/tasks/{hypertrack_id}/completed/'.format(hypertrack_id=hypertrack_id), data=data)

    def test_task_canceled(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TASK))
        cancelation_time = '2016-03-09T06:00:20.648785Z'
        data = {'cancelation_time': cancelation_time}

        with patch.object(Task, '_make_request', return_value=response) as mock_request:
            task = Task(id=hypertrack_id, **DUMMY_TASK)
            task.cancel(**data)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/tasks/{hypertrack_id}/canceled/'.format(hypertrack_id=hypertrack_id), data=data)

    def test_delete_task(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(204, json.dumps({}))

        with patch.object(Task, '_make_request', return_value=response) as mock_request:
            task = Task(id=hypertrack_id, **DUMMY_TASK)
            task.delete()
            mock_request.assert_called_once_with('delete', 'https://app.hypertrack.io/api/v1/tasks/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))


class TripTests(unittest2.TestCase):
    '''
    Test trip methods
    '''
    def test_create_trip(self):
        response = MockResponse(201, json.dumps(DUMMY_TRIP))

        with patch.object(Trip, '_make_request', return_value=response) as mock_request:
            trip = Trip.create(**DUMMY_TRIP)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/trips/', data=DUMMY_TRIP, files=None)

    def test_retrieve_trip(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TRIP))

        with patch.object(Trip, '_make_request', return_value=response) as mock_request:
            trip = Trip.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/trips/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_update_trip(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TRIP))

        with patch.object(Trip, '_make_request', return_value=response) as mock_request:
            trip = Trip(id=hypertrack_id, **DUMMY_TRIP)
            trip.city = 'New York'
            trip.save()
            mock_request.assert_called_once_with('patch', 'https://app.hypertrack.io/api/v1/trips/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id), data={'city': trip.city}, files=None)

    def test_list_trip(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_TRIP]}))

        with patch.object(Trip, '_make_request', return_value=response) as mock_request:
            trips = Trip.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/trips/', params={})

    def test_trip_ended(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TRIP))
        end_location = {'type': 'Point', 'coordinates': [72, 19]}
        data = {'end_location': end_location}

        with patch.object(Trip, '_make_request', return_value=response) as mock_request:
            trip = Trip(id=hypertrack_id, **DUMMY_TRIP)
            trip.end(end_location=end_location)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/trips/{hypertrack_id}/end/'.format(hypertrack_id=hypertrack_id), data=data)

    def test_trip_add_task(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TRIP))
        task_id = str(uuid.uuid4())
        data = {'task_id': task_id}

        with patch.object(Trip, '_make_request', return_value=response) as mock_request:
            trip = Trip(id=hypertrack_id, **DUMMY_TRIP)
            trip.add_task(**data)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/trips/{hypertrack_id}/add_task/'.format(hypertrack_id=hypertrack_id), data=data)

    def test_trip_remove_task(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TRIP))
        task_id = str(uuid.uuid4())
        data = {'task_id': task_id}

        with patch.object(Trip, '_make_request', return_value=response) as mock_request:
            trip = Trip(id=hypertrack_id, **DUMMY_TRIP)
            trip.remove_task(**data)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/trips/{hypertrack_id}/remove_task/'.format(hypertrack_id=hypertrack_id), data=data)

    def test_trip_change_order(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_TRIP))
        task_order = [str(uuid.uuid4()), str(uuid.uuid4())]
        data = {'task_order': task_order}

        with patch.object(Trip, '_make_request', return_value=response) as mock_request:
            trip = Trip(id=hypertrack_id, **DUMMY_TRIP)
            trip.change_task_order(**data)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/trips/{hypertrack_id}/change_task_order/'.format(hypertrack_id=hypertrack_id), data=data)

    def test_delete_trip(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(204, json.dumps({}))

        with patch.object(Trip, '_make_request', return_value=response) as mock_request:
            trip = Trip(id=hypertrack_id, **DUMMY_TRIP)
            trip.delete()
            mock_request.assert_called_once_with('delete', 'https://app.hypertrack.io/api/v1/trips/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))


class GPSLogTests(unittest2.TestCase):
    '''
    Test gpslog methods
    '''
    def test_create_gpslog(self):
        response = MockResponse(201, json.dumps(DUMMY_GPSLOG))

        with patch.object(GPSLog, '_make_request', return_value=response) as mock_request:
            gpslog = GPSLog.create(**DUMMY_GPSLOG)
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/gps/', data=DUMMY_GPSLOG, files=None)

    def test_retrieve_gpslog(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_GPSLOG))

        with patch.object(GPSLog, '_make_request', return_value=response) as mock_request:
            gpslog = GPSLog.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/gps/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_list_gpslog(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_GPSLOG]}))

        with patch.object(GPSLog, '_make_request', return_value=response) as mock_request:
            gps = GPSLog.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/gps/', params={})

    def test_list_gpslog_filtered(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_GPSLOG]}))
        trip_id = str(uuid.uuid4())
        params = {'trip_id': trip_id}

        with patch.object(GPSLog, '_make_request', return_value=response) as mock_request:
            gps = GPSLog.filtered(trip_id=trip_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/gps/filtered/', params=params)

    def test_bulk_gpslog(self):
        response = MockResponse(200, json.dumps({}))

        with patch.object(GPSLog, '_make_request', return_value=response) as mock_request:
            response  = GPSLog.bulk([DUMMY_GPSLOG])
            mock_request.assert_called_once_with('post', 'https://app.hypertrack.io/api/v1/gps/bulk/', data=[DUMMY_GPSLOG])


class EventTests(unittest2.TestCase):
    '''
    Test event methods
    '''
    def test_retrieve_event(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_EVENT))

        with patch.object(Event, '_make_request', return_value=response) as mock_request:
            event = Event.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/events/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_list_event(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_EVENT]}))

        with patch.object(Event, '_make_request', return_value=response) as mock_request:
            events = Event.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/events/', params={})


class NeighborhoodTests(unittest2.TestCase):
    '''
    Test Neighborhood methods
    '''
    def test_retrieve_neighborhood(self):
        hypertrack_id = str(uuid.uuid4())
        response = MockResponse(200, json.dumps(DUMMY_NEIGHBORHOOD))

        with patch.object(Neighborhood, '_make_request', return_value=response) as mock_request:
            neighborhood = Neighborhood.retrieve(hypertrack_id)
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/neighborhoods/{hypertrack_id}/'.format(hypertrack_id=hypertrack_id))

    def test_list_event(self):
        response = MockResponse(200, json.dumps({'results': [DUMMY_NEIGHBORHOOD]}))

        with patch.object(Neighborhood, '_make_request', return_value=response) as mock_request:
            neighborhoods = Neighborhood.list()
            mock_request.assert_called_once_with('get', 'https://app.hypertrack.io/api/v1/neighborhoods/', params={})
