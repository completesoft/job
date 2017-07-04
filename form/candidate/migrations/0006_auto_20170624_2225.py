# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-24 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0005_auto_20170618_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='passp_issue',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Кем выдан'),
        ),
        migrations.AlterField(
            model_name='person',
            name='quant_children',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)], default='0', verbose_name='Количество детей'),
        ),
    ]