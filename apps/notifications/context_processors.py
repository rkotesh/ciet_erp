from django.db.models import Q
from .models import Notification, NotificationRecipient
from apps.academics.models import Department

def notification_context(request):
    if not request.user.is_authenticated:
        return {}
    
    user = request.user
    user_departments = list(user.departments.all())
    if user.role == 'HOD' and not user_departments:
        hod_dept = Department.objects.filter(hod=user).first()
        if hod_dept:
            user_departments = [hod_dept]
    if user.role == 'Student' and hasattr(user, 'student_profile'):
        user_departments = [user.student_profile.department]
    if user.role == 'Parent' and hasattr(user, 'parent_profile'):
        user_departments = list(
            Department.objects.filter(students__parents=user.parent_profile).distinct()
        )
    # Count notifications that are for this user but not marked as read in NotificationRecipient
    # A bit tricky for mass notifications.
    # Logic: Total matching notifications - count of NotificationRecipient where is_read=True
    
    dept_filter = Q(target_department__isnull=True)
    if user_departments:
        dept_filter = dept_filter | Q(target_department__in=user_departments)

    total_relevant = Notification.objects.filter(
        Q(is_global=True) |
        (
            (Q(target_role='All') | Q(target_role=user.role)) &
            dept_filter
        )
    ).count()
    
    read_count = NotificationRecipient.objects.filter(user=user, is_read=True).count()
    
    unread_count = max(0, total_relevant - read_count)
    
    return {
        'unread_notifications_count': unread_count
    }
