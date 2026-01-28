from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

# Register
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # check password
        if password1 != password2:
            messages.error(request,"password do not match")
            return redirect('register')
        # check username
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('register')
        # craete user
        user = User.objects.create_user(username=username,email=email,password=password1)
        user.save()
        messages.success(request,"Registration successful. Please login.")
        return redirect('login')
    # GET Request
    return render(request,'accounts/auth.html')

# LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    # GET request
    return render(request,'accounts/auth.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')     