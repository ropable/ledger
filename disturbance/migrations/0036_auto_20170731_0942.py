# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-31 01:42
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('disturbance', '0035_auto_20170731_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2017, 7, 31, 1, 42, 33, 629277, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
