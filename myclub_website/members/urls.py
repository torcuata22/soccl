from django.urls import path
from . import views
from .views import UserRegisterView

urlpatterns = [
    path('login_user', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register_user', UserRegisterView.as_view(), name='register_user'),


    
]