# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 10:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='title',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='contenttree',
            name='content',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='content_tree', to='content.Content'),
        ),
    ]
