#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0401,W0611,W0614
from decouple import config
from ukmdb_settings.settings_wato import CFG_WATO_URL, \
    CFG_WATO_USERNAME, CFG_WATO_PASSWORD


CFG_DEBUG = config('UKMDB_DEBUG', default=False, cast=bool)
CFG_DB_URL = config('UKMDB_DB_URL', default=None, cast=str)
CFG_MQ_HOST = config('UKMDB_MQ_HOST', default=None, cast=str)
CFG_MQ_TIMEOUT = config('UKMDB_MQ_TIMEOUT', default=1.5, cast=float)
CFG_MQ_VIRTUAL_HOST = config('UKMDB_MQ_VIRTUAL_HOST', default=None, cast=str)
CFG_MQ_USERNAME = config('UKMDB_MQ_USERNAME', default=None, cast=str)
CFG_MQ_PASSWORD = config('UKMDB_MQ_PASSWORD', default=None, cast=str)
CFG_TIMEZONE = config('UKMDB_TIMEZONE', default='Europe/Berlin', cast=str)

CFG_ITOP_URL = config('UKMDB_ITOP_URL', default=None, cast=str)

AMQP_BROKER_URL = "amqp://%s:%s@%s/%s" % (
    CFG_MQ_USERNAME,
    CFG_MQ_PASSWORD,
    CFG_MQ_HOST,
    CFG_MQ_VIRTUAL_HOST,
)
