# Generated by Django 4.1.5 on 2023-01-11 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0015_event_passed_alter_event_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='passed',
        ),
    ]
