# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TextChunk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=255, verbose_name='key', unique=True, help_text='A unique name for this chunk of content')),
                ('content', models.TextField(verbose_name='content', blank=True)),
            ],
            options={
                'ordering': ('key',),
                'verbose_name': 'Text TextChunk',
                'verbose_name_plural': 'Text Chunks',
                'abstract': False,
            },
        ),
    ]
