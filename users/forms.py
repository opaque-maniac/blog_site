from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Form for registering a user
class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': _('Email'),
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'password1': _('Password'),
            'password2': _('Confirm password')
        }
        error_messages = {
            'email': {
                'unique': _('A user with that email already exists')
            },
            'password2': {
                'password_mismatch': _('The two password fields didn’t match')
            }
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'autofocus': True,
                'placeholder': 'Email address',
                'class': 'form-control form-email',
            }),
            'first_name': forms.TextInput(attrs={
                'autofocus': False,
                'placeholder': 'First name',
                'class': 'form-control form-first-name',
            }),
            'last_name': forms.TextInput(attrs={
                'autofocus': False,
                'placeholder': 'Last name',
                'class': 'form-control form-last-name',
            }),
            'password1': forms.PasswordInput(attrs={
                'autofocus': False,
                'class': 'form-control form-password1',
            }),
            'password2': forms.PasswordInput(attrs={
                'autofocus': False,
                'class': 'form-control form-password2',
            })
        }

# Form for logging in a user
class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        labels = {
            'email': _('Email'),
            'password': _('Password')
        }
        error_messages = {
            'invalid_login': _('Please enter a correct email and password. Note that both fields may be case-sensitive.')
        }
        widgets = {
            'email': forms.EmailInput(attrs={'autofocus': True}),
            'password': forms.PasswordInput(attrs={'autofocus': False})
        }


# For for update user profile
class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'profile_picture']
        labels = {
            'email': _('Email'),
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'profile_picture': _('Profile picture'),
        }
        widgets = {
            'email': forms.EmailInput(attrs={'autofocus': True}),
            'first_name': forms.TextInput(attrs={'autofocus': False}),
            'last_name': forms.TextInput(attrs={'autofocus': False}),
        }
