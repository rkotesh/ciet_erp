from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0004_section_mentor_assignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentMentorAssignment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('academic_year', models.CharField(max_length=20)),
                ('assigned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_mentor_assignments_made', to='accounts.user')),
                ('mentor', models.ForeignKey(limit_choices_to={'role': 'Mentor'}, on_delete=django.db.models.deletion.CASCADE, related_name='student_mentor_assignments', to='accounts.user')),
            ],
        ),
        migrations.AddField(
            model_name='studentmentorassignment',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='direct_mentor_assignments', to='students.studentprofile'),
        ),
    ]
