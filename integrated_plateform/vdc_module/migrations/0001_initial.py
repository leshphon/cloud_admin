# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-26 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('identification', models.CharField(max_length=128)),
                ('created_by', models.IntegerField(default=None)),
                ('created_in', models.IntegerField(default=None)),
                ('flavor_id', models.CharField(max_length=128)),
                ('attach_volume_id', models.CharField(max_length=128, null=True)),
                ('image_id', models.CharField(max_length=128, null=True)),
                ('host_id', models.CharField(max_length=128)),
                ('status', models.CharField(max_length=32)),
                ('task_state', models.CharField(max_length=32, null=True)),
                ('vm_state', models.CharField(max_length=32)),
                ('created_time', models.CharField(max_length=128)),
                ('updated_time', models.CharField(max_length=128)),
                ('key_name', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServerAddresses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.CharField(max_length=128)),
                ('net_name', models.CharField(max_length=128)),
                ('net_type', models.CharField(max_length=128)),
                ('net_addr', models.CharField(max_length=128)),
                ('net_mac_addr', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ServerSecurityGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.CharField(max_length=128)),
                ('security_group_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ServerVolume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_id', models.CharField(max_length=128)),
                ('volume_id', models.CharField(max_length=128)),
            ],
        ),
    ]
