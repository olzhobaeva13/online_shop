from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, LogoutAPIView


urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view())
]