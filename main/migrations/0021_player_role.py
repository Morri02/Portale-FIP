# Generated by Django 4.2.1 on 2023-05-20 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_remove_calendario_classifica'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='role',
            field=models.CharField(default='Guardia', max_length=15),
        ),
    ]
