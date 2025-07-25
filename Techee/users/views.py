from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
import re  

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "users/register.html")

        
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            messages.error(request, "Please enter a valid email address.")
            return render(request, "users/register.html")

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, "users/register.html")

        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "users/register.html")

        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
        )

        login(request, user)
        return redirect("main:home_view")

    return render(request, "users/register.html")
