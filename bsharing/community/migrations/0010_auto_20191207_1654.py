# Generated by Django 2.2.5 on 2019-12-07 16:54

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0009_auto_20191207_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post_type_header',
            name='fields',
        ),
        migrations.AddField(
            model_name='post_type_header',
            name='fields',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=''),
        ),
    ]