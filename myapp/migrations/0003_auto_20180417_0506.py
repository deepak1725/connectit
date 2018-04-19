# Generated by Django 2.0.4 on 2018-04-17 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20180417_0459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailnotifications',
            name='social_auth',
        ),
        migrations.AddField(
            model_name='emailnotifications',
            name='social_auth',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.SocialAuth'),
            preserve_default=False,
        ),
    ]