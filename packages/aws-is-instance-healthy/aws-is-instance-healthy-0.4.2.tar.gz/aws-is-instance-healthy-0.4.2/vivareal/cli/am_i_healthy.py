#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import requests
from vivareal.cli.is_instance_healthy import is_instance_healthy


def who_am_i():
    identity_request = requests.get('http://169.254.169.254/latest/dynamic/instance-identity/document', timeout=2)
    identity = identity_request.json()
    return identity['region'], identity['instanceId']


if __name__ == '__main__':
    import sys

    try:
        me = who_am_i()
    except:
        sys.stderr.write('Unable to retrieve instance identity. Are you running inside an AWS instance?')
        sys.exit(200)

    status = is_instance_healthy(me[0], me[1])
    if status[0]:
        sys.stdout.write('Instance %s is healthy\n' % me[1])
        sys.exit(0)
    else:
        sys.stdout.write('Instance %s is unhealthy!\n' % me[1])
        sys.stderr.write('Instance %s is unhealthy based on %s. Reason: %s\n' % (me[1], status[1], status[2]))
        sys.exit(100)
