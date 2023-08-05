#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Simple Psycopg2 Wrapper

:copyright: (c) 2015 Gary Chambers
:license: MIT
'''


from psycopg2 import (IntegrityError, InterfaceError, DatabaseError,
                      OperationalError, ProgrammingError)
from .psypg_wrap import PgConfig, pg_query, pg_commit, pg_rollback, pg_notify

__title__ = 'psypg'
__version__ = '1.5'
__all__ = ['IntegrityError', 'InterfaceError', 'DatabaseError',
           'OperationalError', 'ProgrammingError', 'PgConfig',
           'pg_query', 'pg_commit', 'pg_rollback']
