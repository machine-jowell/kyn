# Generated by Django 4.1 on 2022-08-25 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_alter_userevent_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userevent",
            name="neighbourhood",
            field=models.CharField(
                choices=[
                    ("Choa Chu Kang", "Choa Chu Kang"),
                    ("Bukit Gombak", "Bukit Gombak"),
                    ("Bukit Batok", "Bukit Batok"),
                    ("Jurong East", "Jurong East"),
                    ("Clementi", "Clementi"),
                    ("Dover", "Dover"),
                    ("Buona Vista", "Buona Vista"),
                    ("Commonwealth", "Commonwealth"),
                    ("Queenstown", "Queenstown"),
                    ("Redhill", "Redhill"),
                    ("Tiong Bahru", "Tiong Bahru"),
                    ("Outram Park", "Outram Park"),
                ],
                max_length=100,
            ),
        ),
    ]