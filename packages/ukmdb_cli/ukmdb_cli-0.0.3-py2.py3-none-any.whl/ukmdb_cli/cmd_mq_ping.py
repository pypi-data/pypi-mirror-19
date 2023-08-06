#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=
"""usage: ukm_cli [--debug ...] mq_ping [--help] [--timing] [--max-timing=<msec>]

Options:
  -h --help                Show this mq_ping command screen.
  -d --debug               Show debug information.
  -t --timing              Show some timing information after ping.
  --max-timing=<msec>      Wait time in ms for answer [default: 1000].
"""

import logging
from schema import Schema, Optional, And, Use
from ukmdb_worker import worker

ukmdb_log = logging.getLogger("ukmdb")

SCHEMA = Schema({
    'mq_ping': bool,
    Optional('--help'): bool,
    Optional('--timing'): bool,
    Optional('--debug'): And(Use(int), lambda n: n in (0, 1, 2, 3)),
    Optional('--max-timing'): And(Use(float), lambda n: n >= 0.0),
})


def cmd(args):
    ukmdb_log.debug("starting command 'mq_ping'")
    if args['--timing']:
        ukmdb_log.info('with timing information')

    print("#############  mq_ping  #############")
    worker.ukmdb_error.delay('Tote tragen keine Karos')
    # print(args)
    ukmdb_log.debug(str(args))
    ukmdb_log.debug("command 'mq_ping' stopped")
