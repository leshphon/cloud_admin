# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_auto_20180709_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_role_vdc',
            name='role',
            field=models.ForeignKey(to='user_auth.Role', null=True),
        ),
        migrations.AlterField(
            model_name='user_role_vdc',
            name='vdc',
            field=models.ForeignKey(to='user_auth.VDC', null=True),
        ),
    ]
