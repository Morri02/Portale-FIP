# Generated by Django 4.2.1 on 2023-05-14 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_stat_tabellino_match'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='tabellino',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tabellino', to='main.tabellino'),
        ),
    ]
