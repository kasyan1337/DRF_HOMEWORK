# users/urls.py
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PaymentListView, RegisterView, UserListView, UserDetailView

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=AllowAny), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=AllowAny), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]