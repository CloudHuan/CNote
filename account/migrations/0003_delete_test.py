# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-04 07:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_test'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
    ]