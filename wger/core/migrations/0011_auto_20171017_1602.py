# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-10-17 13:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20171011_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='created_by',
            field=models.ForeignKey(help_text='Default User created by flag', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.UserProfile', verbose_name='Created by'),
        ),
    ]
