from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Register, UserDetail, CreateAlert, DeleteAlert, FetchAlerts

urlpatterns = [
    path("register", Register.as_view()),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("user", UserDetail.as_view(), name="user_detail"),
    path("alerts/create", CreateAlert.as_view(), name="create_alert"),
    path("alerts/delete/<int:pk>", DeleteAlert.as_view(), name="delete_alert"),
    path("alerts/", FetchAlerts.as_view(), name="list_alerts"),
]
