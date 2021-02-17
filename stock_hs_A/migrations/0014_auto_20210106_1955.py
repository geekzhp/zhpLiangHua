# Generated by Django 3.1.4 on 2021-01-06 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_hs_A', '0013_auto_20210104_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='capitalchange',
            name='code',
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='control_shareholder_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='core_employee_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='individual_fund_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='legal_of_other_instate_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='legal_of_outstate_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='natural_of_other_instate_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='natural_of_outstate_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='other_instate_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='other_legal_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='other_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='outstate_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_b',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_b_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_convert',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_fund',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_h',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_h_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_inside',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_instate_legal',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_legal_issue',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_management',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_management_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_nation',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_nation_legal',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_nation_legal_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_nation_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_natural',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_non_trade',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_normal_legal',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_other_limited',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_other_nontrade',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_other_trade',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_outstate_legal',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_perferred',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_raised',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_rmb',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_start',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_strategic_investor',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_total',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='capitalchange',
            name='share_trade_total',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=20, null=True),
        ),
    ]
