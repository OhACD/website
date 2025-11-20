from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('about/', views.about_view, name='about'),
    path('projects/', views.projects_view, name='projects'),
]
