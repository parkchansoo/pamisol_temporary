# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-09 00:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customprofile', '0002_auto_20180207_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]