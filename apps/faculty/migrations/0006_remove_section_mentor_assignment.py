from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0005_student_mentor_assignment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SectionMentorAssignment',
        ),
    ]

