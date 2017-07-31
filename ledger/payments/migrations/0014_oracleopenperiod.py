# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-19 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0013_trackrefund_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='OracleOpenPeriod',
            fields=[
                ('period_name', models.CharField(max_length=240, primary_key=True, serialize=False)),
                ('closing_status', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'payments_open_periods',
                'managed': False,
            },
        ),
    ]