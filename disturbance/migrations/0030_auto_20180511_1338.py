# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-11 05:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disturbance', '0029_proposal_application_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='proposaltype',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='proposaltype',
            name='name',
        ),
    ]
