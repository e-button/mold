# Generated by Django 3.2.5 on 2022-08-19 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_molddata_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='molddata',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
