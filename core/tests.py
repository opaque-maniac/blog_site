from django.test import TestCase
from django.urls import reverse


"""
    Test the home page
    Test response code => 200
    Test the template used => 'core/home.html'
"""
class TestHomeView(TestCase):
    def test_respose_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_response_code_name(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'core/home.html')


"""
    Test the about page
    Test response code => 200
    Test the template used => 'core/about.html'
"""
class TestAboutView(TestCase):
    def test_response_code(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('core:about'))
        self.assertTemplateUsed(response, 'core/about.html')


"""
    Test the contact page
    Test response code => 200
    Test the template used => 'core/contact.html'
"""
class TestContactView(TestCase):
    def test_response_code(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('core:contact'))
        self.assertTemplateUsed(response, 'core/contact.html')


"""
    Test the terms page
    Test response code => 200
    Test the template used => 'core/terms.html'
"""
class TestTermsView(TestCase):
    def test_response_code(self):
        response = self.client.get('/terms/')
        self.assertEqual(response.status_code, 200)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('core:terms'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        response = self.client.get(reverse('core:terms'))
        self.assertTemplateUsed(response, 'core/terms.html')
