from django.test import TestCase
from django.urls import reverse

# Test for the home view
class TestHomeView(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_respose_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_response_code_name(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'core/home.html')

    def tearDown(self) -> None:
        return super().tearDown()

# Test for the about view
class TestAboutView(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_response_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('core:about'))
        self.assertTemplateUsed(response, 'core/about.html')

    def tearDown(self) -> None:
        return super().tearDown()

# Test for the contact view
class TestContactView(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_response_code(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('core:contact'))
        self.assertTemplateUsed(response, 'core/contact.html')
    
    def tearDown(self) -> None:
        return super().tearDown()

# Test for the terms view
class TestTermsView(TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_response_code(self):
        response = self.client.get('/terms/')
        self.assertEqual(response.status_code, 200)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('core:terms'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('core:terms'))
        self.assertTemplateUsed(response, 'core/terms.html')
    
    def tearDown(self) -> None:
        return super().tearDown()
