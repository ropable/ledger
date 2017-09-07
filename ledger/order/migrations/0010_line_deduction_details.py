# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-30 04:30
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20170419_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='deduction_details',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={b'bpay': {}, b'card': {}, b'cash': {}}),
        ),
    ]