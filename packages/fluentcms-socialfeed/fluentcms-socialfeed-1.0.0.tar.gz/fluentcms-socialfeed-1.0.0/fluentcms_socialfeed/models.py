# -*- coding: utf-8 -*-

from future.utils import python_2_unicode_compatible

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fluent_contents.models import ContentItem


@python_2_unicode_compatible
class SocialFeedItem(ContentItem):

    feed = models.ForeignKey('socialaggregator.Feed', related_name='plugins')

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')

    def __str__(self):
        return self.feed.name
