from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'ministry'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    # Admin login/logout
    path('admin-login/', auth_views.LoginView.as_view(
        template_name='ministry/admin/login.html',
        redirect_authenticated_user=True,
        next_page='/ministry-admin/dashboard/'
    ), name='admin_login'),
    
    path('admin-logout/', auth_views.LogoutView.as_view(
        next_page='/'
    ), name='admin_logout'),
]