# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-26 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disturbance', '0021_auto_20180426_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposaltype',
            name='name',
            field=models.CharField(choices=[('Disturbance', 'Disturbance'), ('Apiary', 'Apiary')], max_length=24, verbose_name='Application name (eg. Disturbance, Apiary)'),
        ),
    ]
