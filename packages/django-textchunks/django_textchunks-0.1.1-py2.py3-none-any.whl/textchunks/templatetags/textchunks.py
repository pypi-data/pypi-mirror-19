# -*- coding: utf-8 -*-

import logging

from django import template
from django.core.cache import cache
from django.template import Template
from django.template.loader import get_template
from django.utils.translation import get_language
from django.utils.html import escape
from django.apps import apps


CACHE_PREFIX = 'textchunks_'

Chunk = apps.get_model('textchunks', 'textchunk')

register = template.Library()
logger = logging.getLogger(__name__)


class ChunkNode(template.Node):
    def __init__(self, key, is_variable, cache_time=0, with_template=True,
                 name=None, tpl_is_variable=False,
                 content_type='text'):

        self.template_name = name

        if self.template_name is None:
            self.template_name = 'textchunks/plain.html'
        else:
            if tpl_is_variable:
                self.template_name = template.Variable(self.template_name)
            else:
                self.template_name = name

        self.key = key
        self.is_variable = is_variable
        self.cache_time = cache_time
        self.with_template = with_template
        self.content_type = content_type

    def render(self, context):
        if self.is_variable:
            real_key = template.Variable(self.key).resolve(context)
        else:
            real_key = self.key

        if isinstance(self.template_name, template.Variable):
            real_tpl = self.template_name.resolve(context)
        else:
            real_tpl = self.template_name

        context['chunk_key'] = real_key
        model = Chunk

        obj = None
        # try to get cached object
        if self.cache_time > 0:
            cache_key = CACHE_PREFIX + self.content_type + get_language() + real_key
            obj = cache.get(cache_key)
        # otherwise get it from database
        if obj is None:
            try:
                obj = model.objects.get(key=real_key)
            except model.DoesNotExist:
                # this place we should create an empty object in database
                obj = model(key=real_key)
                obj.content = real_key
                obj.save()

            # cache the object
            if self.cache_time == 0:
                logger.debug("Don't cache %s" % (real_key,))
            else:
                if self.cache_time is None or self.cache_time == 'None':
                    logger.debug(
                        "Caching %s for the cache's default timeout" % real_key
                    )
                    cache.set(cache_key, obj)
                else:
                    logger.debug(
                        "Caching %s for %s seconds" % (
                            real_key, str(self.cache_time)))
                    cache.set(cache_key, obj, int(self.cache_time))

        # Eventually we want to pass the whole context to the template so that
        # users have the maximum of flexibility of what to do in there.
        if self.with_template:
            new_ctx = template.Context(context)
            if hasattr(obj, 'content'):
                obj.content = Template(obj.content).render(new_ctx)
            new_ctx.update({'obj': obj})
            tpl = template.loader.get_template(real_tpl)
            return tpl.render(new_ctx)
        elif hasattr(obj, 'content'):
            return escape(obj.content)
        return None


class BasicChunkWrapper(object):
    def __call__(self, parser, token):
        self.prepare(parser, token)
        return ChunkNode(self.key, self.is_variable, self.cache_time,
                         name=self.name,
                         tpl_is_variable=self.tpl_is_variable,
                         content_type=self.content_type)

    def prepare(self, parser, token):
        """
        The parser checks for following tag-configurations::

            {% textchunk {key} %}
            {% textchunk {key} {timeout} %}
            {% textchunk {key} {timeout} {content_type} %}
            {% textchunk {key} {timeout} {content_type} {tpl_name} %}
        """
        tokens = token.split_contents()
        self.is_variable = False
        self.tpl_is_variable = False
        self.key = None
        self.cache_time = 0
        self.name = None
        self.content_type = 'text'

        tag_name, self.key, args = tokens[0], tokens[1], tokens[2:]
        num_args = len(args)

        if num_args not in range(4):
            t = "%r tag should have up to three arguments"
            raise template.TemplateSyntaxError(t % (tokens[0],))

        if num_args >= 1:
            self.cache_time = args[0]
        if num_args >= 2:
            self.content_type = args[1]
        if num_args == 3:
            self.name = args[2]  # template or tag name

        # Check to see if the slug is properly double/single quoted
        if not (self.key[0] == self.key[-1] and self.key[0] in ('"', "'")):
            self.is_variable = True
        else:
            self.key = self.key[1:-1]

        # Clean up the template name
        if self.name:
            if not (self.name[0] == self.name[-1]
                    and self.name[0] in ('"', "'")):
                self.tpl_is_variable = True
            else:
                self.name = self.name[1:-1]

        if self.cache_time is not None and self.cache_time != 'None':
            self.cache_time = int(self.cache_time)


class PlainChunkWrapper(BasicChunkWrapper):
    def __call__(self, parser, token):
        self.prepare(parser, token)
        return ChunkNode(
            self.key, self.is_variable, self.cache_time,
            False, content_type=self.content_type)


do_get_chunk = BasicChunkWrapper()
do_plain_chunk = PlainChunkWrapper()

register.tag('textchunk', do_get_chunk)
register.tag('textchunk_plain', do_plain_chunk)
