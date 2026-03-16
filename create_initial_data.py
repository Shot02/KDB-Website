import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KDB.settings')
django.setup()

from ministry.models import *

print("Creating initial data...")

# Create Site Settings
settings, created = SiteSettings.objects.get_or_create(
    pk=1,
    defaults={
        'site_name': "KDB Kingdom Disciples Builders",
        'registration_number': "RC. 2614946",
        'can_number': "CAN 0294",
        'mission_statement': "Provoke revival in the church through effective evangelism, soul winning activities, leadership empowerment and ministerial training. Stand to build the disciples of the kingdom. Enhance integrity and effectiveness of Christian ministry.",
        'whatsapp_numbers': ["08052602905", "08060379587", "09044000736"],
        'email': "revottop@gmail.com",
        'location': "Nigeria",
        'bank_name': "UBA",
        'account_number': "2191091914",
        'account_name': "KDB OTTO OUTREACH"
    }
)
if created:
    print("✓ Site Settings created")
else:
    print("✓ Site Settings already exists")

# Create Pillars
pillars_data = [
    {"acronym": "LEP", "title": "Leadership Empowerment Program", 
     "description": "We organize ministers seminars, workshops to build and empower leaders", 
     "icon": "bi-award-fill", "order": 1},
    {"acronym": "EBO", "title": "Evangelism by Objective", 
     "description": "We train and rebuild the church membership into soul winning evangelism with different methods, strategies and approaches of soul winning effective evangelism", 
     "icon": "bi-megaphone-fill", "order": 2},
    {"acronym": "DF", "title": "Discipleship Forum", 
     "description": "We build up bible based disciples that can provoke revival in their communities", 
     "icon": "bi-people-fill", "order": 3},
    {"acronym": "ISL", "title": "Int'l School of Leadership", 
     "description": "Training and modeling ministers of God in the function of their ministerial assignment", 
     "icon": "bi-globe", "order": 4},
]

for pillar_data in pillars_data:
    pillar, created = Pillar.objects.get_or_create(
        acronym=pillar_data["acronym"],
        defaults=pillar_data
    )
    if created:
        print(f"✓ Pillar {pillar_data['acronym']} created")

# Create Missions
missions_data = [
    {"title": "Reach the Unreached", 
     "description": "We reach the unreached and take the light of the gospel to rural areas", 
     "icon": "bi-heart-fill", "order": 1},
    {"title": "Train Ministers", 
     "description": "Training ministers in the function of their ministerial assignment", 
     "icon": "bi-book-fill", "order": 2},
    {"title": "Bring Revival", 
     "description": "Provoke revival in the church through effective evangelism", 
     "icon": "bi-fire", "order": 3},
]

for mission_data in missions_data:
    mission, created = Mission.objects.get_or_create(
        title=mission_data["title"],
        defaults=mission_data
    )
    if created:
        print(f"✓ Mission {mission_data['title']} created")

# Create Programs
programs_data = [
    {"day": "Monday", "title": "Bible Teaching", "start_time": "14:00", "end_time": "16:00", 
     "icon": "bi-book", "order": 1},
    {"day": "Tuesday", "title": "Bible Education", "start_time": "16:00", "end_time": "18:00", 
     "icon": "bi-journal-bookmark", "order": 2},
    {"day": "Thursday", "title": "Bible Education", "start_time": "16:00", "end_time": "18:00", 
     "icon": "bi-journal-bookmark", "order": 3},
    {"day": "Friday", "title": "ISL Training Class", "start_time": "16:00", "end_time": "18:00", 
     "icon": "bi-mortarboard", "order": 4},
    {"day": "Saturday", "title": "ISL Training Class", "start_time": "09:00", "end_time": "12:00", 
     "icon": "bi-person-workspace", "order": 5},
    {"day": "Sunday", "title": "Sunday Service", "start_time": "07:30", "end_time": "11:00", 
     "icon": "bi-building", "order": 6},
]

for program_data in programs_data:
    program, created = Program.objects.get_or_create(
        day=program_data["day"],
        title=program_data["title"],
        start_time=program_data["start_time"],
        defaults=program_data
    )
    if created:
        print(f"✓ Program {program_data['day']} - {program_data['title']} created")

# Create Team Members
team_data = [
    {"name": "Rev Dr. Otto", "position": "Presiding Leader", "order": 1},
    {"name": "Lydia Otto", "position": "General Supervisor", "order": 2},
    {"name": "Sis. Esther", "position": "Head of Evangelism", "order": 3},
    {"name": "Bro. Barnabas", "position": "Head of Welfare", "order": 4},
    {"name": "Bro. Shalom", "position": "Head of Media", "order": 5},
    {"name": "Sis. Mary", "position": "Head of Choir", "order": 6},
    {"name": "Bro. Jacob", "position": "Head of Technical", "order": 7},
]

for member_data in team_data:
    member, created = TeamMember.objects.get_or_create(
        name=member_data["name"],
        defaults=member_data
    )
    if created:
        print(f"✓ Team Member {member_data['name']} created")

# Create Group Photo
group, created = GroupPhoto.objects.get_or_create(
    pk=1,
    defaults={
        'title': "KDB OTTO OUTREACH Family",
        'caption': "All Members",
        'is_active': True
    }
)
if created:
    print("✓ Group Photo created")

# Create Leader
leader, created = Leader.objects.get_or_create(
    pk=1,
    defaults={
        'name': "Rev Dr. Otto",
        'title': "Presiding Leader & Founder",
        'bio': """Rev Dr. Otto is a dedicated servant of God with a passion for reaching the unreached and bringing the light of the gospel to rural communities. With years of ministerial experience, he has been instrumental in training ministers and fostering revival among churches.

Under his leadership, KDB OTTO OUTREACH has grown to become a beacon of hope, touching countless lives through the five pillars of the ministry. His vision for Leadership Empowerment, Strategic Evangelism, Discipleship, and International Leadership Training continues to transform lives across nations.

Rev Dr. Otto believes in the power of unity among ministers and works tirelessly to bring revival in the church and among fellow ministers of the gospel."""
    }
)
if created:
    print("✓ Leader created")

# Create Hero Content
hero, created = HeroContent.objects.get_or_create(
    pk=1,
    defaults={
        'main_title': "KDB",
        'subtitle': "Kingdom Disciples Builders",
        'description': "We reach the unreached and take the light of the gospel to rural areas. Training ministers in the function of their ministerial assignment, bringing revival in church and among ministers.",
        'button1_text': "Explore Our Pillars",
        'button1_link': "#pillars",
        'button2_text': "Contact Us",
        'button2_link': "#contact"
    }
)
if created:
    print("✓ Hero Content created")

# Create Footer Content
footer, created = FooterContent.objects.get_or_create(
    pk=1,
    defaults={
        'about_text': "Kingdom Disciples Builders OTTO OUTREACH Ministry - Reaching the unreached and taking the light of the gospel to rural areas.",
        'copyright_text': "© 2026g KDB OTTO OUTREACH Ministry. All Rights Reserved."
    }
)
if created:
    print("✓ Footer Content created")

print("\n Initial data creation completed!")