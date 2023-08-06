#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import logging
import os.path
import psycopg2
import psycopg2.extensions
import psycopg2.extras


# Always return Unicode strings
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

__version__ = '1.5.3'
__date__ = '01/18/2017'
__author__ = 'Gary Chambers'


logger = logging.getLogger('psypg')


def pg_commit(dbh):
    dbh.commit()


def pg_rollback(dbh):
    dbh.rollback()


def pg_notify(dbh, channel, payload=None):
    query = 'select * from pg_notify(%s, %s)'
    return pg_query(dbh, query, [channel, payload], fetch_one=True)


def pg_query(dbh, query, query_parms=None, autocommit=True,
             real_dict_cursor=True, fetch_one=False):
    """A [hopefully not-too-naive] Psycopg2 query wrapper function"""
    curs = dbh.cursor(cursor_factory=psycopg2.extras.RealDictCursor) \
           if real_dict_cursor else dbh.cursor()
    try:
        curs.execute(query, query_parms)
        rows = curs.fetchone() if fetch_one else curs.fetchall()
        curs.close()
        if autocommit:
            dbh.commit()
        return rows
    except Exception as e:
        dbh.rollback()
        raise


class PgConfig(object):
    """A simple class to return a Postgres DSN from a ConfigParser config
    file"""
    __basedir = os.path.abspath(os.path.dirname(__file__))
    # Simple mapping of module config file keywords to Pg DSN keywords
    dsn_keywords = {'dbname': "dbname={0}",
                    'dbpassword': "password={0}",
                    'dbhost': "host={0}",
                    'dbport': "port={0}",
                    'dbuser': "user={0}"}

    def __init__(self, dbschema='testdb',
                 configfiles=[os.path.join(__basedir, 'db.ini')]):
        self.schemaopts = dict()
        self.dbschema = dbschema
        self.cfp = configparser.ConfigParser()
        self.cfp.read([os.path.expanduser(x) for x in configfiles])
        if dbschema not in self.cfp.sections():
            exception_msg = 'Unknown schema: {0}'.format(dbschema)
            raise Exception(exception_msg)
        else:
            for o in self.cfp.options(dbschema):
                self.schemaopts[o] = self.cfp.get(dbschema, o)

    def dsn(self):
        """Build a Pg DSN"""
        dsn = []
        # Permit the caller to override the user name, otherwise
        # use the ConfigParser section.
        if not 'dbuser' in self.schemaopts:
            self.schemaopts['dbuser'] = self.dbschema
        for opt, dsn_str in self.dsn_keywords.items():
            if opt in self.schemaopts:
                dsn.append(dsn_str.format(self.schemaopts[opt]))

        return ' '.join(dsn)

    def sa_uri(self, dialect=None, **kwargs):
        """Generate a SQLAlchemy URI"""
        uri = 'postgresql'
        if dialect:
            uri = uri + '+' + dialect
        uri = uri + '://'
        if 'dbuser' in self.schemaopts:
            uri = uri + self.schemaopts['dbuser']
        else:
            uri = uri + self.dbschema
        if 'dbpassword' in self.schemaopts:
            uri = uri + ':' + self.schemaopts['dbpassword']
        if 'dbhost' in self.schemaopts:
            uri = uri + '@' + self.schemaopts['dbhost']
        if 'dbport' in self.schemaopts:
            uri = uri + ':' + self.schemaopts['dbport']
        uri = uri + '/' + self.schemaopts['dbname']
        if kwargs:
            uri = uri + '?' + '&'.join(
                    ['%s=%s' % arg for arg in kwargs.items()])
        logger.debug('uri: {}'.format(uri))
        return uri

    def get_handle(self):
        return psycopg2.connect(self.dsn())


if __name__ == '__main__':
    d = PgConfig('testdb', ['db.ini'])
    print(d.dsn())
    print (d.sa_uri())
