# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from fluent_contents.extensions import ContentPlugin, plugin_pool

from socialaggregator.models import Ressource

from .models import SocialFeedItem


@plugin_pool.register
class SocialFeedPlugin(ContentPlugin):
    model = SocialFeedItem
    category = _('Media')
    render_template = "fluentcms_socialfeed/socialfeed.html"

    def get_context(self, request, instance, **kwargs):
        context = super(SocialFeedPlugin, self).get_context(request, instance, **kwargs)
        context.update({
            'feed': instance.feed,
            'ressources': Ressource.activated.filter(
                feeds=instance.feed).order_by('priority', '-ressource_date'),
        })
        return context
