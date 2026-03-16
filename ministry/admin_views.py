from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q


@login_required
def dashboard(request):
    """Admin dashboard with correct counts"""
    context = {
        'total_pillars': Pillar.objects.count(),
        'total_programs': Program.objects.count(),
        'total_team': TeamMember.objects.count(),
        'total_gallery': GalleryItem.objects.filter(is_active=True).count(),
        'total_announcements': Announcement.objects.filter(is_active=True).count(),
        'total_backgrounds': HeroBackground.objects.filter(is_active=True).count(),
        'total_users': User.objects.filter(is_active=True).count(),
        'staff_users': User.objects.filter(is_staff=True, is_active=True).count(),
        'superusers': User.objects.filter(is_superuser=True, is_active=True).count(),
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_gallery': GalleryItem.objects.filter(is_active=True).order_by('-uploaded_at')[:6],
        'recent_announcements': Announcement.objects.filter(is_active=True).order_by('-date')[:5],
        'site_settings': SiteSettings.objects.first(),
        'active_page': 'dashboard'
    }
    return render(request, 'ministry/admin/dashboard.html', context)

# Site Settings
def site_settings(request):
    settings = SiteSettings.objects.first()
    if not settings:
        settings = SiteSettings.objects.create()
    
    if request.method == 'POST':
        settings.site_name = request.POST.get('site_name')
        settings.registration_number = request.POST.get('registration_number')
        settings.can_number = request.POST.get('can_number')
        settings.mission_statement = request.POST.get('mission_statement')
        settings.email = request.POST.get('email')
        settings.location = request.POST.get('location')
        settings.bank_name = request.POST.get('bank_name')
        settings.account_number = request.POST.get('account_number')
        settings.account_name = request.POST.get('account_name')
        settings.facebook_url = request.POST.get('facebook_url')
        settings.instagram_url = request.POST.get('instagram_url')
        settings.youtube_url = request.POST.get('youtube_url')
        settings.twitter_url = request.POST.get('twitter_url')
        
        # Handle logo upload
        if request.FILES.get('logo'):
            settings.logo = request.FILES['logo']
        
        # Handle WhatsApp numbers (as JSON)
        whatsapp = request.POST.getlist('whatsapp_numbers[]')
        settings.whatsapp_numbers = [w for w in whatsapp if w]
        
        settings.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('ministry_admin:site_settings')
    
    context = {
        'settings': settings,
        'active_page': 'settings'
    }
    return render(request, 'ministry/admin/settings.html', context)

# Pillars CRUD
def pillar_list(request):
    pillars = Pillar.objects.all().order_by('order')
    context = {
        'pillars': pillars,
        'active_page': 'pillars'
    }
    return render(request, 'ministry/admin/pillars/list.html', context)

def pillar_add(request):
    if request.method == 'POST':
        pillar = Pillar.objects.create(
            acronym=request.POST.get('acronym'),
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            icon=request.POST.get('icon', 'bi-award-fill'),
            order=request.POST.get('order', 0)
        )
        messages.success(request, f'Pillar "{pillar.title}" added successfully!')
        return redirect('ministry_admin:pillar_list')
    
    context = {'active_page': 'pillars'}
    return render(request, 'ministry/admin/pillars/add.html', context)

def pillar_edit(request, pk):
    pillar = get_object_or_404(Pillar, pk=pk)
    
    if request.method == 'POST':
        pillar.acronym = request.POST.get('acronym')
        pillar.title = request.POST.get('title')
        pillar.description = request.POST.get('description')
        pillar.icon = request.POST.get('icon')
        pillar.order = request.POST.get('order')
        pillar.save()
        messages.success(request, f'Pillar "{pillar.title}" updated successfully!')
        return redirect('ministry_admin:pillar_list')
    
    context = {
        'pillar': pillar,
        'active_page': 'pillars'
    }
    return render(request, 'ministry/admin/pillars/edit.html', context)

def pillar_delete(request, pk):
    pillar = get_object_or_404(Pillar, pk=pk)
    if request.method == 'POST':
        pillar.delete()
        messages.success(request, 'Pillar deleted successfully!')
    return redirect('ministry_admin:pillar_list')

# Programs CRUD
def program_list(request):
    programs = Program.objects.all().order_by('order')
    context = {
        'programs': programs,
        'active_page': 'programs'
    }
    return render(request, 'ministry/admin/programs/list.html', context)

def program_add(request):
    if request.method == 'POST':
        program = Program.objects.create(
            day=request.POST.get('day'),
            title=request.POST.get('title'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            description=request.POST.get('description'),
            icon=request.POST.get('icon', 'bi-book'),
            order=request.POST.get('order', 0)
        )
        messages.success(request, f'Program "{program.title}" added successfully!')
        return redirect('ministry_admin:program_list')
    
    context = {
        'days': Program.DAY_CHOICES,
        'active_page': 'programs'
    }
    return render(request, 'ministry/admin/programs/add.html', context)

def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)
    
    if request.method == 'POST':
        program.day = request.POST.get('day')
        program.title = request.POST.get('title')
        program.start_time = request.POST.get('start_time')
        program.end_time = request.POST.get('end_time')
        program.description = request.POST.get('description')
        program.icon = request.POST.get('icon')
        program.order = request.POST.get('order')
        program.save()
        messages.success(request, f'Program "{program.title}" updated successfully!')
        return redirect('ministry_admin:program_list')
    
    context = {
        'program': program,
        'days': Program.DAY_CHOICES,
        'active_page': 'programs'
    }
    return render(request, 'ministry/admin/programs/edit.html', context)

def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        program.delete()
        messages.success(request, 'Program deleted successfully!')
    return redirect('ministry_admin:program_list')

# Team Members CRUD
def team_list(request):
    members = TeamMember.objects.all().order_by('order')
    context = {
        'members': members,
        'active_page': 'team'
    }
    return render(request, 'ministry/admin/team/list.html', context)

def team_add(request):
    if request.method == 'POST':
        member = TeamMember.objects.create(
            name=request.POST.get('name'),
            position=request.POST.get('position'),
            order=request.POST.get('order', 0)
        )
        
        if request.FILES.get('photo'):
            member.photo = request.FILES['photo']
            member.save()
            
        messages.success(request, f'Team member "{member.name}" added successfully!')
        return redirect('ministry_admin:team_list')
    
    context = {'active_page': 'team'}
    return render(request, 'ministry/admin/team/add.html', context)

def team_edit(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    
    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.position = request.POST.get('position')
        member.order = request.POST.get('order')
        
        if request.FILES.get('photo'):
            # Delete old photo
            if member.photo:
                if os.path.isfile(member.photo.path):
                    os.remove(member.photo.path)
            member.photo = request.FILES['photo']
        
        member.save()
        messages.success(request, f'Team member "{member.name}" updated successfully!')
        return redirect('ministry_admin:team_list')
    
    context = {
        'member': member,
        'active_page': 'team'
    }
    return render(request, 'ministry/admin/team/edit.html', context)

def team_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        # Delete photo file
        if member.photo:
            if os.path.isfile(member.photo.path):
                os.remove(member.photo.path)
        member.delete()
        messages.success(request, 'Team member deleted successfully!')
    return redirect('ministry_admin:team_list')

@login_required
def gallery_list(request):
    """Gallery list with proper counts"""
    # Get filter parameters
    media_type = request.GET.get('type', 'all')
    status = request.GET.get('status', 'all')
    search = request.GET.get('search', '')
    
    # Base queryset
    images = GalleryItem.objects.all()
    
    # Apply filters
    if media_type != 'all':
        images = images.filter(media_type=media_type)
    if status == 'active':
        images = images.filter(is_active=True)
    elif status == 'inactive':
        images = images.filter(is_active=False)
    if search:
        images = images.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Order by order field
    images = images.order_by('order', '-uploaded_at')
    
    # Get counts for stats
    total_images = GalleryItem.objects.count()
    active_images = GalleryItem.objects.filter(is_active=True).count()
    inactive_images = GalleryItem.objects.filter(is_active=False).count()
    
    # Type counts
    image_count = GalleryItem.objects.filter(media_type='image').count()
    video_count = GalleryItem.objects.filter(media_type='video').count()
    flyer_count = GalleryItem.objects.filter(media_type='flyer').count()
    
    context = {
        'images': images,
        'total_images': total_images,
        'active_images': active_images,
        'inactive_images': inactive_images,
        'image_count': image_count,
        'video_count': video_count,
        'flyer_count': flyer_count,
        'active_page': 'gallery',
        'current_filters': {
            'type': media_type,
            'status': status,
            'search': search
        }
    }
    return render(request, 'ministry/admin/gallery/list.html', context)

@login_required
def gallery_add(request):
    """Add new gallery item with proper file handling"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            media_type = request.POST.get('media_type')
            order = request.POST.get('order', 0)
            is_active = request.POST.get('is_active') == 'on'
            
            # Validate required fields
            if not title:
                messages.error(request, 'Title is required')
                return redirect('ministry_admin:gallery_add')
            
            if not media_type:
                messages.error(request, 'Media type is required')
                return redirect('ministry_admin:gallery_add')
            
            # Create gallery item
            gallery_item = GalleryItem.objects.create(
                title=title,
                description=description,
                media_type=media_type,
                order=order,
                is_active=is_active
            )
            
            # Handle file upload
            if request.FILES.get('file'):
                gallery_item.file = request.FILES['file']
                gallery_item.save()
                messages.success(request, f'File uploaded: {request.FILES["file"].name}')
            else:
                messages.error(request, 'No file was uploaded')
                gallery_item.delete()
                return redirect('ministry_admin:gallery_add')
            
            # Handle thumbnail upload for videos
            if media_type == 'video' and request.FILES.get('thumbnail'):
                gallery_item.thumbnail = request.FILES['thumbnail']
                gallery_item.save()
                messages.success(request, 'Thumbnail uploaded successfully')
            
            messages.success(request, f'Gallery item "{title}" added successfully!')
            return redirect('ministry_admin:gallery_list')
            
        except Exception as e:
            messages.error(request, f'Error uploading file: {str(e)}')
            return redirect('ministry_admin:gallery_add')
    
    context = {
        'active_page': 'gallery',
        'media_types': GalleryItem.MEDIA_TYPES
    }
    return render(request, 'ministry/admin/gallery/add.html', context)

@login_required
def gallery_edit(request, pk):
    """Edit gallery item"""
    image = get_object_or_404(GalleryItem, pk=pk)
    
    if request.method == 'POST':
        try:
            image.title = request.POST.get('title')
            image.description = request.POST.get('description', '')
            image.media_type = request.POST.get('media_type')
            image.order = request.POST.get('order', 0)
            image.is_active = request.POST.get('is_active') == 'on'
            
            # Handle new file upload
            if request.FILES.get('file'):
                # Delete old file
                if image.file and os.path.isfile(image.file.path):
                    os.remove(image.file.path)
                image.file = request.FILES['file']
            
            # Handle new thumbnail
            if request.FILES.get('thumbnail'):
                # Delete old thumbnail
                if image.thumbnail and os.path.isfile(image.thumbnail.path):
                    os.remove(image.thumbnail.path)
                image.thumbnail = request.FILES['thumbnail']
            
            image.save()
            messages.success(request, f'Gallery item "{image.title}" updated successfully!')
            return redirect('ministry_admin:gallery_list')
            
        except Exception as e:
            messages.error(request, f'Error updating item: {str(e)}')
    
    context = {
        'image': image,
        'active_page': 'gallery',
        'media_types': GalleryItem.MEDIA_TYPES
    }
    return render(request, 'ministry/admin/gallery/edit.html', context)

@login_required
def gallery_delete(request, pk):
    """Delete gallery item and its files"""
    image = get_object_or_404(GalleryItem, pk=pk)
    
    if request.method == 'POST':
        try:
            # Delete files
            if image.file and os.path.isfile(image.file.path):
                os.remove(image.file.path)
            if image.thumbnail and os.path.isfile(image.thumbnail.path):
                os.remove(image.thumbnail.path)
            
            title = image.title
            image.delete()
            messages.success(request, f'Gallery item "{title}" deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting item: {str(e)}')
    
    return redirect('ministry_admin:gallery_list')


# Hero Section Edit
def hero_edit(request):
    hero = HeroContent.objects.first()
    if not hero:
        hero = HeroContent.objects.create()
    
    if request.method == 'POST':
        hero.main_title = request.POST.get('main_title')
        hero.subtitle = request.POST.get('subtitle')
        hero.description = request.POST.get('description')
        hero.button1_text = request.POST.get('button1_text')
        hero.button1_link = request.POST.get('button1_link')
        hero.button2_text = request.POST.get('button2_text')
        hero.button2_link = request.POST.get('button2_link')
        
        if request.FILES.get('background_image'):
            if hero.background_image:
                if os.path.isfile(hero.background_image.path):
                    os.remove(hero.background_image.path)
            hero.background_image = request.FILES['background_image']
            hero.background_video = None
        
        if request.FILES.get('background_video'):
            if hero.background_video:
                if os.path.isfile(hero.background_video.path):
                    os.remove(hero.background_video.path)
            hero.background_video = request.FILES['background_video']
            hero.background_image = None
        
        hero.save()
        messages.success(request, 'Hero section updated successfully!')
        return redirect('ministry_admin:hero_edit')
    
    context = {
        'hero': hero,
        'active_page': 'hero'
    }
    return render(request, 'ministry/admin/hero/edit.html', context)

# Leader Edit
def leader_edit(request):
    leader = Leader.objects.first()
    if not leader:
        leader = Leader.objects.create()
    
    if request.method == 'POST':
        leader.name = request.POST.get('name')
        leader.title = request.POST.get('title')
        leader.bio = request.POST.get('bio')
        
        if request.FILES.get('photo'):
            if leader.photo:
                if os.path.isfile(leader.photo.path):
                    os.remove(leader.photo.path)
            leader.photo = request.FILES['photo']
        
        leader.save()
        messages.success(request, 'Leader information updated successfully!')
        return redirect('ministry_admin:leader_edit')
    
    context = {
        'leader': leader,
        'active_page': 'leader'
    }
    return render(request, 'ministry/admin/leader/edit.html', context)

# Group Photo
def group_photo(request):
    group = GroupPhoto.objects.first()
    if not group:
        group = GroupPhoto.objects.create()
    
    if request.method == 'POST':
        group.title = request.POST.get('title')
        group.caption = request.POST.get('caption')
        group.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('photo'):
            if group.photo:
                if os.path.isfile(group.photo.path):
                    os.remove(group.photo.path)
            group.photo = request.FILES['photo']
        
        group.save()
        messages.success(request, 'Group photo updated successfully!')
        return redirect('ministry_admin:group_photo')
    
    context = {
        'group': group,
        'active_page': 'group_photo'
    }
    return render(request, 'ministry/admin/group_photo/edit.html', context)

# Custom Logout
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')

def user_list(request):
    """List all admin users"""
    users = User.objects.all().order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(username__icontains=search_query) | \
                users.filter(email__icontains=search_query) | \
                users.filter(first_name__icontains=search_query) | \
                users.filter(last_name__icontains=search_query)
    
    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_users': User.objects.count(),
        'active_page': 'users'
    }
    return render(request, 'ministry/admin/users/list.html', context)

def user_add(request):
    """Add a new admin user"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        
        # Validation
        errors = []
        if not username:
            errors.append('Username is required')
        if not email:
            errors.append('Email is required')
        if not password:
            errors.append('Password is required')
        if password != confirm_password:
            errors.append('Passwords do not match')
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists')
        if User.objects.filter(email=email).exists():
            errors.append('Email already exists')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            
            messages.success(request, f'User "{username}" created successfully!')
            return redirect('ministry_admin:user_list')
    
    context = {
        'active_page': 'users'
    }
    return render(request, 'ministry/admin/users/add.html', context)

def user_edit(request, pk):
    """Edit an existing user"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        errors = []
        if not username:
            errors.append('Username is required')
        if not email:
            errors.append('Email is required')
        
        # Check if username already exists (excluding current user)
        if User.objects.filter(username=username).exclude(pk=pk).exists():
            errors.append('Username already exists')
        
        # Check if email already exists (excluding current user)
        if User.objects.filter(email=email).exclude(pk=pk).exists():
            errors.append('Email already exists')
        
        # Password validation if changing
        if new_password:
            if new_password != confirm_password:
                errors.append('New passwords do not match')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Update user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            
            if new_password:
                user.set_password(new_password)
            
            user.save()
            messages.success(request, f'User "{username}" updated successfully!')
            return redirect('ministry_admin:user_list')
    
    context = {
        'edit_user': user,
        'active_page': 'users'
    }
    return render(request, 'ministry/admin/users/edit.html', context)

def user_delete(request, pk):
    """Delete a user"""
    user = get_object_or_404(User, pk=pk)
    
    # Prevent deleting yourself
    if request.user.pk == user.pk:
        messages.error(request, 'You cannot delete your own account!')
        return redirect('ministry_admin:user_list')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
    
    return redirect('ministry_admin:user_list')

def user_toggle_staff(request, pk):
    """Toggle staff status"""
    user = get_object_or_404(User, pk=pk)
    
    # Prevent toggling yourself
    if request.user.pk == user.pk:
        messages.error(request, 'You cannot change your own status!')
        return redirect('ministry_admin:user_list')
    
    user.is_staff = not user.is_staff
    user.save()
    status = 'granted' if user.is_staff else 'revoked'
    messages.success(request, f'Staff access {status} for "{user.username}"')
    
    return redirect('ministry_admin:user_list')

def user_toggle_superuser(request, pk):
    """Toggle superuser status"""
    user = get_object_or_404(User, pk=pk)
    
    # Prevent toggling yourself
    if request.user.pk == user.pk:
        messages.error(request, 'You cannot change your own superuser status!')
        return redirect('ministry_admin:user_list')
    
    user.is_superuser = not user.is_superuser
    user.save()
    status = 'granted' if user.is_superuser else 'revoked'
    messages.success(request, f'Superuser access {status} for "{user.username}"')
    
    return redirect('ministry_admin:user_list')

def user_reset_password(request, pk):
    """Reset user password"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, f'Password reset successfully for "{user.username}"')
        else:
            messages.error(request, 'Passwords do not match or are empty')
    
    return redirect('ministry_admin:user_edit', pk=pk)

def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-date')
    
    search_query = request.GET.get('search', '')
    if search_query:
        announcements = announcements.filter(title__icontains=search_query)
    
    paginator = Paginator(announcements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_announcements': Announcement.objects.count(),
        'active_page': 'announcements'
    }
    return render(request, 'ministry/admin/announcements/list.html', context)

def announcement_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        is_active = request.POST.get('is_active') == 'on'
        
        announcement = Announcement.objects.create(
            title=title,
            description=description,
            date=date,
            is_active=is_active
        )
        
        if request.FILES.get('image'):
            announcement.image = request.FILES['image']
        
        if request.FILES.get('file'):
            announcement.file = request.FILES['file']
        
        announcement.save()
        messages.success(request, f'Announcement "{title}" added successfully!')
        return redirect('ministry_admin:announcement_list')
    
    context = {'active_page': 'announcements'}
    return render(request, 'ministry/admin/announcements/add.html', context)

def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        announcement.title = request.POST.get('title')
        announcement.description = request.POST.get('description')
        announcement.date = request.POST.get('date')
        announcement.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('image'):
            if announcement.image:
                if os.path.isfile(announcement.image.path):
                    os.remove(announcement.image.path)
            announcement.image = request.FILES['image']
        
        if request.FILES.get('file'):
            if announcement.file:
                if os.path.isfile(announcement.file.path):
                    os.remove(announcement.file.path)
            announcement.file = request.FILES['file']
        
        announcement.save()
        messages.success(request, f'Announcement "{announcement.title}" updated successfully!')
        return redirect('ministry_admin:announcement_list')
    
    context = {
        'announcement': announcement,
        'active_page': 'announcements'
    }
    return render(request, 'ministry/admin/announcements/edit.html', context)

def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        if announcement.image and os.path.isfile(announcement.image.path):
            os.remove(announcement.image.path)
        if announcement.file and os.path.isfile(announcement.file.path):
            os.remove(announcement.file.path)
        
        title = announcement.title
        announcement.delete()
        messages.success(request, f'Announcement "{title}" deleted successfully!')
    
    return redirect('ministry_admin:announcement_list')

# Hero Background Views
def hero_background_list(request):
    backgrounds = HeroBackground.objects.all()
    
    context = {
        'backgrounds': backgrounds,
        'total_backgrounds': backgrounds.count(),
        'active_page': 'hero_backgrounds'
    }
    return render(request, 'ministry/admin/hero_backgrounds/list.html', context)

def hero_background_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        is_active = request.POST.get('is_active') == 'on'
        
        background = HeroBackground.objects.create(
            title=title,
            is_active=is_active
        )
        
        if request.FILES.get('video'):
            background.video = request.FILES['video']
        
        if request.FILES.get('image'):
            background.image = request.FILES['image']
        
        background.save()
        messages.success(request, f'Background "{title}" added successfully!')
        return redirect('ministry_admin:hero_backgrounds')
    
    context = {'active_page': 'hero_backgrounds'}
    return render(request, 'ministry/admin/hero_backgrounds/add.html', context)

def hero_background_edit(request, pk):
    background = get_object_or_404(HeroBackground, pk=pk)
    
    if request.method == 'POST':
        background.title = request.POST.get('title')
        background.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('video'):
            if background.video and os.path.isfile(background.video.path):
                os.remove(background.video.path)
            background.video = request.FILES['video']
        
        if request.FILES.get('image'):
            if background.image and os.path.isfile(background.image.path):
                os.remove(background.image.path)
            background.image = request.FILES['image']
        
        background.save()
        messages.success(request, f'Background updated successfully!')
        return redirect('ministry_admin:hero_backgrounds')
    
    context = {
        'background': background,
        'active_page': 'hero_backgrounds'
    }
    return render(request, 'ministry/admin/hero_backgrounds/edit.html', context)

def hero_background_delete(request, pk):
    background = get_object_or_404(HeroBackground, pk=pk)
    
    if request.method == 'POST':
        if background.video and os.path.isfile(background.video.path):
            os.remove(background.video.path)
        if background.image and os.path.isfile(background.image.path):
            os.remove(background.image.path)
        
        background.delete()
        messages.success(request, 'Background deleted successfully!')
    
    return redirect('ministry_admin:hero_backgrounds')