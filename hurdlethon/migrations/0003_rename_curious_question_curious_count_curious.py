# Generated by Django 5.1.2 on 2024-11-26 05:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hurdlethon', '0002_answer_is_checked_alter_user_interests_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='curious',
            new_name='curious_count',
        ),
        migrations.CreateModel(
            name='Curious',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hurdlethon.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'question')},
            },
        ),
    ]
