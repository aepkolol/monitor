# Generated by Django 3.1.3 on 2022-07-26 07:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0014_auto_20220721_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='last_measurement_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data ostatniego pomiaru'),
        ),
    ]
