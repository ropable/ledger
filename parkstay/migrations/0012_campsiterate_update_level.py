# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-21 04:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkstay', '0011_auto_20161116_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='campsiterate',
            name='update_level',
            field=models.SmallIntegerField(choices=[(0, 'Campground level'), (1, 'Campsite Class level'), (2, 'Campsite level')], default=0),
        ),
    ]
