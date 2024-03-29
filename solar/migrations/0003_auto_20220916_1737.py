# Generated by Django 3.2.4 on 2022-09-16 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solar', '0002_partitions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='solardata',
            options={},
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['grid_power_usage_real', 'time_year'], name='solar_solar_grid_po_882897_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['grid_power_factor', 'time_year'], name='solar_solar_grid_po_bc17b7_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['grid_power_apparent', 'time_year'], name='solar_solar_grid_po_2deb66_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['grid_power_reactive', 'time_year'], name='solar_solar_grid_po_37e35c_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['grid_ac_voltage', 'time_year'], name='solar_solar_grid_ac_9df396_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['grid_ac_current', 'time_year'], name='solar_solar_grid_ac_3cc1a5_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['inverter_ac_frequency', 'time_year'], name='solar_solar_inverte_0ef5ad_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['inverter_ac_current', 'time_year'], name='solar_solar_inverte_3defda_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['inverter_ac_voltage', 'time_year'], name='solar_solar_inverte_f8b004_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['inverter_dc_current', 'time_year'], name='solar_solar_inverte_d535c0_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['inverter_dc_voltage', 'time_year'], name='solar_solar_inverte_4eb991_idx'),
        ),
        migrations.AddIndex(
            model_name='solardata',
            index=models.Index(fields=['power_consumption', 'time_year'], name='solar_solar_power_c_464782_idx'),
        ),
    ]
