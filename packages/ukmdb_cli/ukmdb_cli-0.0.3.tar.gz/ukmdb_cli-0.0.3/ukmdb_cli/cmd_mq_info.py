#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""usage: ukm_cli [--debug ...] mq_info

Options:
  -d --debug               Show debug information.
"""

import logging
from schema import Schema, Optional, And, Use
from ukmdb_amqp.amqp import get_mod_version
from ukmdb_settings import settings

ukmdb_log = logging.getLogger("ukmdb")

SCHEMA = Schema({
    'mq_info': bool,
    Optional('--debug'): And(Use(int), lambda n: n in (0, 1, 2, 3)),
})


def cmd(args):
    ukmdb_log.debug("starting command 'mq_info'")
    ukmdb_log.debug(str(args))

    ukmdb_log.info("ukmdb amqp-module version: %s", get_mod_version())
    print("ukmdb amqp-module version: %s" % (get_mod_version()))

    ukmdb_log.info("mq host: '%s'", settings.CFG_MQ_HOST)
    print("mq host: '%s'" % (settings.CFG_MQ_HOST))

    ukmdb_log.info("mq virtual host: '%s'", settings.CFG_MQ_VIRTUAL_HOST)
    print("mq virtual host: '%s'" % (settings.CFG_MQ_VIRTUAL_HOST))

    ukmdb_log.info("mq username: '%s'", settings.CFG_MQ_USERNAME)
    print("mq username: '%s'" % (settings.CFG_MQ_USERNAME))

    ukmdb_log.info("mq timeout: '%s'", settings.CFG_MQ_TIMEOUT)
    print("mq timeout: '%s'" % (settings.CFG_MQ_TIMEOUT))

    ukmdb_log.debug("command 'mq_info' stopped")
