import importlib
import logging
import sys

from .service import TempgresDatabaseService

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

if ('test' in sys.argv):
    logger.info("Using Tempgres as the test database.")

    if not hasattr(settings, 'TEMPGRES'):
        raise ImproperlyConfigured(
            "settings.TEMPGRES is improperly configured. "
            "Could not find attribute TEMPGRES in settings."
            )

    if not isinstance(settings.TEMPGRES, dict):
        raise ImproperlyConfigured(
            "settings.TEMPGRES is improperly configured. "
            "Attribute TEMPGRES must be a dictionary."
            )

    settings_dict = settings.TEMPGRES

    url_key = 'URL'
    port_key = 'PORT'

    if not (url_key in settings_dict):
        raise ImproperlyConfigured(
            "settings.TEMPGRES is improperly configured. "
            "Please supply the URL value.")

    port = ':{}'.format(settings_dict[port_key]) \
        if port_key in settings_dict else ''
    url = '{}{}'.format(settings_dict['URL'], port)

    tmpgres = TempgresDatabaseService(url)

    logger.debug("Tempgres database information:")
    logger.debug(str(tmpgres))

    settings.DATABASES = {
        'default': {
            'ENGINE': 'tempgres.db.backends.tempgres',
            'NAME': tmpgres['NAME'],
            'USER': tmpgres['USER'],
            'PASSWORD': tmpgres['PASSWORD'],
            'HOST': tmpgres['HOST'],
            'PORT': tmpgres['PORT'],
            'TEST': {
                'NAME': tmpgres['NAME'],
                'USER': tmpgres['USER'],
                'PASSWORD': tmpgres['PASSWORD'],
                'HOST': tmpgres['HOST'],
                'PORT': tmpgres['PORT'],
            }
        }
    }

    if not (any(o in sys.argv for o in ['-k', '--keepdb'])):
        # Force use of --keepdb if this backend is used for testing.
        # The inner logic of the backend ignores --keepdb, but Django's
        # test framework prints out misleading information unless we use --keepdb.
        logger.info("Forcing --keepdb")

        sys.argv.append('--keepdb')
