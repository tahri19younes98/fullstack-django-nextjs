# Generated by Django 5.2.3 on 2025-07-03 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qrmainpage', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='facebookUser',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='instagramUser',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='tiktokUser',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
