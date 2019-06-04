from django.conf import settings
from django.core.urlresolvers import reverse
import shopify

class ConfigurationError(StandardError):
    pass

class LoginProtection(object):
    def __init__(self, get_response):
        self.get_response = get_response

        if not settings.SHOPIFY_API_KEY or not settings.SHOPIFY_API_SECRET:
            raise ConfigurationError("SHOPIFY_API_KEY and SHOPIFY_API_SECRET must be set in settings")
        shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY,
                              secret=settings.SHOPIFY_API_SECRET)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(request, 'session') and 'shopify' in request.session:
            shopify_session = shopify.Session(request.session['shopify']['shop_url'])
            shopify_session.token = request.session['shopify']['access_token']
            shopify.ShopifyResource.activate_session(shopify_session)

    def process_response(self, request, response):
        shopify.ShopifyResource.clear_session()
        return response



# This middleware is essentail in order to allow communication between the server where your app is registered and requests comming from merchants
# that have installed your app. 
# Since your app is rendered as an emmbeded app within the admin panel of your merchant's backends, requests from your app will originate from the
# merchant's store domain and not the domain where your app is hosted which will raise CORS flags and thus be rejected.

# Example: if your app is hosted at abc.com, once it is rendered as an embedded app in the merchant's backend hosted at merchant.myshopify.com 
# and the app attempts to sends a request (POST or GET) back to its host server (abc.com), that request will come from merchant.myshopify.com (not abc.com); and as such it will be rejected by the host server's apache DJANGO engine due to CORS limitations. 

# In order to bypass this limitation, the middleware below allows the domains specified in the response["Access-Control-Allow-Origin"] 
# dictionnary to request resources from the app's host server even though they are not from the same domain origin. 
# note: only the domains listed here will be allowed all others will be rejected 

class corsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"  # Change this to allow only registered merchant store's domains to make requests
        response["Access-Control-Allow-Headers"] =  "Origin, X-Requested-With, Content-Type, Accept, X-Shopify-Web"

        return response
