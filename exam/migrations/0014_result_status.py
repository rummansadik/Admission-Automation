# Generated by Django 3.0.5 on 2022-04-13 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0013_answersheet_unfocus'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='status',
            field=models.CharField(choices=[('Unknown', 'Unknown'), ('Attended', 'Attended'), ('Expelled', 'Expelled')], default='Unknown', max_length=20),
        ),
    ]
