# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-29 08:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0015_auto_20171122_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_id', models.CharField(max_length=20, verbose_name='Идентификатор')),
                ('describe', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'АРМ анкетирования',
                'verbose_name_plural': 'АРМ анкетирования',
            },
        ),
        migrations.RemoveField(
            model_name='mailtogroup',
            name='mail_back_settings',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mail_group',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='mailtoaddress',
            options={'verbose_name': 'Адресат', 'verbose_name_plural': 'Адресаты'},
        ),
        migrations.RemoveField(
            model_name='mailtoaddress',
            name='mail_to_group',
        ),
        migrations.AddField(
            model_name='mailbacksettings',
            name='default',
            field=models.BooleanField(default=False, verbose_name='Настройка по умоланию'),
        ),
        migrations.DeleteModel(
            name='MailToGroup',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.AddField(
            model_name='location',
            name='mail_to',
            field=models.ManyToManyField(related_name='mail_to', to='candidate.MailToAddress', verbose_name='Получатели почты'),
        ),
    ]