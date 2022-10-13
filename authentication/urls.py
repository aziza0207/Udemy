from django.urls import path
from .views import RegisterAPI, MentorRegisterView, LoginAPIView, ResetPasswordRequestView, PasswordResetView

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path("register/mentor/<int:pk>", MentorRegisterView.as_view()),
    path("login/", LoginAPIView.as_view(), name="obtain-token"),
    path('password_reset_request', ResetPasswordRequestView.as_view(), name="password_reset"),
    path('password_reset/<str:uuid>', PasswordResetView.as_view())
]
