# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20170405_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='keyword',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
