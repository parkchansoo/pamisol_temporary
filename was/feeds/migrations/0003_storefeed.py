# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-07 18:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_remove_store_profile'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('feeds', '0002_userfeed_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storefeed', to='stores.Store')),
            ],
        ),
    ]
