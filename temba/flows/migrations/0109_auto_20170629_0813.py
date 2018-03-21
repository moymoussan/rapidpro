# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 08:13
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('flows', '0108_populate_flowrun_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowrun',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]