# Generated by Django 3.0.5 on 2022-04-11 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_answersheet_mcqmarks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answersheet',
            old_name='exam',
            new_name='course',
        ),
    ]
