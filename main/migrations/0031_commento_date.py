# Generated by Django 4.2.1 on 2023-05-24 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_commento_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='commento',
            name='date',
            field=models.DateField(null=True),
        ),
    ]