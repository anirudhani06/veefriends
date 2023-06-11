from django.contrib import admin
from .models import Post, Profile, Comment, Activity

# Register your models here.

admin.site.register([Post, Profile, Comment, Activity])
