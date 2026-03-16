from django.contrib import admin
from django.utils.html import format_html
from .models import *

# ============ SITE SETTINGS ============
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'registration_number', 'can_number', 'mission_statement', 'logo')
        }),
        ('Contact Information', {
            'fields': ('whatsapp_numbers', 'email', 'location')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url', 'twitter_url')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'account_number', 'account_name')
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent adding multiple instances
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False

# ============ PILLARS ============
@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ('acronym', 'title', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('title', 'acronym', 'description')
    list_filter = ('order',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('acronym', 'title', 'description', 'icon', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# ============ MISSIONS ============
@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'description')

# ============ PROGRAMS ============
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('day', 'title', 'start_time', 'end_time', 'order', 'created_at')
    list_editable = ('order',)
    list_filter = ('day',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('day', 'title', 'start_time', 'end_time', 'description', 'icon', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

# ============ TEAM MEMBERS ============
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'image_preview', 'created_at')
    list_editable = ('order',)
    search_fields = ('name', 'position')
    readonly_fields = ('created_at', 'updated_at', 'image_preview_large')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'position', 'photo', 'order')
        }),
        ('Preview', {
            'fields': ('image_preview_large',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%; object-fit:cover;" />', obj.photo.url)
        return format_html('<div style="width:50px; height:50px; background:#ccc; border-radius:50%; display:flex; align-items:center; justify-content:center;"><i class="bi bi-person" style="color:white;"></i></div>')
    image_preview.short_description = 'Photo'
    
    def image_preview_large(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="200" style="border-radius:10px;" />', obj.photo.url)
        return "No photo uploaded"
    image_preview_large.short_description = 'Photo Preview'

# ============ GROUP PHOTO ============
@admin.register(GroupPhoto)
class GroupPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'caption', 'is_active', 'image_preview')
    list_filter = ('is_active',)
    
    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" style="border-radius:5px;" />', obj.photo.url)
        return "No photo"
    image_preview.short_description = 'Preview'

# ============ LEADER ============
@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'title', 'bio', 'photo')
        }),
        ('Preview', {
            'fields': ('image_preview',),
        }),
    )
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="200" style="border-radius:10px;" />', obj.photo.url)
        return "No photo uploaded"
    image_preview.short_description = 'Photo Preview'
    
    def has_add_permission(self, request):
        return not Leader.objects.exists()

# ============ GALLERY ITEM ============
@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'order', 'is_active', 'uploaded_at', 'media_preview')
    list_editable = ('order', 'is_active')
    list_filter = ('media_type', 'is_active', 'uploaded_at')
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_at', 'updated_at', 'media_preview_large', 'file_info')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'media_type', 'order', 'is_active')
        }),
        ('Media Files', {
            'fields': ('file', 'thumbnail', 'media_preview_large')
        }),
        ('File Information', {
            'fields': ('file_info',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def media_preview(self, obj):
        if obj.media_type == 'video':
            if obj.thumbnail:
                return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit:cover;" />', obj.thumbnail.url)
            return format_html('<i class="bi bi-play-circle" style="font-size:30px; color:#17a2b8;"></i>')
        elif obj.media_type == 'flyer':
            if obj.file and obj.file.url.lower().endswith('.pdf'):
                return format_html('<i class="bi bi-file-pdf" style="font-size:30px; color:#dc3545;"></i>')
            elif obj.file:
                return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit:cover;" />', obj.file.url)
        else:
            if obj.file:
                return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit:cover;" />', obj.file.url)
        return "-"
    media_preview.short_description = 'Preview'
    
    def media_preview_large(self, obj):
        if obj.media_type == 'video':
            if obj.thumbnail:
                return format_html('''
                    <div>
                        <img src="{}" width="200" style="border-radius:10px;" />
                        <br>
                        <span class="badge bg-info">Video Thumbnail</span>
                        <br>
                        <video width="200" controls style="margin-top:10px;">
                            <source src="{}" type="video/mp4">
                        </video>
                    </div>
                ''', obj.thumbnail.url, obj.file.url)
            return format_html('''
                <div>
                    <video width="200" controls>
                        <source src="{}" type="video/mp4">
                    </video>
                </div>
            ''', obj.file.url)
        elif obj.media_type == 'flyer':
            if obj.file and obj.file.url.lower().endswith('.pdf'):
                return format_html('''
                    <div>
                        <i class="bi bi-file-pdf" style="font-size:48px; color:#dc3545;"></i>
                        <br>
                        <a href="{}" target="_blank" class="btn btn-sm btn-primary">View PDF</a>
                    </div>
                ''', obj.file.url)
            else:
                return format_html('<img src="{}" width="200" style="border-radius:10px;" />', obj.file.url)
        else:
            return format_html('<img src="{}" width="200" style="border-radius:10px;" />', obj.file.url)
    media_preview_large.short_description = 'Large Preview'
    
    def file_info(self, obj):
        if obj.file:
            file_size = obj.file.size / 1024 / 1024  # Convert to MB
            return format_html('''
                <ul>
                    <li><strong>Filename:</strong> {}</li>
                    <li><strong>Size:</strong> {:.2f} MB</li>
                    <li><strong>Type:</strong> {}</li>
                    <li><strong>Path:</strong> {}</li>
                </ul>
            ''', obj.file.name, file_size, obj.media_type, obj.file.path)
        return "No file uploaded"
    file_info.short_description = 'File Details'

# ============ ANNOUNCEMENTS ============
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_active', 'created_at', 'preview_image')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'preview_image_large')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'date', 'is_active')
        }),
        ('Media Files', {
            'fields': ('image', 'file', 'preview_image_large')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit:cover;" />', obj.image.url)
        elif obj.file:
            if obj.file.url.lower().endswith('.pdf'):
                return format_html('<i class="bi bi-file-pdf" style="font-size:30px; color:#dc3545;"></i>')
        return "-"
    preview_image.short_description = 'Preview'
    
    def preview_image_large(self, obj):
        html = '<div>'
        if obj.image:
            html += f'<img src="{obj.image.url}" width="200" style="border-radius:10px; margin-bottom:10px;" /><br>'
        if obj.file:
            if obj.file.url.lower().endswith('.pdf'):
                html += f'<a href="{obj.file.url}" target="_blank" class="btn btn-sm btn-primary">View PDF Flyer</a>'
            else:
                html += f'<img src="{obj.file.url}" width="200" style="border-radius:10px;" />'
        html += '</div>'
        return format_html(html) if obj.image or obj.file else "No media uploaded"
    preview_image_large.short_description = 'Media Preview'

# ============ HERO CONTENT ============
@admin.register(HeroContent)
class HeroContentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Text Content', {
            'fields': ('main_title', 'subtitle', 'description', 
                      'button1_text', 'button1_link', 'button2_text', 'button2_link')
        }),
        ('Background Media', {
            'fields': ('background_image', 'background_video'),
            'description': 'Upload either an image or video for the background (video takes priority)'
        }),
        ('Preview', {
            'fields': ('media_preview',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('media_preview',)
    
    def media_preview(self, obj):
        html = '<div style="padding:10px; background:#f8f9fa; border-radius:10px;">'
        if obj.background_video:
            html += f'''
                <h5>Current Video:</h5>
                <video width="300" controls>
                    <source src="{obj.background_video.url}" type="video/mp4">
                </video>
            '''
        elif obj.background_image:
            html += f'''
                <h5>Current Image:</h5>
                <img src="{obj.background_image.url}" width="300" style="border-radius:10px;">
            '''
        else:
            html += '<p>No background media uploaded</p>'
        html += '</div>'
        return format_html(html)
    media_preview.short_description = 'Media Preview'
    
    def has_add_permission(self, request):
        return not HeroContent.objects.exists()

# ============ HERO BACKGROUND ============
@admin.register(HeroBackground)
class HeroBackgroundAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'media_type', 'preview')
    list_filter = ('is_active',)
    search_fields = ('title',)
    
    def media_type(self, obj):
        if obj.video:
            return "Video"
        elif obj.image:
            return "Image"
        return "None"
    media_type.short_description = 'Type'
    
    def preview(self, obj):
        if obj.video:
            return format_html('<video width="50" height="50" style="border-radius:5px;"><source src="{}" type="video/mp4"></video>', obj.video.url)
        elif obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px; object-fit:cover;" />', obj.image.url)
        return "-"
    preview.short_description = 'Preview'

# ============ FOOTER CONTENT ============
@admin.register(FooterContent)
class FooterContentAdmin(admin.ModelAdmin):
    fields = ('about_text', 'copyright_text')
    
    def has_add_permission(self, request):
        return not FooterContent.objects.exists()