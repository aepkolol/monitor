# Generated by Django 3.2.15 on 2023-04-03 11:43

from django.db import migrations, models
import django.db.models.deletion
import sdr.models


def update_audio_class(apps, schema_editor):
    default_audio_class_id = sdr.models.AudioClass.objects.get_or_create(name="Default", subname="Default")[0].id
    sdr.models.Transmission.objects.update(audio_class_id=default_audio_class_id)


class Migration(migrations.Migration):

    dependencies = [
        ("sdr", "0012_auto_20230216_1625"),
    ]

    operations = [
        migrations.CreateModel(
            name="AudioClass",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                ("subname", models.CharField(max_length=255, unique=True, verbose_name="Subname")),
            ],
            options={
                "unique_together": {("name", "subname")},
            },
        ),
        migrations.AddField(
            model_name="transmission",
            name="audio_class",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="sdr.audioclass"),
        ),
        migrations.RunPython(update_audio_class),
        migrations.AlterField(
            model_name="transmission",
            name="audio_class",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="sdr.audioclass"),
        ),
    ]
