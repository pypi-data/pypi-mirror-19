# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
        ('socialaggregator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialFeedItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('feed', models.ForeignKey(related_name='plugins', to='socialaggregator.Feed')),
            ],
            options={
                'db_table': 'contentitem_fluentcms_socialfeed_socialfeeditem',
                'verbose_name': 'Feed',
                'verbose_name_plural': 'Feeds',
            },
            bases=('fluent_contents.contentitem',),
        ),
    ]
