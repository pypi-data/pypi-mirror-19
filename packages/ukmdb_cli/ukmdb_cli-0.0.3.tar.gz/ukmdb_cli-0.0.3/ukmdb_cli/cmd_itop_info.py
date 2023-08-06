#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""usage: ukm_cli [--debug ...] itop_info

Options:
  -d --debug               Show debug information.
"""

import logging
from schema import Schema, Optional, And, Use
from ukmdb_itop.itop import get_mod_version
from ukmdb_settings import settings

ukmdb_log = logging.getLogger("ukmdb")

SCHEMA = Schema({
    'itop_info': bool,
    Optional('--debug'): And(Use(int), lambda n: n in (0, 1, 2, 3)),
})


def cmd(args):
    ukmdb_log.debug("starting command 'itop_info'")
    ukmdb_log.debug(str(args))

    ukmdb_log.info("ukmdb itop-module version: %s", get_mod_version())
    print("ukmdb itop-module version: %s" % (get_mod_version()))

    ukmdb_log.info("itop url: '%s'", settings.CFG_ITOP_URL)
    print("itop url: '%s'" % (settings.CFG_ITOP_URL))

    ukmdb_log.debug("command 'itop_info' stopped")
