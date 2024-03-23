from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager

# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    first_name = models.CharField(_('First name'), max_length=100)
    last_name = models.CharField(_('Last name'), max_length=100)
    profile_image = models.ImageField(_('Profile image'), upload_to='profile_images/', null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f'{ self.id } -> { self.email }'
