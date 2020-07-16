"""Charity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from charity_app.views import (
                            LandingPageView,
                            AddDonationView,
                            DonatConfirmView,
                            LoginView,
                            RegisterView,
                            UserLogoutView,
                            ProfileView,
                            ProfileEditView,
                            UserUpdateView,
                            SendMailView,
)

urlpatterns = [
    path('admin/', admin.site.urls, name='panel_admin'),
    path('', LandingPageView.as_view(), name='base'),
    path('add_donation/', AddDonationView.as_view(), name='add_donation'),
    path('confirmation/', DonatConfirmView.as_view(), name='confirmation'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile_edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile_update/', UserUpdateView.as_view(), name='profile_update'),
    path('send_mail/', SendMailView.as_view(), name='send_mail'),
]
