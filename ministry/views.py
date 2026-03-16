from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = 'ministry/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all dynamic content
        context['site_settings'] = SiteSettings.objects.first()
        context['hero'] = HeroContent.objects.first()
        context['hero_background_video'] = HeroBackground.objects.filter(is_active=True).first()
        context['pillars'] = Pillar.objects.all()
        context['missions'] = Mission.objects.all()
        context['programs'] = Program.objects.all()
        context['team_members'] = TeamMember.objects.all()
        context['group_photos'] = GroupPhoto.objects.filter(is_active=True)
        context['leader'] = Leader.objects.first()
        
        # Get gallery items - ONLY ACTIVE ONES
        context['gallery_items'] = GalleryItem.objects.filter(is_active=True).order_by('order', '-uploaded_at')
        
        # Get active announcements
        context['announcements'] = Announcement.objects.filter(is_active=True).order_by('-date')[:6]
        
        # Footer content
        context['footer'] = FooterContent.objects.first()
        
        # Add counts for debugging (optional)
        context['gallery_count'] = GalleryItem.objects.filter(is_active=True).count()
        
        return context
    
class CustomAdminLoginView(LoginView):
    template_name = 'ministry/admin/login.html'
    
    def get_success_url(self):
        return '/ministry-admin/dashboard/'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('ministry_admin:dashboard')
        return super().dispatch(request, *args, **kwargs)