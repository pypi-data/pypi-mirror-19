==========
Simpleauth
==========

Simpleauth is a simple app created for the class requirement.
Detailed documentation (if any!) is with in the source files as comments.

(I'd suggested to go through the source, since that would be an easier task than to
figure out manually)

Quick start
-----------
1. Include the shopcart urlconf in your project urls.py like this::

   urlpatterns = [
        ...
        url(r'^simpleauth/', include('simpleauth.urls')),
   ]


2. Add "shopcart" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = [
        ...
        'simpleauth',
   ]

3. Modify the DATABASES section
   (Recommended DB is MySQL, but you can use sqlite3.)::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '{DATABASE_NAME}',
            'USER' : '{DATABASE_USER}',
            'PASSWORD' : '{DATABASE_PASSWORD}',
        }
    }

4. Make the migrations
   (This is used to generate the DB table)::

   $ python3 manage.py makemigrations simpleauth

5. Then, migrate to DB::

   $ python3 manage.py migrate simpleauth

3. Start the development server and visit http://127.0.0.1:8000/simpleauth/ to view the
   simpleauth app


