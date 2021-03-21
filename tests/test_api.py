from collections import OrderedDict

import pytest
from rest_framework import status
from rest_framework.test import APIClient

BASE_URL = '/api/v1/'
CARS_ENDPOINT = BASE_URL + 'cars/'
RATE_ENDPOINT = BASE_URL + 'rate/'
POPULAR_ENDPOINT = BASE_URL + 'popular/'

VALID_CARS_ADD = (
    {'make': 'Honda', 'model': 'Civic'},
    {'make': 'Fiat', 'model': '500'}
)


INVALID_CARS_ADD = (
    ({},{'make': ['This field is required.'], 'model': ['This field is required.']}),
    ({'make': 'Honda'}, {'model': ['This field is required.']}),
    ({'model': '500'}, {'make': ['This field is required.']}),
    ({'make': 'xyz', 'model': 'Accord'}, ['This make does not exists at all.']),
    ({'make': 'Fiat', 'model': 'bar'}, ['This model does not exists at all.'])
)


RATE_DATA = (
    (1, status.HTTP_201_CREATED),
    (3, status.HTTP_201_CREATED),
    (5, status.HTTP_201_CREATED),
    (-1, status.HTTP_400_BAD_REQUEST),
    (6, status.HTTP_400_BAD_REQUEST),
    (0, status.HTTP_400_BAD_REQUEST)
)

@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
@pytest.mark.parametrize("data", VALID_CARS_ADD)
def test_correct_add_car(api_client, data):
    resp = api_client.post(CARS_ENDPOINT, data, format='json')
    assert resp.status_code == status.HTTP_201_CREATED
    return resp.data


@pytest.mark.django_db
@pytest.mark.parametrize("data", VALID_CARS_ADD)
def test_add_duplicate(api_client, data):
    test_correct_add_car(api_client, data)
    resp = api_client.post(CARS_ENDPOINT, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == ['Model already exists in database.']


@pytest.mark.django_db
@pytest.mark.parametrize("data, resp_data", INVALID_CARS_ADD)
def test_invalid_add_car(api_client, data, resp_data):
    resp = api_client.post(CARS_ENDPOINT, data, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == resp_data


@pytest.mark.django_db
@pytest.mark.parametrize("data, rate, status", ((car, rate, status) for car in VALID_CARS_ADD
                                                for rate, status in RATE_DATA))
def test_rate_car(api_client, data, rate, status):
    resp_data = test_correct_add_car(api_client, data)
    rate_data = {'car': resp_data['id'], 'rate': rate}
    resp = api_client.post(RATE_ENDPOINT, rate_data, format='json')
    assert resp.status_code == status


@pytest.mark.django_db
def test_get_cars(api_client):
    for car_data in VALID_CARS_ADD:
        resp_data = test_correct_add_car(api_client,car_data)
        for rate in range(4, 6):
            rate_data = {'car': resp_data['id'], 'rate': rate}
            resp = api_client.post(RATE_ENDPOINT, rate_data, format='json')
            assert resp.status_code == status.HTTP_201_CREATED
    resp = api_client.get(CARS_ENDPOINT)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['results'] == [OrderedDict({'id': idx, 'avg': 4.5, **{k: v.lower() for k, v in car_data.items()}})
                                    for idx, car_data in enumerate(VALID_CARS_ADD, 1)]


@pytest.mark.django_db
def test_get_popular(api_client):
    for car_data in VALID_CARS_ADD:
        resp_data = test_correct_add_car(api_client, car_data)
        for rate in range(1, 6):
            rate_data = {'car': resp_data['id'], 'rate': rate}
            resp = api_client.post(RATE_ENDPOINT, rate_data, format='json')
            assert resp.status_code == status.HTTP_201_CREATED
    resp = api_client.get(POPULAR_ENDPOINT)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data['results'] == [OrderedDict({'id': idx,
                                                 'count': 5,
                                                 **{k: v.lower() for k, v in car_data.items()}})
                                    for idx, car_data in enumerate(VALID_CARS_ADD, 1)]

