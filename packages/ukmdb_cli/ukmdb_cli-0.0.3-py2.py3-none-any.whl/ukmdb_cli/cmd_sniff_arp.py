#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
"""usage: ukm_cli [--debug ...] sniff_arp [--help] <iface>

Arguments:
  iface                    interface for listing

Options:
  -h --help                Show this sniff_arp command screen.
  -d --debug               Show debug information.
"""

import logging
import ipaddress
import re
from cachetools import ttl_cache
from scapy.all import sniff, ARP
from schema import Schema, Optional, And, Use
from ukmdb_audit import worker
from ukmdb_cli.cmd_base import get_uuid, tomorrow

ukmdb_log = logging.getLogger("ukmdb")

SCHEMA = Schema({
    'sniff_arp': bool,
    '<iface>': Use(str),
    Optional('--help'): bool,
    Optional('--debug'): And(Use(int), lambda n: n in (0, 1, 2, 3)),
})


def format_mac(mac):
    # remove delimiters and convert to lower case
    mac = re.sub('[.:-]', '', mac).lower()
    mac = ''.join(mac.split())  # remove whitespaces
    assert len(mac) == 12  # length should be now exactly 12 (eg. 008041aefd7e)
    assert mac.isalnum()  # should only contain letters and numbers
    # convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
    mac = ":".join(["%s" % (mac[i:i + 2]) for i in range(0, 12, 2)])
    return mac


@ttl_cache()
def send_new_ip(ip4_addr):
    ukmdb_log.debug("send_new_ip('%s')", ip4_addr)
    ip4_obj = ipaddress.ip_address(ip4_addr)
    ukmdb_type = 'ipv4'
    app_domain = 'net@ikom'
    app_type = ukmdb_type
    app_name = ''
    app_id = str(ip4_obj)
    msg_uuid = get_uuid(app_domain, app_type, app_name, app_id)
    object_dict = {
        'uuid': str(msg_uuid),
        'type': ukmdb_type,
        'props': {},
        'app_domain': app_domain,
        'app_type': app_type,
        'app_name': app_name,
        'app_id': app_id,
        'comment': '',
    }
    worker.add_object.apply_async((object_dict,),
                                  exchange='ukmdb_all_in',
                                  expires=tomorrow())
    return str(msg_uuid)


@ttl_cache()
def send_new_mac(mac_addr):
    ukmdb_log.debug("send_new_mac('%s')", mac_addr)
    mac_str = format_mac(mac_addr)
    ukmdb_type = 'mac_addr'
    app_domain = 'net@ikom'
    app_type = ukmdb_type
    app_name = ''
    app_id = mac_str
    mac_uuid = get_uuid(app_domain, app_type, app_name, app_id)
    object_dict = {
        'uuid': str(mac_uuid),
        'type': ukmdb_type,
        'props': {},
        'app_domain': app_domain,
        'app_type': app_type,
        'app_name': app_name,
        'app_id': app_id,
        'comment': '',
    }
    worker.add_object.apply_async((object_dict,),
                                  exchange='ukmdb_all_in',
                                  expires=tomorrow())
    return str(mac_uuid)


@ttl_cache()
def send_connection_uuid2uuid(uuid1, uuid2, direction):
    ukmdb_log.debug("send_connection_uuid2uuid(%s,%s,%s)",
                    uuid1, uuid2, direction)
    ukmdb_type = 'mac--ip'
    app_domain = 'net@ikom'
    app_type = ukmdb_type
    app_name = ''
    app_id = str(uuid1) + '--' + str(uuid2)
    con_uuid = get_uuid(app_domain, app_type, app_name, app_id)
    object_dict = {
        'uuid': str(con_uuid),
        'type': ukmdb_type,
        'props': {},
        'app_domain': app_domain,
        'app_type': app_type,
        'app_name': app_name,
        'app_id': app_id,
        'item1': uuid1,
        'item2': uuid2,
        'comment': '',
    }
    worker.add_object.apply_async((object_dict,),
                                  exchange='ukmdb_all_in',
                                  expires=tomorrow())
    return str(con_uuid)


def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1, 2):  # who-has or is-at
        ip_uuid = send_new_ip(pkt.psrc)
        mac_uuid = send_new_mac(pkt.hwsrc)
        send_connection_uuid2uuid(mac_uuid, ip_uuid, direction='--')
        # return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")
        # worker.add_object.apply_async((object_dict,),
        #                               exchange='ukmdb_all_in',
        #                               # routing_key='ddd8',
        #                               # reply_to='ddd9',
        #                               # reply_to='ukmdb_all_errors',
        #                               expires=60)


def cmd(args):
    ukmdb_log.debug("starting command 'sniff_arp'")
    print("#############  sniff_arp  #############")
    sniff(iface="en0", prn=arp_monitor_callback, filter="arp", store=0)
    ukmdb_log.debug(str(args))
    ukmdb_log.debug("command 'sniff_arp' stopped")
