# Replace the API Key and Shared Secret with the one given for your
# App by Shopify.
#
# To create an application, or find the API Key and Secret, visit:
# - for private Apps:
#     https://${YOUR_SHOP_NAME}.myshopify.com/admin/api
# - for partner Apps:
#     https://www.shopify.com/services/partners/api_clients
#
# You can ignore this file in git using the following command:
#   git update-index --assume-unchanged shopify_settings.py
import os

# APP URL
APP_DOMAINURL = 'https://cdn1.gdprinsider.ovh'  # !!!! IMPORTANT NO TRAILING '/' at the end of your domain

# API ACCESS
SHOPIFY_API_KEY = '4fdc027a0c4d0e48044ae5ad4ef2ce19'
SHOPIFY_API_SECRET = '80728c3d7509dd1d34c374852f6a0f20'

# See http://api.shopify.com/authentication.html for available scopes
# Set the permisssions your app will need.
SHOPIFY_API_SCOPE = ['read_customers', 'write_customers', 'write_script_tags', 'read_orders']


# Settings for APP recurring payments
APP_NAME = 'MY EXAMPLE APP'
APP_PRICE = 19.99  # Price in USD (always 2 decimal places)
APP_TESTFLAG = True  # Test flag to true will set the RecurringApplicationCharge to NOT actually charge the credit card
APP_RETURNURL = "https://cdn1.gdprinsider.ovh/activatecharge/"  # The URL the customer is sent to when accept/decline charge.
APP_TRIALDAYS = 2

