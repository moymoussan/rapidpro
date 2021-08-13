# Generated by Django 3.2.6 on 2021-08-13 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("channels", "0131_auto_20210813_1724"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channelconnection",
            name="status",
            field=models.CharField(
                choices=[
                    ("P", "Pending"),
                    ("W", "Wired"),
                    ("I", "In Progress"),
                    ("D", "Complete"),
                    ("E", "Error"),
                    ("F", "Failed"),
                ],
                max_length=1,
            ),
        ),
    ]
