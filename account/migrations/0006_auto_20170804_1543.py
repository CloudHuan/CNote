# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-04 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20170804_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pwd',
            field=models.CharField(max_length=20),
        ),
    ]
