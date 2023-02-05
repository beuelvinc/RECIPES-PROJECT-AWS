from django.urls import path, re_path
from .views import RegisterApi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    re_path(r'^register/?$', RegisterApi.as_view(), name='register_api'),
    re_path(r'^login/?$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'refresh/?$', TokenRefreshView.as_view(), name='token_refresh'),

]
