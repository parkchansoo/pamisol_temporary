# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-09 00:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_auto_20180208_2151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='like',
            new_name='like_user',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='like',
            new_name='like_user',
        ),
    ]
