# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-12 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkstay', '0030_feature_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campsite',
            name='cs_dimensions',
        ),
        migrations.RemoveField(
            model_name='campsite',
            name='cs_number_vehicles',
        ),
        migrations.RemoveField(
            model_name='campsite',
            name='cs_parking_spaces',
        ),
        migrations.RemoveField(
            model_name='campsite',
            name='cs_tents',
        ),
        migrations.RemoveField(
            model_name='campsiteclass',
            name='dimensions',
        ),
        migrations.RemoveField(
            model_name='campsiteclass',
            name='number_vehicles',
        ),
        migrations.RemoveField(
            model_name='campsiteclass',
            name='parking_spaces',
        ),
        migrations.RemoveField(
            model_name='campsiteclass',
            name='tents',
        ),
        migrations.AddField(
            model_name='campsite',
            name='cs_campervan',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campsite',
            name='cs_caravan',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campsite',
            name='cs_description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='campsite',
            name='cs_tent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campsiteclass',
            name='campervan',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campsiteclass',
            name='caravan',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='campsiteclass',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='campsiteclass',
            name='tent',
            field=models.BooleanField(default=False),
        ),
    ]