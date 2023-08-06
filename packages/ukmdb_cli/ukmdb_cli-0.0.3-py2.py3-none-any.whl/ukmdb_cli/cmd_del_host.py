#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0330
"""usage: ukm_cli [--debug ...] del_host [--help] <fqdn> [--comment=<comment>]

Arguments:
  fqdn                fqdn of the host

Options:
  --comment=<comment>      a comment for this command
  -h --help                Show this del_host command screen.
  -d --debug               Show debug information.
"""

import logging
from schema import Schema, Optional, And, Use
from ukmdb_worker import worker
from ukmdb_cli.cmd_base import conv_dict

UKMDB_LOG = logging.getLogger("ukmdb")

SCHEMA = Schema({
    'del_host': bool,
    '<fqdn>': And(Use(str), lambda fqdn: len(fqdn) <= 16, error='wrong fqdn'),
    Optional('--help'): bool,
    Optional('--debug'): And(Use(int), lambda n: n in (0, 1, 2, 3)),
})


def cmd(args):
    UKMDB_LOG.debug("starting command 'del_host'")
    props = {}
    (msg_uuid, obj_dict, expires) = conv_dict('kvm@ikom',  # app_domain
                                              'vhost',  # app_type
                                              'kvm@adm000-kvm16f',  # app_name
                                              args['<fqdn>'],  # app_id
                                              props,
                                              args['--comment'],  # comment
                                              )
    worker.del_object.apply_async((obj_dict,),
                                  exchange='ukmdb_all_in',
                                  expires=expires)
    UKMDB_LOG.debug(str(args))
    UKMDB_LOG.debug("command 'del_host' stopped")
    return str(msg_uuid)
