from .models import SiteSettings, FooterContent

def site_settings(request):
    """Make site settings available to all templates"""
    return {
        'site_settings': SiteSettings.objects.first(),
        'footer': FooterContent.objects.first(),
    }