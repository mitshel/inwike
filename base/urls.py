from django.contrib import admin
from django.urls import path

from base.views import HomeView, ProfileView, ScopeView, loginView, logoutView, base_login, get_photo, upload_photo

urlpatterns = [
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('scope/<int:scope_id>/', base_login(ScopeView.as_view()), name='scope'),
    path('photo/', base_login(get_photo), name='photo'),
    path('upload_photo/', base_login(upload_photo), name='upload_photo'),
    path('', base_login(ProfileView.as_view()), name='home'),
]