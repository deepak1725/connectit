# Generated by Django 2.0.4 on 2018-04-18 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20180418_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialauth',
            name='followers',
            field=models.TextField(default=[]),
        ),
    ]