"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

import copy


CREATE_USER_URL = reverse('user:create')
PAYLOAD = {
    'email': 'test@example.com',
    'password': 'testpass123',
    'name': 'Test Name',  
}

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        res = self.client.post(CREATE_USER_URL, PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=PAYLOAD['email'])
        self.assertTrue(user.check_password(PAYLOAD['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if use rwith email exists."""
        create_user(**PAYLOAD)
        res = self.client.post(CREATE_USER_URL, PAYLOAD)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test error returned if password lesls than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'tpw',
            'name': 'Test Name',    
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=PAYLOAD['email']
        ).exists()
        self.assertFalse(user_exists)


