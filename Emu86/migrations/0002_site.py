# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-04 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Emu86', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('url', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('descr', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('header', models.CharField(default='', max_length=128)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
    ]
