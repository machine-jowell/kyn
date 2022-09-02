# Generated by Django 4.1 on 2022-08-25 08:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_alter_userevent_created_by"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userevent", old_name="time", new_name="end_time",
        ),
        migrations.AddField(
            model_name="userevent",
            name="start_time",
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
