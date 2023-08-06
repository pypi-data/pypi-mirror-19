# -*- coding: utf-8 -*-
from decouple import config

CFG_WATO_URL = config('UKMDB_WATO_URL', default='http://checkmk.xyz.com', cast=str)
CFG_WATO_USERNAME = config('UKMDB_WATO_USERNAME', default='checkmk_user', cast=str)
CFG_WATO_PASSWORD = config('UKMDB_WATO_PASSWORD', default='checkmk_passwd', cast=str)
