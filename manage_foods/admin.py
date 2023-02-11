from django.contrib import admin

from .models import  Food,Ingredient

admin.site.register([Food,Ingredient])
