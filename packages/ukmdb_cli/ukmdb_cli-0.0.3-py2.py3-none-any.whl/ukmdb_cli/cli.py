#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""UKMDB CLI.

Usage: ukm_cli [--help] [--verbose] [--debug ...] <command> [<args>...]

  ukm_cli [--debug ...] add_host [--help] <fqdn> [--comment=<comment>] [--set-tags=<tags>] [KEY_VALUE] ...
  ukm_cli [--debug ...] edit_host [--help] <fqdn> [--comment=<comment>] [--set-tags=<tags> | --add-tags=<tags> | --del-tags=<tags>] [KEY_VALUE] ...
  ukm_cli [--debug ...] del_host [--help] <fqdn> [--comment=<comment>]

  ukm_cli [--debug ...] sniff_arp [--help] <iface>

  ukm_cli [--debug ...] mq_info
  ukm_cli [--debug ...] mq_ping [--help] [--timing] [--max-timing=<msec>]

  ukm_cli [--debug ...] get_id <uuid> [--help]
  ukm_cli [--debug ...] get_uuid <app_domain> <app_name> <app_id> [--help]

  ukm_cli [--debug ...] itop_info

Options:
  -v --verbose             Show more information.
  -d --debug               Show debug information (maybe multiple).

  ukm_cli (-h | --help)
  ukm_cli --version

"""

import logging
from docopt import docopt
from ukmdb_cli import cmd_get_uuid
from ukmdb_cli import cmd_get_id
from ukmdb_cli import cmd_mq_ping
from ukmdb_cli import cmd_itop_info
from ukmdb_cli import cmd_mq_info, cmd_add_host, cmd_edit_host, cmd_del_host
from ukmdb_cli import cmd_sniff_arp
from ukmdb_cli.cmd_base import validate, set_debug_level
from ukmdb_cli import __version__


ukmdb_log = logging.getLogger("ukmdb")


def main():
    arguments = docopt(__doc__, options_first=True, version=__version__)
    set_debug_level(ukmdb_log, arguments)

    ukmdb_log.debug(u'program start')

    if arguments['<command>'] == 'mq_ping':
        ukmdb_log.debug(u"starting command 'mq_ping'")
        cmd_mq_ping.cmd(validate(docopt(cmd_mq_ping.__doc__),
                                 cmd_mq_ping.SCHEMA))
    elif arguments['<command>'] == 'mq_info':
        cmd_mq_info.cmd(validate(docopt(cmd_mq_info.__doc__),
                                 cmd_mq_info.SCHEMA))
    elif arguments['<command>'] == 'get_id':
        cmd_get_id.cmd(validate(docopt(cmd_get_id.__doc__),
                                cmd_get_id.SCHEMA))
    elif arguments['<command>'] == 'get_uuid':
        cmd_get_uuid.cmd(validate(docopt(cmd_get_uuid.__doc__),
                                  cmd_get_uuid.SCHEMA))
    elif arguments['<command>'] == 'itop_info':
        cmd_itop_info.cmd(validate(docopt(cmd_itop_info.__doc__),
                                   cmd_itop_info.SCHEMA))
    elif arguments['<command>'] == 'edit_host':
        cmd_edit_host.cmd(validate(docopt(cmd_edit_host.__doc__),
                                   cmd_edit_host.SCHEMA))
    elif arguments['<command>'] == 'add_host':
        cmd_add_host.cmd(validate(docopt(cmd_add_host.__doc__),
                                  cmd_add_host.SCHEMA))
    elif arguments['<command>'] == 'del_host':
        cmd_del_host.cmd(validate(docopt(cmd_del_host.__doc__),
                                  cmd_del_host.SCHEMA))
    elif arguments['<command>'] == 'sniff_arp':
        cmd_sniff_arp.cmd(validate(docopt(cmd_sniff_arp.__doc__),
                                   cmd_sniff_arp.SCHEMA))
    else:
        exit(
            "{0} is not a command. See 'ukm_cli --help'.".format(
                arguments['<command>']))
