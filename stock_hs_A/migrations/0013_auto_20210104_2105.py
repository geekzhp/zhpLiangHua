# Generated by Django 3.1.4 on 2021-01-04 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_hs_A', '0012_capitalchange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='comments',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
    ]
