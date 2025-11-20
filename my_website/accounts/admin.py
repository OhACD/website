from django.contrib import admin
from .managers import UserManager
from .models import User

# Register your models here.
admin.site.register(User)
