from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Complaints

# Test complaint model
class TestComplaintModel(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'thisismypassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)

        self.complaint_detials = {
            'name': 'complaintuser',
            'email': 'complaints@example.com',
            'message': 'Terrible! Just terrible',
            'phone': '+123445679000398'
        }
        self.complaint = Complaints.objects.create(**self.complaint_detials)
    
    def test_complaint(self) -> None:
        self.assertEqual(self.complaint.name, self.complaint_detials['name'])
        self.assertEqual(self.complaint.email, self.complaint_detials['email'])
        self.assertEqual(self.complaint.message, self.complaint_detials['message'])
        self.assertEqual(self.complaint.phone, self.complaint_detials['phone'])
    
    def tearDown(self) -> None:
        self.complaint.delete()
        self.user.delete()