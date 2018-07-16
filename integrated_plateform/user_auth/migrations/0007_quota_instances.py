# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0006_auto_20180709_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='quota',
            name='instances',
            field=models.IntegerField(default=None),
        ),
    ]
