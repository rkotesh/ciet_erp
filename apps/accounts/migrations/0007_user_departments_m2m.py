from django.db import migrations, models


def forwards_copy_departments(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    Department = apps.get_model('academics', 'Department')

    def _get_dept(code):
        return Department.objects.filter(code__iexact=code).first() or Department.objects.filter(name__iexact=code).first()

    ai = _get_dept('AI')
    aiml = _get_dept('AIML')

    for user in User.objects.all():
        dept = getattr(user, 'department', None)
        if not dept:
            continue
        if user.role in ['Faculty', 'Mentor'] and (
            (dept.code and dept.code.upper() in ['AI', 'AIML']) or (dept.name and dept.name.upper() in ['AI', 'AIML'])
        ):
            depts = [d for d in [ai, aiml] if d] or [dept]
        else:
            depts = [dept]
        user.departments.set(depts)
        if user.role == 'HOD':
            dept.hod = user
            dept.save(update_fields=['hod', 'updated_at'])


def backwards_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_role_choices'),
        ('academics', '0004_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='departments',
            field=models.ManyToManyField(blank=True, related_name='staff', to='academics.department'),
        ),
        migrations.RunPython(forwards_copy_departments, backwards_noop),
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
    ]

