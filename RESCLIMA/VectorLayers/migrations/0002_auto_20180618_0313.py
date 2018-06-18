# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('VectorLayers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identity_card', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=10)),
                ('institution', models.CharField(max_length=100)),
                ('usuario', models.OneToOneField(related_name='researcher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Researcher',
                'verbose_name_plural': 'Researchers',
            },
        ),
        migrations.AlterModelOptions(
            name='style',
            options={'ordering': ['id']},
        ),
    ]
