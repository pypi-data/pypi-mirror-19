# django-oauth

Description
--------
Djdg Django Oauth provides a simple signature middleware verification between apps

Support
-------
mail to zane.yang@hey900.com

Requirements
------------

* Python 2.7
* Django  1.9

Installation
------------

**Install with pip**

    pip install djdg-django-oauth

**Add `djdg_oauth` to your `INSTALLED_APPS`**


    INSTALLED_APPS = (
        ...
        'djdg_oauth',
    )

**run migrate to add tables:**


	python manage.py migrate djdg_oauth


**list, add, del app secret:**

    python manage.py listauthapp {app_name}
    python manage.py addauthapp {app_name}
    python manage.py delauthapp {app_name}

**add middleware**(**options**,  *you can create yourself middleware with   djdg_oauth.oauthclient.OauthClient.verify_request*):

    MIDDLEWARE_CLASSES = (
    ...
    'djdg_oauth.middleware.DjdgAuthMiddleware',
)

**add settings**(*app secret gaved by others*)

    DJDG_AUTH = {
        "APPS": [
            {"appid": "xxxxxx", "secret": "xxxxxxxxxxxxxxxxxxx", "app": "xxx"},
              ....
        ]
        "FULL_ESCAPE_URL": [....] # full match url to escape auth check,
        "REGEX_ESCAPE_URL": [....] # regex match url to escape auth check,
		"REGEX_CHECK_URL":[...] # need check url, if not empty, escape urls invalid
    }
)

Documentation
--------------

**Verify request**

	from djdg_oauth.oauthclient import OauthClient
	auth = OauthClient()
	auth.verify(request)

**Do request**

	from djdg_oauth.oauthclient import OauthClient
	request_data = {
		"url": #url,
		"app": #app type,
		"parameters": #all request data,
		"method": #request method,
		"headers": #default None
	}
	OauthClient.oauth_request(**request_data)


License
-------

djdg-oauth is released under the terms of the **BSD license**. Full details in ``LICENSE`` file.

Changelog
---------

version 0.0.20

debug ascii error


