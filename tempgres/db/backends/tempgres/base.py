"""
Tempgres database backend for Django

Based on the PostgreSQL database backend for Django 2.0.4

This backend was developed because a bug in the supplied 
backend prevented Django from using an already existing
database from the Tempgres service.
"""

import django.db.backends.postgresql.base as pg_base

from django.db import DEFAULT_DB_ALIAS

from .creation import DatabaseCreation


class DatabaseWrapper(pg_base.DatabaseWrapper):
    def __init__(self, settings_dict, alias=DEFAULT_DB_ALIAS,
                 allow_thread_sharing=False):
        vendor = 'Clockwork Consulting / postgresql'
        display_name = 'Tempgres / PostgreSQL'

        # Use our own database creator
        self.creation_class = DatabaseCreation

        super().__init__(settings_dict, alias, allow_thread_sharing)
