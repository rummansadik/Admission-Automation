# Generated by Django 3.0.5 on 2022-04-10 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0003_shortquestion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortquestion',
            name='answer',
        ),
    ]