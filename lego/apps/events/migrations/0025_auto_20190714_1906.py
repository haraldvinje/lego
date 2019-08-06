# Generated by Django 2.1.7 on 2019-07-14 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0024_event_youtube_url")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="event_type",
            field=models.CharField(
                choices=[
                    ("company_presentation", "company_presentation"),
                    ("lunch_presentation", "lunch_presentation"),
                    ("alternative_presentation", "alternative_presentation"),
                    ("course", "course"),
                    ("kid_event", "kid_event"),
                    ("party", "party"),
                    ("social", "social"),
                    ("other", "other"),
                    ("event", "event"),
                ],
                max_length=50,
            ),
        )
    ]