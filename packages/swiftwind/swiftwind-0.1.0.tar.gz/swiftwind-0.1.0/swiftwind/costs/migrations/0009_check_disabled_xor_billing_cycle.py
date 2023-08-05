# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-09 12:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0008_check_cannot_create_recurred_cost_for_disabled_cost'),
    ]

    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE costs_recurringcost ADD CONSTRAINT check_disabled_xor_initial_billing_cycle
            CHECK (
                (disabled AND initial_billing_cycle_id IS NULL)
                OR
                (NOT disabled AND initial_billing_cycle_id IS NOT NULL)
            )
            """,
            "ALTER TABLE costs_recurringcost DROP CONSTRAINT check_disabled_xor_initial_billing_cycle"
        )
    ]
