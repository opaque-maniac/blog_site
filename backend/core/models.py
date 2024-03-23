from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Model for complaints
class Complaints(models.Model):
    RESPONSE_CHOICES = (
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('whatsapp', 'WhatsApp'),
        ('sms', 'SMS'),
        ('visit', 'Visit'),
        ('other', 'Other')
    )

    email = models.EmailField()
    name = models.CharField(max_length=225)
    phone = models.CharField(max_length=225, blank=True, null=True)
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)
    seen_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints_seen')
    date_seen = models.DateTimeField(blank=True, null=True)
    responded = models.BooleanField(default=False)
    mode_of_response = models.CharField(max_length=225, blank=True, null=True, choices=RESPONSE_CHOICES)
    response = models.TextField(blank=True, null=True)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints_responded')
    date_of_first_response = models.DateTimeField(blank=True, null=True)
    solved = models.BooleanField(default=False)
    solved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints_solved')
    date_of_solution = models.DateTimeField(blank=True, null=True)
    link_to_complaint_doc = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = _('complaint')
        verbose_name_plural = _('complaints')
    
    def __str__(self):
        return f'{ self.id } -> { self.email }'
