# Generated by Django 2.0.4 on 2018-04-11 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=50)),
                ('expires_in', models.CharField(max_length=50)),
                ('refresh_token', models.CharField(max_length=50)),
                ('scope', models.CharField(max_length=50)),
                ('auth_id', models.CharField(max_length=50)),
                ('email_notifications', models.BooleanField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
