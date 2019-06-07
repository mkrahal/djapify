# DJAPIFY - Shopify App Development Framework

Djapify is a shopify app development framework for Python and Django.

This framework is made to be used as a functional starting point for the development of shopify apps, with all the necessary low-level structures pre-coded. 

Pre-coded Features:

-  App Installation (authenticate with merchant store using Oauth, create sessions, and request access tokens to make api calls to the store)
-  Webhook registration (recieve uninstallation notices when merchant removes the app)
-  Script tag registration (inject html / css / javascript in order to manipulate storefront) 
-  Embedded App SDK support (use shopify's SDK to embed apps directly in the merchant admin section and provide access to native admin GUI features)
-  Support for handling Cross Origin Requests via a CORS specific middleware
-  Create application charges and activate recurring charges
-  Request permissions for application scope
-  HMAC validation (create and manage sessions using HMAC validation)
-  Gracefully fallback when user declines recurring charge
-  Celery task to periodically check if recurring charge is still active (if recurring charge has been cancelled then the store will be deleted from app server "Registered Store" Database and app service will no longer provided)



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 2.7
* Django
* Rabbit-mq
* Supervisor
* For a complete list of required python libraries see [requirement.txt](https://github.com/mkrahal/djapify/blob/master/extras/requirements.txt)
* App must be hosted on a webserver with a valid SSL certificate (must use https protocol)

### Installing

1. Clone the repository 
	```
	$ git clone https://github.com/mkrahal/djapify
	```

2. Install rabbitmq and its dependencies
	```
	$ sudo apt-get install -y erlang
	$ sudo apt-get install rabbitmq-server
	```

3. Enable rabbitmq to start on boot
	```
	$ sudo systemctl enable rabbitmq-server
	$ sudo systemctl start rabbitmq-server 
	```

4. Install supervisor to run celery cronjobs as daemons (in background)
	```
	$ sudo apt-get install supervisor
	```

5. Install the libraries listed in requirements.txt using pip
	```
	$ pip install -r djapify/extras/requirements.txt
	```

6. Register your app in shopify's partner backend, get your API_KEY and SECRET and register you redirect_url (white listed url)

7. Enter your API_KEY, SECRET, and redirect_url in app_settings.py 

8. Make migrations in django to create your tables from your predefined models using:
   	```
	$ python manage.py makemigrations
	$ python manage.py migrate 
	```
9. Start services and run app
	```
	$ sudo supervisorctl restart shopify_scaffolding_beat
	$ sudo supervisorctl restart shopify_scaffolding
	$ sudo systemctl start rabbitmq-server
	$ python manage.py runserver
	```
	
## Deployment

DO NOT USE DJANGO DEVELOPMENT WEB SERVER IN A PRODUCTION SETTING. 
Production server should be run using a webserver / python engine combination (such as APACHE + wsgi).

## Built With

* [Python 2.7](https://www.python.org/)
* [DJANGO 1.11](https://www.djangoproject.com/)
* [SHOPIFY Python API](https://github.com/Shopify/shopify_python_api)

## Contributing

Please read [CONTRIBUTING.md](https://github.com/mkrahal/djapify/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.


## Built With

* Python 2.7

## Authors

* **MK RAHAL** - *Initial work* - [MK RAHAL](https://github.com/mkrahal)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/mkrahal/djapify/blob/master/LICENSE.md) file for details

