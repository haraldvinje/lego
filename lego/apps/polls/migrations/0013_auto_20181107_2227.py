# Generated by Django 2.1.2 on 2018-11-07 22:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20181107_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='valid_until',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 6, 22, 27, 17, 529480, tzinfo=utc)),
        ),
    ]
