from django.shortcuts import render

# View for the homepage
def home(request):
    return render(request, 'core/home.html')

# View for the about page
def about(request):
    return render(request, 'core/about.html')

# View for the contact page
def contact(request):
    return render(request, 'core/contact.html')

# View for the terms and conditions page
def terms(request):
    return render(request, 'core/terms.html')
