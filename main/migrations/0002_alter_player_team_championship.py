# Generated by Django 4.2.1 on 2023-05-10 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='players', to='main.team'),
        ),
        migrations.CreateModel(
            name='ChampionShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('year', models.PositiveSmallIntegerField()),
                ('location', models.CharField(max_length=20)),
                ('teams', models.ManyToManyField(related_name='teams', to='main.team')),
            ],
        ),
    ]
