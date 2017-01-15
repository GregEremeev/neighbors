from copy import deepcopy

from rest_framework import status
from rest_framework.test import APITestCase

from neighbors.core.models import User


class UserAPITest(APITestCase):

    BASE_API_URL = '/api/v1/'
    USER_API_URL = BASE_API_URL + 'users/'
    USER_INSTANCE_API_URL = USER_API_URL + '{}/'
    NEAREST_NEIGHBORS_API_URL = USER_INSTANCE_API_URL + 'nearest_neighbors/'

    LOCATIONS = [{'latitude': 55.703129, 'longitude': 37.623367},
                 {'latitude': 55.667517, 'longitude': 37.627487},
                 {'latitude': 55.640399, 'longitude': 37.623367},
                 {'latitude': 55.602402, 'longitude': 37.617874},
                 {'latitude': 55.569805, 'longitude': 37.615128}]

    USER_DATA = {'username': 'username', 'first_name': 'first_name', 'last_name': 'last_name',
                 'location': {'latitude': 55.755826, 'longitude': 37.6173}}

    def test_get_user_collection(self):
        user_number = 5
        for i in range(user_number):
            data = deepcopy(self.USER_DATA)
            data['username'] += str(i)
            self.create_user(data)

        response = self.client.get(self.USER_API_URL, {'limit': user_number})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), user_number)
        user = User.objects.get(username=data['username'])

        resp_data = filter(lambda d: d['username'] == data['username'], response.data['results'])
        self.validate_user_data(user, data, list(resp_data)[0])

    def test_get_user(self):
        data = deepcopy(self.USER_DATA)
        res = self.create_user(data)

        response = self.client.get(self.USER_INSTANCE_API_URL.format(res.data['id']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(username=data['username'])
        self.validate_user_data(user, data, response.data)

    def test_delete_user(self):
        data = deepcopy(self.USER_DATA)
        res = self.create_user(data)

        response = self.client.delete(self.USER_INSTANCE_API_URL.format(res.data['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(list(User.objects.all()), [])

    def test_create_user(self):
        data = deepcopy(self.USER_DATA)
        response = self.create_user(data)

        user = User.objects.get()
        self.validate_user_data(user, data, response.data)

    def test_update_user(self):
        data = deepcopy(self.USER_DATA)
        self.create_user(data)
        user = User.objects.get()

        data['username'] = 'another_username'
        data['first_name'] = 'another_first_name'
        data['last_name'] = 'another_last_name'
        data['location'] = {'latitude': 55.832915, 'longitude': 37.915878}

        response = self.client.patch(
            self.USER_INSTANCE_API_URL.format(user.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get()
        self.validate_user_data(user, data, response.data)

    def validate_user_data(self, user, data, response_data):
        self.assertEqual(user.id, response_data['id'])

        loc = data.pop('location')
        loc_res = response_data['location']
        self.assertEqual((loc['longitude'], loc['latitude']),
                         (float(loc_res['longitude']), float(loc_res['latitude'])))
        self.assertEqual((loc['longitude'], loc['latitude']), user.location.coords)

        for k, v in data.items():
            self.assertEqual(getattr(user, k), v)
            self.assertEqual(response_data[k], v)

    def create_user(self, data):
        response = self.client.post(self.USER_API_URL, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def test_nearest_neighbors(self):
        neighbors_num = 2
        for num, location in enumerate(deepcopy(self.LOCATIONS)):
            data = deepcopy(self.USER_DATA)
            data['username'] += str(num)
            data['location'] = location
            self.create_user(data)

        user = User.objects.first()
        response = self.client.get(
            self.NEAREST_NEIGHBORS_API_URL.format(user.id), {'limit': neighbors_num, 'radius': 100.9})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), neighbors_num)

        expected_locations = self.LOCATIONS[1:neighbors_num + 1]
        for loc, neighbor in zip(expected_locations, response.data):
            neighbor_loc = neighbor['location']
            self.assertEqual([loc['latitude'], loc['longitude']],
                             [float(neighbor_loc['latitude']), float(neighbor_loc['longitude'])])
