# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-25 08:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0012_auto_20170725_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailtoaddress',
            name='mail_to_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate.MailToGroup', verbose_name='Группа получателей'),
        ),
    ]