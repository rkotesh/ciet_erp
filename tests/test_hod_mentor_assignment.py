import pytest
from django.urls import reverse
from django.utils import timezone
from django.test import Client
from apps.accounts.models import User
from apps.academics.models import Department, Section
from apps.students.models import StudentProfile
from apps.faculty.models import StudentMentorAssignment

@pytest.mark.django_db
def test_class_split_mentor_assignment():
    client = Client()
    
    # 1. Setup Department & HOD
    dept = Department.objects.create(name="Computer Science", code="CS")
    hod = User.objects.create(email="hod@cs.com", role="HOD")
    dept.hod = hod
    dept.save()
    
    # 2. Setup Section
    section = Section.objects.create(name="A", department=dept)
    
    # 3. Setup Mentors
    mentor_1 = User.objects.create(email="mentor1@cs.com", role="Mentor")
    mentor_2 = User.objects.create(email="mentor2@cs.com", role="Mentor")
    mentor_1.departments.add(dept)
    mentor_2.departments.add(dept)
    
    # 4. Setup 4 Students (R001 - R004)
    students = []
    for i in range(1, 5):
        user = User.objects.create(email=f"student{i}@cs.com", role="Student")
        profile = StudentProfile.objects.create(
            user=user,
            roll_no=f"R00{i}",
            batch="2022-2026",
            department=dept,
            section=section
        )
        students.append(profile)
        
    # Log in HOD
    client.force_login(hod)
    
    # 5. POST to HOD Dashboard for mentor split assignment
    url = reverse('hod-dashboard')
    response = client.post(url, {
        'action': 'assign_mentor_halves',
        'batch': '2022-2026',
        'section_id': section.id,
        'mentor_1_id': mentor_1.id,
        'mentor_2_id': mentor_2.id
    })
    
    assert response.status_code == 302 # redirect
    
    # 6. Verify assignments in DB
    # 1st half: students R001, R002
    assign_1 = StudentMentorAssignment.objects.get(mentor=mentor_1)
    assert set(assign_1.students.all()) == {students[0], students[1]}
    
    # 2nd half: students R003, R004
    assign_2 = StudentMentorAssignment.objects.get(mentor=mentor_2)
    assert set(assign_2.students.all()) == {students[2], students[3]}
    
    # 7. Verify double-assignment prevention constraint
    # Let's create a new batch/section
    section_b = Section.objects.create(name="B", department=dept)
    user_b = User.objects.create(email="student_b@cs.com", role="Student")
    profile_b = StudentProfile.objects.create(
        user=user_b,
        roll_no="R005",
        batch="2023-2027",
        department=dept,
        section=section_b
    )
    
    # Attempt to assign mentor_1 (who is already assigned to batch 2022-2026) to 2023-2027
    mentor_3 = User.objects.create(email="mentor3@cs.com", role="Mentor")
    mentor_3.departments.add(dept)
    
    response_double = client.post(url, {
        'action': 'assign_mentor_halves',
        'batch': '2023-2027',
        'section_id': section_b.id,
        'mentor_1_id': mentor_1.id, # Already assigned to 2022-2026!
        'mentor_2_id': mentor_3.id
    })
    
    # Should redirect, but session messages should show error
    assert response_double.status_code == 302
    # Verify assignment for mentor_1 did not change to include profile_b
    assert profile_b not in assign_1.students.all()
