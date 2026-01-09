from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpView, LoginView, MeView, LogoutView, UserVerify

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('verify/', UserVerify.as_view(), name='verify')
]
