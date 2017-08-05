# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-05 05:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('cid', models.IntegerField(default=0)),
                ('public', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=10, unique=True)),
                ('pwd', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100, unique=True)),
                ('token', models.CharField(max_length=100)),
            ],
        ),
    ]
