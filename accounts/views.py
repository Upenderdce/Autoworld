from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from accounts.forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('http://127.0.0.1:8000')  # Replace with the name of your homepage URL
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

from django.contrib.auth import views as auth_views

# Login view can be imported directly from auth_views
