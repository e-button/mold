# Generated by Django 3.2.5 on 2022-08-19 07:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_molddata'),
    ]

    operations = [
        migrations.AddField(
            model_name='molddata',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='molddata',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]