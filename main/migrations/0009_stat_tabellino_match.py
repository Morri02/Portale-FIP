# Generated by Django 4.2.1 on 2023-05-14 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_championship_teams_alter_player_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveSmallIntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='main.player')),
            ],
        ),
        migrations.CreateModel(
            name='Tabellino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statA1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA1', to='main.stat')),
                ('statA10', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA10', to='main.stat')),
                ('statA11', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA11', to='main.stat')),
                ('statA12', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA12', to='main.stat')),
                ('statA2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA2', to='main.stat')),
                ('statA3', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA3', to='main.stat')),
                ('statA4', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA4', to='main.stat')),
                ('statA5', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA5', to='main.stat')),
                ('statA6', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA6', to='main.stat')),
                ('statA7', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA7', to='main.stat')),
                ('statA8', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA8', to='main.stat')),
                ('statA9', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statA9', to='main.stat')),
                ('statB1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB1', to='main.stat')),
                ('statB10', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB10', to='main.stat')),
                ('statB11', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB11', to='main.stat')),
                ('statB12', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB12', to='main.stat')),
                ('statB2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB2', to='main.stat')),
                ('statB3', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB3', to='main.stat')),
                ('statB4', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB4', to='main.stat')),
                ('statB5', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB5', to='main.stat')),
                ('statB6', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB6', to='main.stat')),
                ('statB7', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB7', to='main.stat')),
                ('statB8', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB8', to='main.stat')),
                ('statB9', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statB9', to='main.stat')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pointsA', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('pointsB', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('location', models.CharField(max_length=50)),
                ('championship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.championship')),
                ('tabellino', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='tabellino', to='main.tabellino')),
                ('teamA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamA', to='main.team')),
                ('teamB', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamB', to='main.team')),
            ],
        ),
    ]