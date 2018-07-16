# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_auto_20180709_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_role_vdc',
            name='vdc',
            field=models.ForeignKey(to='user_auth.VDC', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='user_role_vdc',
            unique_together=set([('user', 'role', 'vdc')]),
        ),
    ]
