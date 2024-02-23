from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model

from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from blog.models import Post


"""
    This is a view function for the register page
    It uses the RegisterForm from this apps form file
    It renders => 'users/register.html'
"""
def register_view(request):
    # The post method
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Automatically authenticate user
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect(reverse('core:home'))
    else:
        # For the get method
        form = RegisterForm()
    # Rendering the page
    return render(request, 'users/register.html', { 
        'form': form
    })


"""
    This is a view function for the login page
    It uses the LoginForm from this apps form file
    It renders => 'users/login.html'
"""
def login_view(request):
    return LoginView.as_view(template_name = 'users/login.html', authentication_form = LoginForm)(request)


"""
    This is a view function for the logout function
    It uses no form
    It renders no template
"""
@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('core:home'))


"""
    This is a view function for the profile page
    It uses the no form
    It renders => 'users/profile.html'
"""
@login_required
def profile(request):
    user = get_user_model().objects.get(id=request.user.id)
    return render(request, 'users/profile.html', { 'user': user })


"""
    This is a view function for the register page
    It uses the ProfileUpdateForm from this apps form file
    It renders => 'users/update_profile.html'
"""
@login_required
def update_profile(request):
    # Query the user profile
    user_profile = get_user_model().objects.get(id=request.user.id)
    if request.method == 'POST':
        # For the post method
        form = ProfileUpdateForm(instance=user_profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:profile'))
    else:
        # For the get method
        form = ProfileUpdateForm(instance=user_profile)
    # Render the page
    return render(request, 'users/update_profile.html', { 'form': form })


"""
    This is a view function for the other users page
    It uses no form
    It renders => 'users/user_profile.html'
"""
def user_profile(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    return render(request, 'users/user_profile.html', {
        'user': user,
    })

