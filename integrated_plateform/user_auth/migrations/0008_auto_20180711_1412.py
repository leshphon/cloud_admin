# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0007_quota_instances'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quota',
            old_name='disk',
            new_name='volume',
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
