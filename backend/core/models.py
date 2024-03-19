from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Model for complaints
class Complaint(models.Model):
    email = models.EmailField(_('email'))
    name = models.CharField(_('name'), max_length=255)
    message = models.TextField(_('message'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    seen = models.BooleanField(_('seen'), default=False)
    seen_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='seen_by')
    date_seen = models.DateTimeField(_('date seen'), null=True, blank=True)
    resolved = models.BooleanField(_('resolved'), default=False)
    resolved_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_by')
    date_resolved = models.DateTimeField(_('date resolved'), null=True, blank=True)

    class Meta:
        verbose_name = 'complaint'
        verbose_name_plural = 'complaints'
    
    def __str__(self):
        return f'{self.email} - {self.name} - {self.created_at}'