from django.shortcuts import render, redirect
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


def settings_view(request: HttpRequest):
    if request.method == "POST":
        mode = request.POST.get("mode", "light")  
        response = redirect(request.META.get("HTTP_REFERER", "/"))  
        response.set_cookie("mode", mode, max_age=60 * 60 * 24 * 30)  
        return response

    return render(request, "main/settings.html")