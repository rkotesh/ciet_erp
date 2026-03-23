from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0003_subject_faculty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=10)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='academics.department')),
            ],
            options={
                'ordering': ['department__code', 'name'],
                'unique_together': {('department', 'name')},
            },
        ),
    ]

