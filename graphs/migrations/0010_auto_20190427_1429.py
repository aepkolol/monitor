# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-27 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("graphs", "0009_sensortype_visible"),
    ]

    operations = [
        migrations.AlterField(model_name="measurement", name="value", field=models.DecimalField(decimal_places=6, max_digits=20, verbose_name="Wartość"),),
    ]
