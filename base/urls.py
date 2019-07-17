from django.contrib import admin
from django.urls import path

from base.views import HomeView, ProfileView, ScopeView

urlpatterns = [
    path('scope/<int:scope_id>/', ScopeView.as_view(), name='scope'),
    path('', ProfileView.as_view(), name='home'),
]