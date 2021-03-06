# Generated by Django 3.1.4 on 2020-12-28 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_hs_A', '0003_auto_20201228_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industries',
            name='industryType',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='stock_hs_A.industrytype'),
        ),
        migrations.AlterField(
            model_name='industries',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='industries',
            name='start_date',
            field=models.DateField(default=None),
        ),
    ]
