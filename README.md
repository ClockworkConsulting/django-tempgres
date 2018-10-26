# django-tempgres
Tempgres client for django projects

Include app for testing with Tempgres DB

This app, which implements support for using a database provided by a Tempgres
service, in Django. The development of this app was prompted by a bug in Django
2.0.4 which invalidates the --keepdb flag when using the postgresql-backend.

The app is half database-backend, half stand-alone.

The database backend extends the classes DatabaseWrapper and
DatabaseCreation from django.db.backends.postgresql. Specifically, the
method _execute_create_test_db in creation.py has been overridden and
tailored to work with Tempgres (basically just checking if the database
have actually been created). The DatabaseWrapper in base.py simply
points to this new creator-class. The rest of the backend is just the
backend from django.db.backends.postgresql.

The file service.py contacts a Tempgres service and parses the response.
When the temporary database connection information has been received,
the DATABASES variable in Django settings is redefined to user the
tempgres-backend and is updated with the connection information.

The Tempgres service is configured in the Django settings.py file with
the following variable:

    TEMPGRES = {
        'URL': 'http://tempgres.cwconsult.dk',
        'PORT': '8080'
    }

To enable logging, register the app in settings.py:

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        # SIMPLE LOGGING FOR TEMPGRES
        'formatters': {
            'simple_tempgres': {
                'format': '{message}',
                'style': '{',
            },
        },
        'handlers': {
            'console_tempgres': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple_tempgres'
            },
        },
        'loggers': {
            'tempgres': {
                'handlers': ['console_tempgres'],
                'propagate': True,
                'level': 'DEBUG'
            },
        }
    }

Note that in tempgres/settings.py the use of the --keepdb flag is
forced, just so the Django test framework does not print out misleading
information during test setup and teardown.
