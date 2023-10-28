from .forms import NewUserForm as UserForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.shortcuts import redirect

# View for the register page
def register(request):
    if request.method != 'POST':
        form = UserForm()
    else:
        form = UserForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(username=username, password=password)
            authenticate(request, user)
            return redirect('blog:home')
    context = {'form' : form}
    return render(request, 'registration/signup.html', context)

# View for the login page
def login(request):
    return LoginView.as_view(template_name = 'registration/login.html')(request)

# View for the logout function
def logout(request):
    return LogoutView.as_view()(request)