# Generated by Django 3.2.5 on 2022-08-30 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20220830_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='molddata',
            name='start_time',
            field=models.DateTimeField(default='2022-08-30 13:25:02'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='create_time',
            field=models.DateTimeField(default='2022-08-30 13:25:02'),
        ),
    ]
