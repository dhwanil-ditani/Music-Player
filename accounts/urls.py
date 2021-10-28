from django.urls import path
from accounts.views import SignupView, activate
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('register/', SignupView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
]
