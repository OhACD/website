from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.forms import RegisterForm

# Create your views here.
def landing_view(request):
    return render(request, "core/landing.html")

def about_view(request):
    return render(request, "core/about.html")

def projects_view(request):
    return render(request, "core/projects.html")
