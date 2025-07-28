from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Home View
def home_view (request: HttpRequest):
    return render(request, "main/index.html")

# Contact View
def contact_view (request: HttpRequest):
    return render(request, "main/contact.html")


# About View
def about_view (request: HttpRequest):
    return render(request, "main/about.html")