# Generated by Django 3.2.15 on 2023-01-02 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdr', '0008_transmission_data_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recordingsession',
            name='recordings',
        ),
        migrations.DeleteModel(
            name='Recording',
        ),
        migrations.DeleteModel(
            name='RecordingSession',
        ),
    ]
