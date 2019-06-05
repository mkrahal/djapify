# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class ModalCustomizations(models.Model):
    shop_url = models.CharField(max_length=300)
    popup_message = models.CharField(max_length=500, default='This is an example of storefront manipulation using scripttag JavaScript injection. When the store home page is loaded, the that were registered on app install send a request to the app webserver, which then returns a piece of JavaScript code, this code is executed on load allowing app developers to inject HTML, CSS, and JS in order to directly modify the way the storefront appears/behaves (such as creating this pop-up modal and message.')

