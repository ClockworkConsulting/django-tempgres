"""
This file is based on the file creation.py from
the PostgreSQL database backend for Django 2.0.4.

It is essentially a backport of a bugfix, but tailored
to use with Tempgres, where we always use an existing
database.
"""

import sys
import logging

import django.db.backends.postgresql.creation as pg_creation

from django.db.backends.utils import strip_quotes

logger = logging.getLogger(__name__)

class DatabaseCreation(pg_creation.DatabaseCreation):
    # Make sure that we can use an already created database
    def _database_exists(self, cursor, database_name):
        cursor.execute('SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s', [strip_quotes(database_name)])
        return cursor.fetchone() is not None

    def _execute_create_test_db(self, cursor, parameters, keepdb=False):
        # Ignore --keepdb as we do not want to create a database
        # when using Tempgres
        if self._database_exists(cursor, parameters['dbname']):
            logger.debug("Found database %s" % parameters['dbname'])
            return
        else:
            sys.stderr.write('Database with name %s does not exist.\n' % parameters['dbname'])
            sys.exit(2)
