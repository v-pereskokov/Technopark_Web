# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-22 21:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0003_auto_20161122_2019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='like',
            options={'verbose_name': '\u041b\u0430\u0439\u043a\u0438', 'verbose_name_plural': '\u041b\u0430\u0439\u043a\u0438'},
        ),
        migrations.AddField(
            model_name='like',
            name='author',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='ask.Profile'),
        ),
        migrations.AddField(
            model_name='like',
            name='question',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='ask.Question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='question',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
        ),
    ]
