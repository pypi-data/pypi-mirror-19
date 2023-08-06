#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=
"""usage: ukm_cli [--debug ...] get_uuid <app_domain> <app_name> <app_id> [--help]

Options:
  -h --help                Show this mq_ping command screen.
  -d --debug               Show debug information.
"""

from schema import Schema, Optional, And, Use

SCHEMA = Schema({
    'get_uuid': bool,
    '<app_domain>': Use(str),
    '<app_name>': Use(str),
    '<app_id>': Use(str),
    Optional('--help'): bool,
    Optional('--debug'): And(Use(int), lambda n: n in (0, 1, 2, 3, 4)),
})


def cmd(args):
    if args['--debug']:
        print('DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG DEBUG ')
    print("#############  get_uuid  #############")
    print(args)
