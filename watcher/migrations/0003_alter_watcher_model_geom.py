# Generated by Django 5.0.4 on 2024-04-22 19:51

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("watcher", "0002_watcher_model_delete_watcher_mod"),
    ]

    operations = [
        migrations.AlterField(
            model_name="watcher_model",
            name="geom",
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]
