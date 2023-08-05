# -*- coding: utf-8 -*-

from django import forms
from .models import TextChunk


class EditForm(forms.ModelForm):
    class Meta:
        model = TextChunk
        fields = ('id', 'content', )
