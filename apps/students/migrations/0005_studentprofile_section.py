from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0004_section'),
        ('students', '0004_project_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='academics.section'),
        ),
    ]

