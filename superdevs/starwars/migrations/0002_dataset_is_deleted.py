# Generated by Django 4.2 on 2023-04-19 20:09

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("starwars", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]
