# views.py
import bcrypt
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password1')
            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())  # Hash the password
            user.password = hashed_password.decode('utf-8')  # Save the hashed password
            user.save()  # Save the user with the hashed password
            custom_user = CustomUser(user=user)
            custom_user.save()  # Save the CustomUser model
            user = authenticate(request, username=custom_user.get_username(), password=raw_password)
            login(request, user)
            return redirect('home')  # Redirect to your desired page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return HttpResponse("Welcome to the home page!")

def some_view(request):
    custom_user = CustomUser.objects.get(user=request.user)
    username = custom_user.get_username()
    return HttpResponse(username)
