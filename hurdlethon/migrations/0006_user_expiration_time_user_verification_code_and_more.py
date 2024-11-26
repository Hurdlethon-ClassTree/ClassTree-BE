# Generated by Django 5.1.3 on 2024-11-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hurdlethon', '0005_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expiration_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='verification_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
