# Generated by Django 4.1.5 on 2023-01-05 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0008_alter_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='Forum.profile'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='Forum.event'),
        ),
    ]
