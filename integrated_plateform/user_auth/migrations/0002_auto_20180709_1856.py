# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Role_VDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.ForeignKey(to='user_auth.Role')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user_role',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='user_role',
            name='role',
        ),
        migrations.RemoveField(
            model_name='user_role',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='user_vdc',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='user_vdc',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user_vdc',
            name='vdc',
        ),
        migrations.AddField(
            model_name='user',
            name='recent_use_VDC',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='vdc',
            name='backend_info',
            field=models.TextField(default=None),
        ),
        migrations.DeleteModel(
            name='User_Role',
        ),
        migrations.DeleteModel(
            name='User_VDC',
        ),
        migrations.AddField(
            model_name='user_role_vdc',
            name='user',
            field=models.ForeignKey(to='user_auth.User'),
        ),
        migrations.AddField(
            model_name='user_role_vdc',
            name='vdc',
            field=models.ForeignKey(to='user_auth.VDC'),
        ),
        migrations.AlterUniqueTogether(
            name='user_role_vdc',
            unique_together=set([('user', 'vdc', 'role')]),
        ),
    ]
