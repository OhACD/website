from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.forms import RegisterForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'main/users.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            new_form = AuthenticationForm(request)
            return render(request, "main/login.html", {"form": new_form, "message": "Invalid Credentials"})
    else:
        form = AuthenticationForm()

    return render(request, "main/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})
