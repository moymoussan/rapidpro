# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-04 21:10
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('orgs', '0036_ensure_anon_user_exists'),
        ('contacts', '0065_backfill_urn_identity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacturn',
            name='identity',
            field=models.CharField(help_text='The Universal Resource Name as a string, excluding display if present. ex: tel:+250788383383', max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='contacturn',
            unique_together=set([('identity', 'org'), ('urn', 'org')]),
        ),
        migrations.RunSQL("CREATE INDEX CONCURRENTLY contacts_contacturn_org_scheme_display "
                          "ON contacts_contacturn (org_id, scheme, display)"
                          "WHERE display IS NOT NULL"),
    ]