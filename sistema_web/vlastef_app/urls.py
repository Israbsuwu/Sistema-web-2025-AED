from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('panel/users/', views.admin_users_view, name='admin_users'),
]
