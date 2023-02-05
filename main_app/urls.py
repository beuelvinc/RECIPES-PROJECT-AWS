from django.urls import path, re_path
from .views import *


urlpatterns = [
    re_path(r'list/?$', ListFoods.as_view(), name='ListFoods'),
    re_path(r'detail/?$', DetailFood.as_view(), name='DetailFood'),

]
