# Generated by Django 3.1.4 on 2020-12-29 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock_hs_A', '0005_auto_20201229_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industries',
            name='industryType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stock_hs_A.industrytype'),
        ),
        migrations.AlterField(
            model_name='industries',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
