# Generated by Django 4.1.5 on 2023-01-06 18:22

import datetime
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0012_merge_20230105_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='official_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2023, 1, 6), 'valid values are not in the past')]),
        ),
    ]
