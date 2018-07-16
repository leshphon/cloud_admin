# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_auto_20180709_1947'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user_role_vdc',
            unique_together=set([]),
        ),
    ]
