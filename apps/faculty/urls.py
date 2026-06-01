from django.urls import path
from apps.faculty import views

# ── Faculty Portal UI URLs ──────────────────────────────────────────────────
ui_urlpatterns = [
    path('hod/',     views.HODDashboardView.as_view(),    name='hod-dashboard'),
    path('mentor/',  views.MentorTemplatePageView.as_view(template_name='mentor-dashboard-html/index.html'), name='mentor-dashboard'),
    path('mentor/profile/', views.MentorTemplatePageView.as_view(template_name='mentor-dashboard-html/mentor-profile.html'), name='mentor-profile'),
    path('mentor/students/', views.MentorTemplatePageView.as_view(template_name='mentor-dashboard-html/fully-assigned-students.html'), name='mentor-students'),
    path('mentor/courses/', views.MentorTemplatePageView.as_view(template_name='mentor-dashboard-html/courses.html'), name='mentor-courses'),
    path('mentor/courses/data/', views.mentor_courses_api, name='mentor-courses-json'),
    path('mentor/cohorts/', views.MentorTemplatePageView.as_view(template_name='mentor-dashboard-html/cohorts.html'), name='mentor-cohorts'),
    path('mentor/cohorts/data/', views.mentor_cohorts, name='mentor-cohorts-json'),
    path('mentor/assign-marks/', views.MentorTemplatePageView.as_view(template_name='mentor-dashboard-html/assign-mid-marks.html'), name='mentor-assign-marks'),
    path('mentor/upload-attendance/', views.MentorTemplatePageView.as_view(template_name='mentor-dashboard-html/upload-attendance.html'), name='mentor-upload-attendance'),
    path('portal/',  views.FacultyDashboardView.as_view(), name='faculty-dashboard'),
    path('portal/cohorts/', views.FacultyHubCohortsView.as_view(), name='faculty-cohorts'),
    path('portal/explore-students/', views.FacultyHubExploreStudentsView.as_view(), name='faculty-explore-students'),
    path('portal/hod-updates/', views.FacultyHubHodUpdatesView.as_view(), name='faculty-hod-updates'),
    path('portal/courses/', views.FacultyHubCoursesView.as_view(), name='faculty-courses'),
    path('portal/institution-courses/', views.FacultyHubInstitutionCoursesView.as_view(), name='faculty-institution-courses'),
    path('portal/settings/', views.FacultyHubSettingsView.as_view(), name='faculty-settings'),
    path('courses/<str:course_id>/score-template/',
         views.download_score_template, name='score-template-download'),
]

# ── Legacy API URLs (kept for backward compat) ─────────────────────────────
urlpatterns = [
    path('subjects/',      views.FacultySubjectsView.as_view(),      name='faculty-subjects'),
    path('pending-certs/', views.PendingCertificationsView.as_view(), name='pending-certs'),
]
# Expose UI URL patterns as part of the module urlpatterns so Django can reverse them
urlpatterns += ui_urlpatterns
