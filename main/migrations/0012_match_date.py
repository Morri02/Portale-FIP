# Generated by Django 4.2.1 on 2023-05-14 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_calendario_giornata_match_giornata'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
