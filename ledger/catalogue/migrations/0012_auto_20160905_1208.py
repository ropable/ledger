# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 04:08
from __future__ import unicode_literals

from django.db import migrations
import oscar.models.fields.slugfield


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0011_product_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=oscar.models.fields.slugfield.SlugField(max_length=255, verbose_name='Slug'),
        ),
    ]
