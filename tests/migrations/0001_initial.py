# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-01 21:58
from __future__ import unicode_literals

from django.db import migrations, models

import regexfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', regexfield.fields.RegexField(verbose_name='url path')),
            ],
        ),
    ]