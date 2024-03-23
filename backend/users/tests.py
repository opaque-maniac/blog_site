from django.test import TestCase
from django.contrib.auth import get_user_model

# Testing custom user model
class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'thisismypassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)

        self.superuser_credentials = {
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'password': 'thisismypassword'
        }
        self.superuser = get_user_model().objects.create_superuser(**self.superuser_credentials)

    def test_create_user(self) -> None:
        self.assertEqual(self.user.email, self.user_credentials['email'])
        self.assertEqual(self.user.first_name, self.user_credentials['first_name'])
        self.assertEqual(self.user.last_name, self.user_credentials['last_name'])
        self.assertTrue(self.user.check_password(self.user_credentials['password']))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self) -> None:
        self.assertEqual(self.superuser.email, self.superuser_credentials['email'])
        self.assertEqual(self.superuser.first_name, self.superuser_credentials['first_name'])
        self.assertEqual(self.superuser.last_name, self.superuser_credentials['last_name'])
        self.assertTrue(self.superuser.check_password(self.superuser_credentials['password']))
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)

    def tearDown(self) -> None:
        self.user.delete()
        self.superuser.delete()