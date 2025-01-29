# Generated by Django 5.1.3 on 2025-01-28 12:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrv', '0010_alter_measures_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='measures',
            name='android_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='measures',
            name='bpm',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='breathingrate',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='hf',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='hf_nu',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='hf_perc',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='hr_mad',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='ibi',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='lf',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='lf_hf',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='lf_nu',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='lf_perc',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='p_total',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='pnn20',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='pnn50',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='rmssd',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='s',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='sd1',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='sd1_sd2',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='sd2',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='sdnn',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='sdsd',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='timeStamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='measures',
            name='vlf',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='measures',
            name='vlf_perc',
            field=models.FloatField(default=-1),
        ),
    ]
