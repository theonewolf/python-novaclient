#!/usr/bin/env python

from getpass import getpass
from logging import basicConfig, DEBUG, getLogger, INFO



from novaclient.v1_1 import client
from novaclient.exceptions import HTTPNotImplemented, NotFound

basicConfig()
LOG = getLogger('introspection-test')
LOG.setLevel(DEBUG)

def try_call(fn, *args, **kwargs):
    try:
        print fn(*args, **kwargs)
    except HTTPNotImplemented:
        LOG.error('<%s> HTTPNotImplemented returned by server!' % fn.__name__)
    except NotFound:
        LOG.error('<%s> NotFound returned by server!' % fn.__name__)

if __name__ == '__main__':
    user = raw_input('Username: ')
    tenant = raw_input('Tenant: ')
    url = raw_input('API URL: ')
    instance = raw_input('Test Instance ID: ')
    entity = raw_input('Test Introspection Entity: ')
    pw = getpass()


    if not user: user = 'wolf'
    if not tenant: tenant = 'SatyaGroup'
    if not url: url = 'http://crimson.aura.cs.cmu.edu:5000/v2.0/'
    if not instance: instance = '25f017ea-b97f-4bd6-a648-fa828b12c98c'
    if not entity: entity = 'TESTENTITY'

    LOG.debug('Connecting novaclient with username "%s", tenant "%s", and ' +
              'URL "%s"', user, tenant, url)
    c = client.Client(user, pw, tenant, url, service_type='compute')

    print c.servers.list()[0].to_dict()

    try_call(c.introspection.list, instance)
    try_call(c.introspection.get, instance, entity)
    try_call(c.introspection.create, instance, drive_id='virtio0',
                                               introspection_target='gammaray')
    try_call(c.introspection.delete, instance, entity)
