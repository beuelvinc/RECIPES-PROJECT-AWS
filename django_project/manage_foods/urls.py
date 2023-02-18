from django.urls import path,re_path
from .views import *

urlpatterns = [
    re_path(r'list/?$', FoodList.as_view(), name='food_list'),
    path('detail/<int:pk>/', FoodDetail.as_view(), name='food_detail'),

    re_path(r'ingredient/?$', IngredientList.as_view(), name='ingredient_list'),
    path('ingredient/<int:pk>/', IngredientDetail.as_view(), name='ingredient_detail'),

]