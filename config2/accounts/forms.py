from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        labels = {'email' : 'E-mail', 'username' : 'Username', 'password1' : 'Password', 'password2' : 'Confirm Password'}
        