# Generated by Django 4.1.6 on 2023-03-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homePage', '0006_auto_20230131_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='demo',
            field=models.URLField(default='https://github.com/topics/chatbot-demo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='repo',
            field=models.URLField(default='https://github.com/topics/chatbot-demo'),
            preserve_default=False,
        ),
    ]