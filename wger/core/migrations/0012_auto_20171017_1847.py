# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-10-17 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20171017_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='created_by',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
