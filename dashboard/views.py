from django.shortcuts import render, redirect
import shopify
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from installer.models import ShopDeatz
from django.core.exceptions import ObjectDoesNotExist
from .models import ModalCustomizations
import hmac

# ############################################################################################################################################
# #  Support Functions
# ############################################################################################################################################


# We need  full shop URL to pass as arguement when rendering the EASDK initialization Javascript (templates/EASDK_JS.html)
def construct_shop_url():
    # Initalize Current Shop Object to extract shop domain and construct full_shop_url,
    try:
        current_shop = shopify.Shop.current()
    except Exception:
        current_shop = ''

    full_shop_url = 'https://' + current_shop.domain
    return full_shop_url



@csrf_protect
def index(request):

    ###########################################################################################################
    # Shop Request Validation and Authentication
    #########################################################################################################

    # Since, the URL for this view is requested from within the iframe, it is no longer requested by shopify, but rather by your webserver.
    # It is as if the user was on our website requesting pages directly so shopify cannot add arguements to the requests.
    # As such, the 'shop' item is no longer passed by shopify in the request
    # So to get shop_url, veriy the request's origin we need to do so using the HMAC that is passed in the first request comming from shopify
    # You should avoid using the shop_login decorator becaus that uses sessions meaning that if the user emptys his browser cookies or logs
    # in from a different computer then he will need to  re-install the app (restart 0auth flow) in order to recieve a new Session.

    # Get the Hmac from the request query
    login_hmac = str(request.GET.get('hmac', False))

    # Then build the request query string (in lexographical order) without the HMAC entry to pass to hmac_validator()
    # see example in shopifydev/info/hmac.py
    query_dictionary = dict(request.GET.iterlists())
    print query_dictionary
    query_string = ''
    for key in sorted(query_dictionary):
        if key == 'hmac':
            continue
        value = query_dictionary[key][0]  # because it comes back as a single item list
        value = value.replace('%3A', ':')
        value = value.replace('%2F', '/')
        value = value.replace('%', r'%26')
        value = value.replace('&', r'%25')
        value = value.replace('=', r'%3d')

        key = key.replace('%', r'%26')
        key = key.replace('&', r'%25')
        key = key.replace('=', r'%3d')

        query_string = query_string + key + '=' + value + '&'

    #remove the trailing '&'
    query_string = query_string[:-1]

    print 'hmac query string = %s' %(query_string)
    h = hmac.new(settings.SHOPIFY_API_SECRET, query_string, hashlib.sha256)
    calculated_hmac = (h.hexdigest())

    # HMAC VALUES MATCH
    if calculated_hmac == login_hmac:
        print 'hmac values match'
        shop_url = request.GET.get('shop', False)
        try:
            # Verify that shop_url exists in DB,
            ShopDeatzInst = ShopDeatz.objects.get(shop_url=str(shop_url))

        # This Exception will help to stop Apache from bugging out in cases where you are making DB and API calls using non existant stores
        # i.e, when the db.sql is reinitialized while a store still has the app installed but is not present in local DB
        except ObjectDoesNotExist:
            print 'Error: %s shop has app installed but is not present in the DB' %(shop_url)
            return redirect('https://www.shopify.com/login')

        # If the above authentication tests were passed then create a session for the user to authenticate any 
        # further requests he makes to our web server and drop the session cookie
        request.session['MYEXAMPLEAPP_SESS'] = shop_url
        request.session['MYEXAMPLEAPP_DKEY'] = ShopDeatzInst.download_key
        request.session.modified = True
        pass

    #HMAC VALUES DO NOT MATCH
    else:
        print 'hmac DOES NOT MATCH'
        print 'checking if user can be authenticated via a valid session'

        # Step1 : Try  to get session tokens 
        try:
            shop_url = request.session['MYEXAMPLEAPP_SESS'] 
            download_key = request.session['MYEXAMPLEAPP_DKEY'] 

            # Step2: Verify that shop_url exists in DB,
            try:
                ShopDeatzInst = ShopDeatz.objects.get(shop_url=str(shop_url))

            # This Exception will help to stop Apache from bugging out in cases where you are making DB and API calls using non existant stores
            # i.e, when the db.sql is reinitialized while a store still has the app installed but is not present in local DB
            except ObjectDoesNotExist:
                print 'Error: %s shop has app installed but is not present in the DB' %(shop_url)
                return redirect('https://www.shopify.com/login')

            # Step3: Verify that the download key of the user's second token matches the store of the user's first token
            if download_key == ShopDeatzInst.download_key:
                pass
            else:
                return redirect('https://www.shopify.com/login')

        except Exception:
            return redirect('https://www.shopify.com/login') 

    # If all of the above checks pass then activate your shopify session to make api calls
    session = shopify.Session(shop_url, ShopDeatzInst.auth_token)
    shopify.ShopifyResource.activate_session(session)

    ##########################################################################################################
    # View Code
    #########################################################################################################
    print "hhere"
    # At this point you can emit API calls directly without having to 'activate your session' because once the app is installed,
    # session activation is automatically done by the middleware

    # If this is a page request and not a <POST> then 'submitted' key will not be present in request.POST, 
    # in this case just get current styles from DB and render the requested page

    if 'submitted' not in request.POST:
        
        # Get current styes from DB and render them in context
        ModalCustInst = ModalCustomizations.objects.get(shop_url=shop_url)
        
        context = {
                   'SHOPIFY_API_KEY': settings.SHOPIFY_API_KEY,
                   'full_shop_url': construct_shop_url,
                   'popup_message': ModalCustInst.popup_message,
                   'page_title': 'Customize Pop-Up Modal',
                  }

    
        return render(request, 'dashboard/custpop.html', context)

    # Otherwise, this means the user is posting data (clicked the save button on dashboard), so continue with code execution to preocess data
    else:
        pass

    # Capture Posted Data
    popup_message = request.POST['popup-message']

    # Write data to DB
    ModalCustInst = ShopCustomizations.objects.get(shop_url=shop_url)
    ModalCustInst.popup_message = popup_message
    ModalCustInst.save()

    # Pass new customizations into context and re-load customizepop.html with new values
    context = {
                'SHOPIFY_API_KEY': settings.SHOPIFY_API_KEY,
                'full_shop_url': construct_shop_url,
                'popup_message': ModalCustInst.popup_message,
                'page_title': 'Customize Pop-Up Modal',       
              }

    return render(request, 'dashboard/custpop.html', context)



