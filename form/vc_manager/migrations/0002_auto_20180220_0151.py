# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-19 23:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vc_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vcstatusname',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Новое'), (1, 'Просмотренное'), (2, 'Собеседование'), (3, 'Принят'), (4, 'НЕ принят'), (5, 'Архив')], unique=True, verbose_name='Статус резюме'),
        ),
    ]
