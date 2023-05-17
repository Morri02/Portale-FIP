# Generated by Django 4.2.1 on 2023-05-10 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=20)),
                ('main_sponsor', models.CharField(default=None, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('birth_date', models.DateTimeField()),
                ('number', models.IntegerField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.team')),
            ],
        ),
    ]
