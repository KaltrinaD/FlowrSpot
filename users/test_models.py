from django.test import TestCase
from .models import User, Flowers, SightingModel, Likes

# class UserAuthenticationTest(TestCase):
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
import json


class ApiTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('d', 'd@d.com', 'd')

        self.token = Token.objects.get(user=self.user).key
        self.c = Client()

    def test_authorization(self):
        header = {'Authorization: Bearer': 'Token {}'.format(self.token)}
        response = self.client.get(reverse('sightings_all'), {}, **header)
        self.assertEqual(response.status_code, 200, "REST token-auth failed")

