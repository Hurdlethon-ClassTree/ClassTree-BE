# Generated by Django 5.1.3 on 2024-11-26 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hurdlethon', '0006_user_expiration_time_user_verification_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_email', models.EmailField(max_length=254, unique=True)),
                ('verification_code', models.CharField(max_length=6)),
                ('code_expiration', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='expiration_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='verification_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='verified',
        ),
    ]
