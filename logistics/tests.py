from django.test import Client
from django.test import TestCase

from logistics.permissions import is_driver, is_owner


class CommonApiTest(TestCase):

    def test_login_logout(self):
        c = Client()
        response = c.post('/api/signup/', {"login": "owner1",
                                           "password": "owner1",
                                           "role": "1",
                                           "first_name": "Vasya",
                                           "last_name": "Pupkin",
                                           "email": "aa@bb.ru"}
                          )
        self.assertEqual(response.status_code, 201)
        self.assertEqual({'status': 'ok'}, response.data)

        response = c.post('/api/auth/', {"login": "owner1", "password": "owner1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'status': 'ok'}, response.data)

        response = c.get('/api/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'status': 'ok'}, response.data)

        response = c.get('/api/logout/')
        self.assertEqual(response.status_code, 409)
        self.assertIn(('status','error'), response.data.items())

    def test_owner_roles(self):
        c = Client()
        response = c.post('/api/signup/', {"login": "owner1",
                                           "password": "owner1",
                                           "role": "1",
                                           "first_name": "Vasya",
                                           "last_name": "Pupkin",
                                           "email": "aa@bb.ru"})
        self.assertEqual({'status': 'ok'}, response.data)

        response = c.post('/api/auth/', {"login": "owner1", "password": "owner1"})
        self.assertEqual({'status': 'ok'}, response.data)

        self.assertTrue(is_owner(response.wsgi_request.user))
        self.assertFalse(is_driver(response.wsgi_request.user))

    def test_driver_roles(self):
        c = Client()
        response = c.post('/api/signup/', {"login": "driver1",
                                           "password": "driver1",
                                           "role": "2",
                                           "first_name": "Vasya",
                                           "last_name": "Pupkin",
                                           "email": "aa@bb.ru"})
        self.assertEqual({'status': 'ok'}, response.data)

        response = c.post('/api/auth/', {"login": "driver1", "password": "driver1"})
        self.assertEqual({'status': 'ok'}, response.data)

        self.assertFalse(is_owner(response.wsgi_request.user))
        self.assertTrue(is_driver(response.wsgi_request.user))
