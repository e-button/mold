# Generated by Django 3.2.5 on 2022-08-22 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_molddata_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='molddata',
            name='times',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='molddata',
            name='start_time',
            field=models.DateTimeField(default='2022-08-22 13:39:12'),
        ),
    ]
