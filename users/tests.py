from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Test the custom user model
class TestCustomUser(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.superuser_credentials = {
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'password': 'adminpassword'
        }
        self.superuser = get_user_model().objects.create_superuser(**self.superuser_credentials)
        self.superuser.save()
    
    def test_string_representation(self):
        self.assertEqual(self.user.__str__(), self.user.email)
        self.assertEqual(self.superuser.__str__(), self.superuser.email)
    
    def test_create_user(self):
        self.assertEqual(self.user.email, self.user_credentials['email'])
        self.assertEqual(self.user.first_name, self.user_credentials['first_name'])
        self.assertEqual(self.user.last_name, self.user_credentials['last_name'])
        self.assertTrue(self.user.check_password(self.user_credentials['password']))
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)
    
    def test_create_superuser(self):
        self.assertEqual(self.superuser.email, self.superuser_credentials['email'])
        self.assertEqual(self.superuser.first_name, self.superuser_credentials['first_name'])
        self.assertEqual(self.superuser.last_name, self.superuser_credentials['last_name'])
        self.assertTrue(self.superuser.check_password(self.superuser_credentials['password']))
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_superuser)
    
    def tearDown(self) -> None:
        self.user.delete()
        self.superuser.delete()

# Test the register page view
class TestRegisterView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
    
    def test_response_code(self):
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)

    def test_response_code_name(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_post_method(self):
        response = self.client.post(reverse('users:register'), self.user_credentials)
        self.assertEqual(response.status_code, 200)
    
# Test the login page view
class TestLoginView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()
    
    def test_response_code(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_post_method(self):
        response = self.client.post(reverse('users:login'), self.user_credentials)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self) -> None:
        self.user.delete()

# Test the profile view
class TestProfileView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()
    
    def test_response_code(self):
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(reverse('users:profile'))
        self.assertRedirects(response, '/users/login/?next=/users/profile/')

    def test_response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
    
    def tearDown(self) -> None:
        self.user.delete()

# Test the logout view
class TestLogoutView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

    def test_response_code(self):
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, '/users/login/?next=/users/logout/')
    
    def test_response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, '/')

    def tearDown(self) -> None:
        self.user.delete()

 # Test for the update profile view
class TestUpdateProfileView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()
        self.test_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_response_code(self):
        response = self.client.get('/users/profile/update/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('users:update_profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('users:update_profile'))
        self.assertRedirects(response, '/users/login/?next=/users/profile/update/')
    
    def test_response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('users:update_profile'))
        self.assertEqual(response.status_code, 200)
    
    def test_redirect_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('users:update_profile'))
        self.assertTemplateUsed(response, 'users/update_profile.html')
    
    def test_post_method(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.post(reverse('users:update_profile'), self.test_data)
        self.assertEqual(response.status_code, 302)
    
    def test_redirect_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.post(reverse('users:update_profile'), self.test_data)
        self.assertRedirects(response, reverse('users:profile'))

    def tearDown(self) -> None:
        self.user.delete()   
