from django.urls import path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignUpView, LoginView, MeView, LogoutView, UserVerify,
    ResendVerificationEmail, CompanyView, CompanyRetrieveUpdateDestroyView,
    PofileCreateView, ProfileRetrieveUpdateView, ExperienceView, ExperienceDestroyView, EducationView
)


router = DefaultRouter()
router.register(r'education', EducationView, basename='education')


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('verify/', UserVerify.as_view(), name='verify'),
    path('resend-verification/', ResendVerificationEmail.as_view(), name='resend_verification'),
    path('company/', CompanyView.as_view(), name='company'),
    path('company/<uuid:id>/', CompanyRetrieveUpdateDestroyView.as_view(), name='company'),
    path('profile/', PofileCreateView.as_view({'post': 'create'})),
    path('profile/', ProfileRetrieveUpdateView.as_view(), name='profile'),
    path('experience/', ExperienceView.as_view(), name='experience'),
    path('experience/<uuid:id>/', ExperienceDestroyView.as_view(), name='experience')
] + router.urls
