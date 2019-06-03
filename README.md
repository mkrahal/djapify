# DJAPIFY - Shopify App Development Framework

Djapify is a shopify app development framework for Python and Django.

This framework is made to be used as a functional starting point for the development of shopify apps, with all the necessary low-level structures pre-coded. 

Pre-coded Features:

-  App Installation (authenticate with merchant store using Oauth, create sessions, and request access tokens to make api calls to the store)
-  Webhook registration (recieve uninstallation notices when merchant removes the app)
-  Script tag registration (inject html / css / javascript in order to manipulate storefront) 
-  Embedded App SDK  (use shopify's SDK to embed apps directly in the merchant admin section and provide access to native admin GUI features)
-  Support for handling Cross Origin Requests via a CORS specific middleware
-  Create application charges and activate recurring charges
-  Request permissions for application scope
-  HMAC validation (create and manage sessions using HMAC validation)
-  Gracefully fallback when user declines recurring charge
-  Celery task to periodically check if recurring charge is still active (if not store is deleted from app server "Registered Store" Database and     app service is no longer provided)



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 2.7
* Django
* Rabbit-mq
* Supervisor
* For a complete list of required python libraries see [requirement.txt]()

### Installing

* Clone the repository 
	
```git clone https://github.com/mkrahal/djapify```

1. Install rabbitmq and its dependencies
	$sudo apt-get install -y erlang
	$sudo apt-get install rabbitmq-server

2. Enable rabbitmq to start on boot
	$sudo systemctl enable rabbitmq-server
	$sudo systemctl start rabbitmq-server 

3. Install supervisor to run celery cronjobs as daemons (in background)
	$ sudo apt-get install supervisor

4. Install the libraries listed in requirements.txt using pip
	$pip install -r info/requirements.txt

5. Register your app in shopify's partner backend, get your API_KEY and SECRET and register you redirect_url (white listed url)

6. Enter your API_KEY, SECRET, and redirect_url in shopify_settings.py 

7. Make migrations in django to create your tables from your predefined models using:
   
	$ python manage.py makemigrations
	$ python manage.py migrate 

8. Run Fixtures using $ python manage.py loaddata <fixturename> 
    in this case: 
    $ python manage.py loaddata dashboard/fixtures/default_styles_fixture.json

9. Run your django server
	$python manage.py runserver
	NOTE: This is only for testing! Production server should be run using a webserver / python engine combination (such as APACHE + wsgi).

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Python 2.7](https://www.python.org/)
* [DJANGO 1.11](https://www.djangoproject.com/)
* [SHOPIFY Python API](https://github.com/Shopify/shopify_python_api)

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Built With

* Python 2.7

## Authors

* **MK RAHAL** - *Initial work* - [MK RAHAL](https://github.com/mkrahal)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

