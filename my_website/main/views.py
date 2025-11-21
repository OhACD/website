from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.forms import RegisterForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'main/users.html')

def _apply_auth_form_styles(form):
    base_input = "w-full rounded-xl border border-brand-baseMuted bg-brand-base px-4 py-3 text-brand-text placeholder-brand-textMuted focus:border-brand-accentMint focus:outline-none focus:ring-2 focus:ring-brand-accentMint/50"
    for field in form.fields.values():
        field.widget.attrs.setdefault("placeholder", field.label)
        field.widget.attrs["class"] = f"{field.widget.attrs.get('class', '')} {base_input}".strip()
    return form


def login_view(request):
    if request.method == 'POST':
        form = _apply_auth_form_styles(AuthenticationForm(request, data=request.POST))
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            new_form = _apply_auth_form_styles(AuthenticationForm(request))
            return render(request, 'main/login.html', {'form': new_form, 'message': 'Invalid Credentials'})
    else:
        form = _apply_auth_form_styles(AuthenticationForm())

    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})
