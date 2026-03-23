from django.contrib import admin
from apps.faculty.models import Cohort, InstitutionCourse, TrainingProgram, StudentMentorAssignment


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ("name", "cohort_type", "department", "created_by", "is_active")
    list_filter = ("cohort_type", "is_active", "department")
    search_fields = ("name", "created_by__email")
    ordering = ("-created_at",)


@admin.register(InstitutionCourse)
class InstitutionCourseAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "created_by", "is_published_to_profile")
    list_filter = ("category", "is_published_to_profile")
    search_fields = ("name", "created_by__email")
    ordering = ("-created_at",)


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "start_date", "end_date", "is_active")
    list_filter = ("department", "is_active")
    search_fields = ("title", "department__name")
    ordering = ("-start_date",)


@admin.register(StudentMentorAssignment)
class StudentMentorAssignmentAdmin(admin.ModelAdmin):
    list_display = ("mentor", "academic_year", "assigned_by")
    list_filter = ("academic_year",)
    search_fields = ("mentor__email",)
