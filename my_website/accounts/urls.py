from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('verify/', views.verify_email, name='verify'),
    path('login/confirm/', views.login_confirm, name='login_confirm')
]
