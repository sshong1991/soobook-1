# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 01:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20170404_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
