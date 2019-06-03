# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TemplateDefaults(models.Model):
    template_name = models.CharField(max_length=100)
    background_color = models.CharField(max_length=100)
    text_color = models.CharField(max_length=100)
    secondary_text_color = models.CharField(max_length=100)
    active_tab_text_color = models.CharField(max_length=100)
    accept_color = models.CharField(max_length=100)
    decline_color = models.CharField(max_length=100)
    font_type = models.CharField(max_length=100)
    font_size =  models.CharField(max_length=100)  # 'small', 'normal', 'large'
    time_delay = models.IntegerField(default=0)
    widget_behaviour = models.CharField(max_length=100, default='Default')

    def __str__(self):
        return self.template_name


class ModalCustomizations(models.Model):
    shop_url = models.CharField(max_length=300)
    active_template = models.CharField(max_length=100)
    background_color = models.CharField(max_length=100)
    text_color = models.CharField(max_length=100)
    secondary_text_color = models.CharField(max_length=100)
    active_tab_text_color = models.CharField(max_length=100)
    accept_color = models.CharField(max_length=100)
    decline_color = models.CharField(max_length=100)
    font_type = models.CharField(max_length=100)
    font_size =  models.CharField(max_length=100)  # 'small', 'normal', 'large'
    time_delay = models.IntegerField(default=0)
    widget_behaviour = models.CharField(max_length=100, default='Default')

