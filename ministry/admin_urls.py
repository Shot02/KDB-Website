from django.urls import path
from django.contrib.auth.decorators import login_required
from . import admin_views

app_name = 'ministry_admin'  # This defines the namespace

urlpatterns = [
    # Dashboard
    path('dashboard/', login_required(admin_views.dashboard), name='dashboard'),
    
    # User Management
    path('users/', login_required(admin_views.user_list), name='user_list'),
    path('users/add/', login_required(admin_views.user_add), name='user_add'),
    path('users/<int:pk>/edit/', login_required(admin_views.user_edit), name='user_edit'),
    path('users/<int:pk>/delete/', login_required(admin_views.user_delete), name='user_delete'),
    path('users/<int:pk>/toggle-staff/', login_required(admin_views.user_toggle_staff), name='user_toggle_staff'),
    path('users/<int:pk>/toggle-superuser/', login_required(admin_views.user_toggle_superuser), name='user_toggle_superuser'),
    path('users/<int:pk>/reset-password/', login_required(admin_views.user_reset_password), name='user_reset_password'),
    
    # Site Settings
    path('settings/', login_required(admin_views.site_settings), name='site_settings'),
    
    # Pillars
    path('pillars/', login_required(admin_views.pillar_list), name='pillar_list'),
    path('pillars/add/', login_required(admin_views.pillar_add), name='pillar_add'),
    path('pillars/<int:pk>/edit/', login_required(admin_views.pillar_edit), name='pillar_edit'),
    path('pillars/<int:pk>/delete/', login_required(admin_views.pillar_delete), name='pillar_delete'),
    
    # Programs
    path('programs/', login_required(admin_views.program_list), name='program_list'),
    path('programs/add/', login_required(admin_views.program_add), name='program_add'),
    path('programs/<int:pk>/edit/', login_required(admin_views.program_edit), name='program_edit'),
    path('programs/<int:pk>/delete/', login_required(admin_views.program_delete), name='program_delete'),
    
    # Team Members
    path('team/', login_required(admin_views.team_list), name='team_list'),
    path('team/add/', login_required(admin_views.team_add), name='team_add'),
    path('team/<int:pk>/edit/', login_required(admin_views.team_edit), name='team_edit'),
    path('team/<int:pk>/delete/', login_required(admin_views.team_delete), name='team_delete'),
    
    # Gallery
    path('gallery/', login_required(admin_views.gallery_list), name='gallery_list'),
    path('gallery/add/', login_required(admin_views.gallery_add), name='gallery_add'),
    path('gallery/<int:pk>/edit/', login_required(admin_views.gallery_edit), name='gallery_edit'),
    path('gallery/<int:pk>/delete/', login_required(admin_views.gallery_delete), name='gallery_delete'),
    
    # Announcements
    path('announcements/', login_required(admin_views.announcement_list), name='announcement_list'),
    path('announcements/add/', login_required(admin_views.announcement_add), name='announcement_add'),
    path('announcements/<int:pk>/edit/', login_required(admin_views.announcement_edit), name='announcement_edit'),
    path('announcements/<int:pk>/delete/', login_required(admin_views.announcement_delete), name='announcement_delete'),
    
    # Hero Section
    path('hero/', login_required(admin_views.hero_edit), name='hero_edit'),
    
    # Hero Backgrounds
    path('hero-backgrounds/', login_required(admin_views.hero_background_list), name='hero_backgrounds'),
    path('hero-backgrounds/add/', login_required(admin_views.hero_background_add), name='hero_background_add'),
    path('hero-backgrounds/<int:pk>/edit/', login_required(admin_views.hero_background_edit), name='hero_background_edit'),
    path('hero-backgrounds/<int:pk>/delete/', login_required(admin_views.hero_background_delete), name='hero_background_delete'),
    
    # Leader Info
    path('leader/', login_required(admin_views.leader_edit), name='leader_edit'),
    
    # Group Photo
    path('group-photo/', login_required(admin_views.group_photo), name='group_photo'),
]