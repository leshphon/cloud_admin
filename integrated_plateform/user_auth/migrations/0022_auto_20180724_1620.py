# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-24 08:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0021_auto_20180724_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='used_cpu',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='user',
            name='used_instances',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='user',
            name='used_ram',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='user',
            name='used_volume',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='vdc',
            name='used_cpu',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='vdc',
            name='used_instances',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='vdc',
            name='used_ram',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='vdc',
            name='used_volume',
            field=models.IntegerField(default=None),
        ),
    ]
