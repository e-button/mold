# Generated by Django 3.2.5 on 2022-08-19 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_molddata_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='molddata',
            name='end_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
