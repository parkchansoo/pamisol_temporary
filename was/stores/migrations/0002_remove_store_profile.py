# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-07 11:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='profile',
        ),
    ]