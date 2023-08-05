# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-25 23:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hordak', '0003_check_zero_amount_20160907_0921'),
        ('transactions', '0006_auto_20160925_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionimport',
            name='hordak_import',
            field=models.ForeignKey(default=27, on_delete=django.db.models.deletion.CASCADE, to='hordak.StatementImport'),
            preserve_default=False,
        ),
    ]
