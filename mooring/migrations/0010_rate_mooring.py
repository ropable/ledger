# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-21 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooring', '0009_auto_20180619_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='mooring',
            field=models.DecimalField(decimal_places=2, default='10.00', max_digits=8),
        ),
    ]
