# Generated by Django 3.2.4 on 2021-08-03 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_auto_20210710_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatherdata',
            name='indoor_dew_temp',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weatherdata',
            name='indoor_feels_temp',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weatherdata',
            name='outdoor_dew_temp',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weatherdata',
            name='outdoor_feels_temp',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
