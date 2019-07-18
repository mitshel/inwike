from django.contrib import admin
from django.urls import path

from base.views import HomeView, ProfileView, ScopeView, loginView, logoutView, base_login

urlpatterns = [
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('scope/<int:scope_id>/', base_login(ScopeView.as_view()), name='scope'),
    path('', base_login(ProfileView.as_view()), name='home'),
]