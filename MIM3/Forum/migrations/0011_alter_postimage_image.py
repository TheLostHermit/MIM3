# Generated by Django 4.1.5 on 2023-01-05 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum', '0010_alter_post_is_project_alter_postimage_is_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.ImageField(upload_to='post_images'),
        ),
    ]
