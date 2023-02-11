from django.urls import path
from .views import *

urlpatterns = [
    path('food/', FoodList.as_view(), name='food_list'),
    path('food/<int:pk>/', FoodDetail.as_view(), name='food_detail'),
    path('ingredient/', IngredientList.as_view(), name='food_list'),
    path('ingredient/<int:pk>/', IngredientDetail.as_view(), name='food_detail'),
]