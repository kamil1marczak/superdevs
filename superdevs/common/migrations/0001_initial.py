# Generated by Django 4.2 on 2023-04-19 15:31

import uuid

import django.utils.timezone
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RandomModel",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
            ],
        ),
        migrations.AddConstraint(
            model_name="randommodel",
            constraint=models.CheckConstraint(
                check=models.Q(("start_date__lt", models.F("end_date"))), name="start_date_before_end_date"
            ),
        ),
    ]
