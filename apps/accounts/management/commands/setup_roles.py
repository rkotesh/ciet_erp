from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


ROLE_PERMISSIONS = {
    'Director':  ['*'],  # All permissions (clarity; superuser already bypasses),
    'Examcell':  ['view_marks', 'view_attendance'],
    'HOD':       [
        # Mentor assignments
        'add_mentorassignment', 'change_mentorassignment', 'view_mentorassignment',
        # Updates on Training Programs
        'add_trainingprogram', 'change_trainingprogram', 'view_trainingprogram',
        # Department announcements (core.Announcement)
        'add_announcement', 'change_announcement', 'view_announcement',
        # Course / semester timetables and academic calendars
        'add_timetable', 'change_timetable', 'view_timetable',
        'add_academiccalendar', 'change_academiccalendar', 'view_academiccalendar',
    ],
    'Mentor':    ['add_marks', 'add_attendance', 'view_studentprofile'],
    'Faculty':   ['add_course', 'add_assessment', 'view_cohort'],
    'Student':   ['view_marks', 'view_attendance', 'change_studentprofile', 'add_certification'],
    'Parent':    ['view_marks', 'view_attendance'],
}


class Command(BaseCommand):
    help = 'Create default role groups and permissions'

    def handle(self, *args, **options):
        for role_name, perm_codenames in ROLE_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=role_name)
            if '*' in perm_codenames:
                perms = Permission.objects.all()
            else:
                perms = Permission.objects.filter(codename__in=perm_codenames)
            group.permissions.set(perms)
            self.stdout.write(f'✓ Role {role_name} configured')
