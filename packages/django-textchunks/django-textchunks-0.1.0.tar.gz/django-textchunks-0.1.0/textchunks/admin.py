# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


class ChunkAdmin(admin.ModelAdmin):
    list_display = ('key', 'content')
    search_fields = ('key', 'content')


admin.site.register(models.TextChunk, ChunkAdmin)
