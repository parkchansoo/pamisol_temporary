# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-08 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customprofile', '0002_auto_20180207_1927'),
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='like',
            field=models.ManyToManyField(related_name='menu_like', to='customprofile.UserProfile'),
        ),
    ]
