# Generated by Django 4.2.1 on 2023-05-10 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_player_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to='player_images'),
        ),
    ]
