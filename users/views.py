from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model

from .forms import RegisterForm, LoginForm, ProfileUpdateForm

# View for the register page
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect(reverse('core:home'))
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

# View for the login page
def login_view(request):
    return LoginView.as_view(template_name = 'users/login.html', authentication_form = LoginForm)(request)

# View for the logout page
@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('core:home'))

# View for the profile page
@login_required
def profile(request):
    user = get_user_model().objects.get(id=request.user.id)
    return render(request, 'users/profile.html', { 'user': user })

# View for the update profile view
@login_required
def update_profile(request):
    user_profile = get_user_model().objects.get(id=request.user.id)
    if request.method == 'POST':
        form = ProfileUpdateForm(instance=user_profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:profile'))
    else:
        form = ProfileUpdateForm(instance=user_profile)
    return render(request, 'users/update_profile.html', { 'form': form })
