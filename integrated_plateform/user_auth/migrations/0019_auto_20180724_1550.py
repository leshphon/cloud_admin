# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-24 07:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0018_auto_20180714_0606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='quota',
        ),
        migrations.RemoveField(
            model_name='user',
            name='usage',
        ),
        migrations.RemoveField(
            model_name='vdc',
            name='quota',
        ),
        migrations.RemoveField(
            model_name='vdc',
            name='usage',
        ),
        migrations.DeleteModel(
            name='Quota',
        ),
        migrations.DeleteModel(
            name='Usage',
        ),
    ]
