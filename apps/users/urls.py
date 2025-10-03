# accounts/urls.py
from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    path("password-change/", PasswordChangeView.as_view(), name="password-change"), #old pass enter

    path('send-message/', SendMessageClass.as_view(), name='contact-list'),

]