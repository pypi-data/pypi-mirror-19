#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ukmdb_cli
----------------------------------

Tests for `ukmdb_cli` module.
"""

# import pytest

from unittest import TestCase
from freezegun import freeze_time
import datetime
from ukmdb_cli import cmd_base


def mocked_get_now(timezone):
    return datetime.datetime(2001, 12, 31, 11, 22, 33)
    # dt = datetime.datetime(2012, 1, 1, 10, 10, 10)
    # return timezone.localize(dt)


class TestUkmdbCli(TestCase):

    @classmethod
    def setup_class(cls):
        pass

    def test_get_uuid(self):
        test_domain = 'test_domain'
        test_type = 'test_type'
        test_name = 'test_name'
        test_id = 'test_id'
        check_uuid = '9a9df032-c57b-5954-827e-f1657b351482'
        gen_uuid = cmd_base.get_uuid(test_domain, test_type,
                                     test_name, test_id)
        self.assertEqual(check_uuid, str(gen_uuid))

    @freeze_time("2012-12-28")
    def test_in_ndays(self):
        self.assertEqual(cmd_base.in_ndays(3),
                         datetime.datetime(2012, 12, 31))

    @freeze_time("2012-12-28")
    def test_tomorrow(self):
        self.assertEqual(cmd_base.tomorrow(),
                         datetime.datetime(2012, 12, 29))

    @freeze_time("2012-12-28")
    def test_conv_dict(self):
        test_domain = 'test_domain'
        test_type = 'test_type'
        test_name = 'test_name'
        test_id = 'test_id'
        test_props = {'prop1': 'val01',
                      'prop2': 'val02'}
        test_comment = 'The quick brown fox jumps over the lazy dog'
        ret_tupel = cmd_base.conv_dict(test_domain, test_type, test_name,
                                       test_id, test_props, test_comment)
        (ret_uuid, ret_dict, ret_expires) = ret_tupel
        self.assertEqual(str(ret_uuid),
                         '9a9df032-c57b-5954-827e-f1657b351482')
        self.assertEqual(ret_dict, {
            'app_domain': 'test_domain',
            'app_id': 'test_id',
            'app_name': 'test_name',
            'app_type': 'test_type',
            'comment': 'The quick brown fox jumps over the lazy dog',
            'props': {'prop1': 'val01', 'prop2': 'val02'},
            'uuid': '9a9df032-c57b-5954-827e-f1657b351482'
        })
        self.assertEqual(ret_expires, datetime.datetime(2012, 12, 29))

    @classmethod
    def teardown_class(cls):
        pass
