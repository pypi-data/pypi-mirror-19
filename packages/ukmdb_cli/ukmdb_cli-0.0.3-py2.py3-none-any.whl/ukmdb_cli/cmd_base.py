#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0103

import logging
import uuid
from datetime import datetime, timedelta
from schema import SchemaError


def validate(args, test_schema):
    try:
        args = test_schema.validate(args)
        return args
    except SchemaError as e:
        exit(e)


def set_debug_level(logger, arguments):
    if arguments['--debug'] == 1:
        logger.setLevel(logging.WARNING)
        logging.basicConfig()
        logger.warning("Debugging with level: 'WARNING'")
    elif arguments['--debug'] == 2:
        logger.setLevel(logging.INFO)
        logging.basicConfig()
        logger.info("Debugging with level: 'INFO'")
    elif arguments['--debug'] > 2:
        logger.setLevel(logging.DEBUG)
        logging.basicConfig()
        logger.debug("Debugging with level: 'DEBUG'")
    else:
        logger.setLevel(logging.ERROR)
        logging.basicConfig()


def get_uuid(app_domain, app_type, app_name, app_id):
    enterprise_number = '1.3.6.1.4.1.7052.'
    oid_cat = enterprise_number + '%' + \
        app_domain + '%' + app_type + '%' + \
        app_name + '%' + app_id
    return uuid.uuid5(uuid.NAMESPACE_OID, oid_cat)


def in_ndays(days):
    return datetime.utcnow() + timedelta(days)


def tomorrow():
    return in_ndays(days=1)


def conv_dict(app_domain, app_type, app_name, app_id, props, comment=''):
    msg_uuid = get_uuid(app_domain, app_type, app_name, app_id)
    object_dict = {
        'uuid': str(msg_uuid),
        'app_domain': app_domain,
        'app_type': app_type,
        'app_name': app_name,
        'app_id': app_id,
        'props': props,
        'comment': comment,
    }
    if app_type in ['vhost', 'host']:
        expires = in_ndays(3)
    else:
        expires = tomorrow()
    return (msg_uuid, object_dict, expires)
