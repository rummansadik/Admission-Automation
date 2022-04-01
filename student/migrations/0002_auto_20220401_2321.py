# Generated by Django 3.0.5 on 2022-04-01 17:21

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=100, size=[250, 500], upload_to='profile_pic/Student'),
        ),
    ]