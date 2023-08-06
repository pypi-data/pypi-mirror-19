#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103,C0123

"""
test_ukmdb_settings
----------------------------------

Tests for `ukmdb_settings` module.
"""

# import pytest


from ukmdb_settings import settings   # pylint: disable=E0401


class TestUkmdb_settings(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_env_debug(self):
        assert type(settings.CFG_DEBUG) == bool
        assert settings.CFG_DEBUG is False

    def test_env_db_url(self):
        assert type(settings.CFG_DB_URL) == str
        assert settings.CFG_DB_URL == 'sqlite:///./tests.db'

    def test_env_mq_host(self):
        assert type(settings.CFG_MQ_HOST) == str
        assert settings.CFG_MQ_HOST == 'host4test'

    def test_env_mq_timeout(self):
        assert type(settings.CFG_MQ_TIMEOUT) == float
        assert settings.CFG_MQ_TIMEOUT == 1.5

    def test_env_mq_virtual_host(self):
        assert type(settings.CFG_MQ_VIRTUAL_HOST) == str
        assert settings.CFG_MQ_VIRTUAL_HOST == 'virt_host4test'

    def test_env_mq_username(self):
        assert type(settings.CFG_MQ_USERNAME) == str
        assert settings.CFG_MQ_USERNAME == 'test_mq_user'

    def test_env_mq_password(self):
        assert type(settings.CFG_MQ_PASSWORD) == str
        assert settings.CFG_MQ_PASSWORD == 'test_mq_passw0rd'

    def test_env_timezone(self):
        assert type(settings.CFG_TIMEZONE) == str
        assert settings.CFG_TIMEZONE == 'Europe/Berlin'

    @classmethod
    def teardown_class(cls):
        pass
