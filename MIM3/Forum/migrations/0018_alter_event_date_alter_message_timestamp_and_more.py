# Generated by Django 4.1.5 on 2023-01-13 18:10

import datetime
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0017_message_event_alter_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2023, 1, 13), 'valid values are not in the past')]),
        ),
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]