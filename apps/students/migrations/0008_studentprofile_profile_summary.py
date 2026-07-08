from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_certification_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='profile_summary',
            field=models.TextField(blank=True, default=''),
        ),
    ]
