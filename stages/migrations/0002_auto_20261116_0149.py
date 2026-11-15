from django.db import migrations


def forwards(apps, schema_editor):
    Stage = apps.get_model('stages', 'Stage')
    Stage.objects.filter(status='planned').update(status='planned')
    Stage.objects.filter(status='in_progress').update(status='in_progress')
    Stage.objects.filter(status='done').update(status='done')


class Migration(migrations.Migration):

    dependencies = [
        ('stages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]