# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-08 11:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_files', '0003_auto_20190705_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafile',
            name='linked_models',
        ),
    ]