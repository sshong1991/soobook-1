# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0009_book_isbn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='isbn',
        ),
        migrations.AlterField(
            model_name='book',
            name='cover_thumbnail',
            field=models.TextField(),
        ),
    ]
