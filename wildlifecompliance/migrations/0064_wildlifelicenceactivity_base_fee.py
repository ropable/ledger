# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-07-12 07:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0063_application_application_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='wildlifelicenceactivity',
            name='base_fee',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=8),
        ),
    ]
