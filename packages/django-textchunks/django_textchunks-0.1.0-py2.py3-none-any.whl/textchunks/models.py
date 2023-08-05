# -*- coding: utf-8 -*-

from django.db import models
from django.core.cache import cache
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _

CACHE_PREFIX = 'textchunks_'


class TextChunk(models.Model):
    """
    A TextChunk is a piece of content associated with a unique key that can be
    inserted into any template with the use of a special template tag
    """
    key = models.CharField(
        _('key'), max_length=255, unique=True,
        help_text=_('A unique name for this chunk of content'))
    content = models.TextField(_('content'), blank=True)

    content_type = 'text'

    class Meta:
        verbose_name = _('Text Chunk')
        verbose_name_plural = _('Text Chunks')
        ordering = ('key', )

    def __unicode__(self):
        return self.key

    def save(self, *args, **kwargs):
        cache_key = CACHE_PREFIX + self.content_type + get_language() + self.key
        cache.delete(cache_key)  # cache invalidation on save
        super(TextChunk, self).save(*args, **kwargs)
