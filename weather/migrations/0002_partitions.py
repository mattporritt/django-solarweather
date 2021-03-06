# Generated by Django 3.2.4 on 2022-02-06 06:35

from django.db import migrations, models
from psqlextra.backend.migrations.operations import PostgresAddRangePartition


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2021_08",
            from_values="1628702487",
            to_values="1630418353",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2021_09",
            from_values="1630418423",
            to_values="1633010364",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2021_10",
            from_values="1633010432",
            to_values="1635685171",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2021_11",
            from_values="1635685243",
            to_values="1638277180",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2021_12",
            from_values="1638277251",
            to_values="1640955588",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2022_01",
            from_values="1640955658",
            to_values="1643633997",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2022_02",
            from_values="1643634000",
            to_values="1645966800",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2022_03",
            from_values="1646053200",
            to_values="1648731599",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2022_04",
            from_values="1648775111",
            to_values="1651327160",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2022_05",
            from_values="1651327220",
            to_values="1654005596",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2022_06",
            from_values="1654005667",
            to_values="1656597546",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2022_07",
            from_values="1656597606",
            to_values="1659275999",
        ),
        PostgresAddRangePartition(
            model_name="WeatherData",
            name="2022_08",
            from_values="1659276000",
            to_values="1661954399",
        ),
    ]
