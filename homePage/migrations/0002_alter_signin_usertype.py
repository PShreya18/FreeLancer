# Generated by Django 3.2.13 on 2022-10-28 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signin',
            name='userType',
            field=models.BooleanField(default=1),
        ),
    ]
