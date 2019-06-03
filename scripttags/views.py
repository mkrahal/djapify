#s-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from installer.models import ShopDeatz
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from dashboard.models import ModalCustomizations

# Create your views here.

# This view is to returns the ScriptTag's source JS when it is requested by the store. 
# The returned source JS then injects HTML into the store front code.
def scripttagsrc1(request): 
    print 'scriptsrc.views()'

    # Get the name of the current shop
    # use request.GET['shop'] as shop_url is passed with the <GET> request
    try:
        shop_url = request.GET['shop']
    
    except Exception:
        shop_url = 'nostoreError'        # Block to handle Multivalue error

    # Add switch to check if store exists in our registered store's DB. In case store does not exist in our DB, return HTTPBadRequest
    # if the store exists, it will make one further check to verify that the access token passed for the store corresponds to the one
    # we have in our DB. If it does it means that the request is legitimately comming from the store, if they don't match, then someone
    # could be attempting to forge fake sessionsi using the shop_url to access data (but he does not have the auth token)
    try:
        # Verify that shop_url exists in DB,
        ShopDeatzInst = ShopDeatz.objects.get(shop_url=str(shop_url))
 
    # This Exception will help to stop Apache from bugging out in cases where you are making DB and API calls using non existant stores
    # i.e, when the db.sql is reinitialized while a store still has the app installed but is not present in local DB
    except ObjectDoesNotExist:
        print 'Error: %s shop has app installed but is not present in the DB' % (shop_url)
        return HttpResponseForbidden()

    
    ##########################################################################################################
    # View Code
    #########################################################################################################
 
    # Execute this code to return the JS only if the above two tests were passed
    
    # Create model instances to fetch styles from dashboard.models.ShopCustomizations to render templates
    ModalCustomSettingsINSTANCE = ModalCustomizations.objects.get(shop_url=shop_url)
    
    # Convert sleep time to milliseconds, it needs to be passed in milli-seconds to JavaScript 
    time_delay_millisec = ModalCustomSettingsINSTANCE.time_delay * 1000      

    context = {
               'background_color': ModalCustomSettingsINSTANCE.background_color,
               'text_color': ModalCustomSettingsINSTANCE.text_color,
               'secondary_text_color': ModalCustomSettingsINSTANCE.secondary_text_color,
               'active_tab_text_color': ModalCustomSettingsINSTANCE.active_tab_text_color,
               'accept_color': ModalCustomSettingsINSTANCE.accept_color,
               'decline_color': ModalCustomSettingsINSTANCE.decline_color,
               'font_size': ModalCustomSettingsINSTANCE.font_size,
               'behaviour': ModalCustomSettingsINSTANCE.widget_behaviour,
               'time_delay': time_delay_millisec,
               'shop_url': shop_url,
              }


    # render and return the JS scripttag injection code
    return render(request, 'scripttag_src/JS_storefront_injection.html', context)

