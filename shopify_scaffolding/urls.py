from django.conf.urls import include, url
from django.contrib import admin

from installer.views import login, authenticate, finalize, logout, webhook, activateRecurringCharge
from dashboard.views import index,
from scripttags.views import scripttagsrc1

urlpatterns = [
                #url(r'admin/', admin.site.urls),
                url(r'^$', login, name='shopify_app_login'),

                # Installer
                url(r'^authenticate/$', authenticate, name='shopify_app_authenticate'),
                url(r'^finalize/$', finalize, name='shopify_app_finalize'),
                url(r'^logout/$', logout, name='shopify_app_logout'),
                url(r'^webhook/$', webhook, name='shopify_app_webhook'),
                url(r'^activatecharge/$', activateRecurringCharge, name='activate_charge'),

                # Dashboard
                url(r'^$', index, name='root_path'),

                # Script Tags
                url(r'^scriptsrc1/$', scripttagsrc1, name='first_script_tag'),
                
              ]
