# Generated by Django 4.0.8 on 2023-01-09 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("flows", "0311_alter_flowrunstatuscount_index_together_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FlowRunCount",
        ),
    ]