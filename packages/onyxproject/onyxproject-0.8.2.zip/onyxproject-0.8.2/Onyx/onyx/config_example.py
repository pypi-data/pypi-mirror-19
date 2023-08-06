# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""

from os.path import dirname, abspath, join, exists
import os

INSTALL_FOLDER = 'install'
SECRET_KEY = 'change me please'
SECURITY_PASSWORD_SALT= 'change me please'


basedir = os.path.abspath(os.path.dirname(__file__))

import onyx
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+str(list(onyx.__path__)[0]) + "/db/data.db"
SQLALCHEMY_MIGRATE_REPO = str(list(onyx.__path__)[0]) + "/db/db_repository"
SQLALCHEMY_TRACK_MODIFICATIONS = True

# flatpages
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = join(dirname(__file__), 'docs')
del dirname, abspath, join

# default babel values
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'
ACCEPT_LANGUAGES = ['en', 'fr', ]

# available languages
LANGUAGES = {
    'en': u'English',
    'fr': u'Français'
}

MAIL_SERVER= ''
MAIL_PORT=  465
MAIL_USERNAME= ''
MAIL_PASSWORD= ''
MAIL_USE_TLS= False
MAIL_USE_SSL= True
# Celery
BROKER_TRANSPORT = 'redis'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACCEPT_CONTENT = ['json',]

# cache
CACHE_TYPE = 'memcached'
CACHE_MEMCACHED_SERVERS = ['127.0.0.1:11211', ]
# CACHE_MEMCACHED_USERNAME =
# CACHE_MEMCACHED_PASSWORD =
