from django.db import models
from django.core.exceptions import ValidationError
import os

# ============ VALIDATOR FUNCTIONS ============
def validate_file_size(file):
    """Validate file size - max 20MB"""
    max_size_mb = 20
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size cannot exceed {max_size_mb}MB. Current file size: {file.size / 1024 / 1024:.2f}MB")

def validate_image_file(file):
    """Validate image files"""
    # Check file size
    validate_file_size(file)
    
    # Check if it's actually an image
    valid_image_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if file.content_type not in valid_image_types:
        raise ValidationError(f"File must be an image. Received: {file.content_type}")
    
    # Check file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed: {', '.join(valid_extensions)}")

def validate_video_file(file):
    """Validate video files"""
    # Check file size
    validate_file_size(file)
    
    # Check if it's actually a video
    valid_video_types = ['video/mp4', 'video/webm', 'video/ogg', 'video/quicktime']
    if file.content_type not in valid_video_types:
        raise ValidationError(f"File must be a video. Received: {file.content_type}")
    
    # Check file extension
    valid_extensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported video format. Allowed: {', '.join(valid_extensions)}")

def validate_pdf_file(file):
    """Validate PDF files"""
    # Check file size
    validate_file_size(file)
    
    # Check if it's PDF or image
    valid_types = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
    if file.content_type not in valid_types:
        raise ValidationError(f"File must be PDF or image. Received: {file.content_type}")

# ============ SITE SETTINGS ============
class SiteSettings(models.Model):
    """Global site settings - singleton model"""
    site_name = models.CharField(max_length=200, default="KDB Kingdom Disciples Builders")
    registration_number = models.CharField(max_length=50, default="RC. 2614946")
    can_number = models.CharField(max_length=50, default="CAN 0294")
    mission_statement = models.TextField(
        default="Provoke revival in the church through effective evangelism, soul winning activities, leadership empowerment and ministerial training. Stand to build the disciples of the kingdom. Enhance integrity and effectiveness of Christian ministry."
    )
    
    # Logo
    logo = models.ImageField(
        upload_to='logos/', 
        blank=True, 
        null=True,
        validators=[validate_image_file],
        help_text='Upload ministry logo (JPG, PNG)'
    )
    
    # Contact Info
    whatsapp_numbers = models.JSONField(default=list, help_text='Format: ["08052602905", "08060379587"]')
    email = models.EmailField(default="revottop@gmail.com")
    location = models.CharField(max_length=200, default="Nigeria")
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    # Bank Details
    bank_name = models.CharField(max_length=100, default="UBA")
    account_number = models.CharField(max_length=20, default="2191091914")
    account_name = models.CharField(max_length=200, default="KDB OTTO OUTREACH")
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name
    
    def clean(self):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("You can only have one Site Settings instance")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

# ============ PROGRAMS ============
class Program(models.Model):
    """Weekly/Daily Programs"""
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    title = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="bi-book")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Added null=True
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)      # Added null=True
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.day} - {self.title}"


# ============ PILLARS ============
class Pillar(models.Model):
    """Five Pillars of the Ministry"""
    acronym = models.CharField(max_length=10, help_text="e.g., LEP, EBO, DF, ISL")
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="bi-award-fill")
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Added null=True
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)      # Added null=True
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.acronym} - {self.title}"

# ============ MISSIONS ============
class Mission(models.Model):
    """Mission points"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default="bi-heart-fill")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

# ============ TEAM MEMBERS ============
class TeamMember(models.Model):
    """Leadership Team"""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    photo = models.ImageField(
        upload_to='team/', 
        blank=True, 
        null=True,
        validators=[validate_image_file]
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Added null=True
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)      # Added null=True
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name



# ============ GROUP PHOTO ============
class GroupPhoto(models.Model):
    """Group photo for the team section"""
    title = models.CharField(max_length=200, default="KDB OTTO OUTREACH Family")
    caption = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(
        upload_to='group/', 
        blank=True, 
        null=True,
        validators=[validate_image_file]
    )
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Group Photo"
        verbose_name_plural = "Group Photos"
    
    def __str__(self):
        return self.title

# ============ LEADER ============
class Leader(models.Model):
    """Presiding Leader Information"""
    name = models.CharField(max_length=200, default="Rev Dr. Otto")
    title = models.CharField(max_length=200, default="Presiding Leader & Founder")
    bio = models.TextField()
    photo = models.ImageField(
        upload_to='leaders/', 
        blank=True, 
        null=True,
        validators=[validate_image_file]
    )
    
    class Meta:
        verbose_name = "Presiding Leader"
        verbose_name_plural = "Presiding Leader"
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.pk and Leader.objects.exists():
            raise ValidationError("You can only have one Presiding Leader")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

# ============ GALLERY ITEM ============
class GalleryItem(models.Model):
    """Gallery items supporting images, videos, and flyers"""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('flyer', 'Flyer/Poster'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    file = models.FileField(
        upload_to='gallery/%Y/%m/', 
        validators=[validate_file_size],
        help_text='Upload image, video, or flyer'
    )
    thumbnail = models.ImageField(
        upload_to='gallery/thumbnails/%Y/%m/', 
        blank=True, 
        null=True,
        validators=[validate_image_file],
        help_text='Optional thumbnail for videos'
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Added null=True
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)      # Added null=True
    
    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = 'Gallery Item'
        verbose_name_plural = 'Gallery Items'
    
    def __str__(self):
        return f"{self.title} ({self.media_type})"

# ============ ANNOUNCEMENTS ============
class Announcement(models.Model):
    """Announcements and events with flyers"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(
        upload_to='announcements/%Y/%m/', 
        blank=True, 
        null=True,
        validators=[validate_image_file]
    )
    file = models.FileField(
        upload_to='announcements/files/%Y/%m/', 
        blank=True, 
        null=True,
        validators=[validate_pdf_file],
        help_text='Upload flyer PDF or image'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Added null=True
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)      # Added null=True
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
    
    def __str__(self):
        return self.title

# ============ HERO CONTENT ============
class HeroContent(models.Model):
    """Hero section content"""
    main_title = models.CharField(max_length=200, default="KDB")
    subtitle = models.CharField(max_length=200, default="Kingdom Disciples Builders")
    description = models.TextField(
        default="We reach the unreached and take the light of the gospel to rural areas. Training ministers in the function of their ministerial assignment, bringing revival in church and among ministers."
    )
    button1_text = models.CharField(max_length=50, default="Explore Our Pillars")
    button1_link = models.CharField(max_length=200, default="#pillars")
    button2_text = models.CharField(max_length=50, default="Contact Us")
    button2_link = models.CharField(max_length=200, default="#contact")
    background_image = models.ImageField(
        upload_to='hero/', 
        blank=True, 
        null=True,
        validators=[validate_image_file]
    )
    background_video = models.FileField(
        upload_to='hero/', 
        blank=True, 
        null=True,
        validators=[validate_video_file]
    )
    
    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"
    
    def __str__(self):
        return "Hero Content"
    
    def clean(self):
        if not self.pk and HeroContent.objects.exists():
            raise ValidationError("You can only have one Hero Content")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

# ============ HERO BACKGROUND ============
class HeroBackground(models.Model):
    """Hero section backgrounds (video or image)"""
    title = models.CharField(max_length=200, blank=True)
    video = models.FileField(
        upload_to='hero/backgrounds/', 
        blank=True, 
        null=True,
        validators=[validate_video_file],
        help_text='Upload background video (MP4 recommended)'
    )
    image = models.ImageField(
        upload_to='hero/backgrounds/', 
        blank=True, 
        null=True,
        validators=[validate_image_file],
        help_text='Fallback image for hero section'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Added null=True
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)      # Added null=True
    
    class Meta:
        verbose_name = "Hero Background"
        verbose_name_plural = "Hero Backgrounds"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title or f"Hero Background {self.id}"

# ============ FOOTER CONTENT ============
class FooterContent(models.Model):
    """Footer content"""
    about_text = models.TextField(
        default="Kingdom Disciples Builders OTTO OUTREACH Ministry - Reaching the unreached and taking the light of the gospel to rural areas."
    )
    copyright_text = models.CharField(
        max_length=200, 
        default="© 2024 KDB OTTO OUTREACH Ministry. All Rights Reserved."
    )
    
    class Meta:
        verbose_name = "Footer Content"
        verbose_name_plural = "Footer Content"
    
    def __str__(self):
        return "Footer Settings"
    
    def clean(self):
        if not self.pk and FooterContent.objects.exists():
            raise ValidationError("You can only have one Footer Content")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)