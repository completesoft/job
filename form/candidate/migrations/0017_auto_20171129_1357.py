# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-29 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0016_auto_20171129_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='mail_to_group',
        ),
        migrations.AlterField(
            model_name='mailbacksettings',
            name='default',
            field=models.BooleanField(default=False, verbose_name='Использовать по умоланию'),
        ),
    ]