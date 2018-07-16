# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-07-14 06:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0017_merge_20180714_0605'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='quota',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_auth.Quota'),
        ),
        migrations.AddField(
            model_name='user',
            name='usage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_auth.Usage'),
        ),
        migrations.AlterField(
            model_name='quota',
            name='cpu',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='quota',
            name='ram',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='recent_use_VDC',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='vdc',
            name='backend_info',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='vdc',
            name='description',
            field=models.TextField(default=None),
        ),
    ]
