# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-22 01:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooring', '0042_auto_20180821_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='admissionsbooking',
            name='noOfConcessions',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
