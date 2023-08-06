#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0330
"""usage: ukm_cli [--debug ...] add_host [--help] <fqdn> [--comment=<comment>] [--set-tags=<tags>] [KEY_VALUE] ...

Arguments:
  fqdn                     fqdn of the host

Options:
  --comment=<comment>      a comment for this command
  --set-tags=<tags>        list of new tags, old tags will be deleted,
                           tags are separated by comma
                           e.g. --set-tags=dark.blue,Red,yellow
  KEY_VALUE                key and value in form firstname=Roger
  -h --help                Show this add_host command screen.
  -d --debug               Show debug information.
"""

import logging
from schema import Schema, Optional, And, Use, Or, Regex
from ukmdb_worker import worker
from ukmdb_cli.cmd_base import conv_dict

UKMDB_LOG = logging.getLogger("ukmdb")
SCHEMA = Schema({
    'add_host': bool,
    '<fqdn>': And(Use(str), lambda fqdn: len(fqdn) <= 16, error='wrong fqdn'),
    Optional('--set-tags'): Or(None, Regex('^[a-zA-Z0-9,._-]+$',
                                           error='tags in form aa.de,bb2,Cde')),
    Optional('KEY_VALUE'): list,
    Optional('--help'): bool,
    Optional('--debug'): And(Use(int), lambda n: n in (0, 1, 2, 3)),
})


def cmd(args):
    UKMDB_LOG.info("starting command 'add_host'")
    props = {}
    if args['--set-tags'] is not None:
        props['set-tags'] = args['--set-tags'].split(',')
    for kv_pair in args['KEY_VALUE']:
        key, value = kv_pair.split('=')
        if key not in props.keys():
            props[key] = value
    (msg_uuid, obj_dict, expires) = conv_dict('kvm@ikom',  # app_domain
                                              'vhost',  # app_type
                                              'kvm@adm000-kvm16f',  # app_name
                                              args['<fqdn>'],  # app_id
                                              props,
                                              args['--comment'],  # comment
                                              )
    worker.add_object.apply_async((obj_dict,),
                                  exchange='ukmdb_all_in',
                                  expires=expires)
    UKMDB_LOG.debug(obj_dict)
    UKMDB_LOG.debug(str(args))
    UKMDB_LOG.info("command 'add_host' stopped")
    return str(msg_uuid)
