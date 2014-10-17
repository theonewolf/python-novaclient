#!/usr/bin/env python

from getpass import getpass
from subprocess import call
from time import sleep



from novaclient.v1_1 import client
from novaclient.exceptions import HTTPNotImplemented, NotFound



USER        =   'wolf'
TENANT      =   'Testing'
URL         =   'http://crimson.aura.cs.cmu.edu:5000/v2.0/'
ENTITY      =   'TESTENTITY'
NAME        =   'wolf-test-introspection'
KEYPAIR     =   'wolfstack'
PUBLIC_IP   =   '128.2.213.132'
IMAGE       =   '6a587030-5677-40f7-ac99-029a305f9e67'
FLAVOR      =   '6bc0289a-cfbb-4ee4-90f5-de92106dc4bb'



def print_section(section, **kwargs):
    section = '\x1b[37;1m' + section + '\x1b[0m'

    if len(kwargs) > 0:
        args = None
        section += ' ['

        for k,v in kwargs.iteritems():
            section += '%s=\'%s\',' % (k, v)

        section = section[:-1] # take out trailing comma
        section += ']'

    print '--- %s ---' % (section),
    raw_input()

def print_tabbed(lines):
    lines = ''.join(['\t%s\n' % (l) for l in  lines.split('\n')])
    print lines,

def activate_introspection(client, instance):
    entity = client.introspection.create(instance, drive_id='virtio0',
                        introspection_target='gammaray').introspected_entity_id

    print_section('Listing Active Introspections', instance=instance)
    print_tabbed(str(c.introspection.list(instance)))

    c.introspection.delete(instance, entity)

def assign_public_ip(client, instance_id, ip):
    client.servers.add_floating_ip(instance_id, ip)

    while ssh_to_instance(ip, 'sync') != 0:
        sleep(3)
        print '\tTrying ssh...'

    print '\tSSH Succeeded!'

def ssh_to_instance(ip, command=None):
    CMD = ['ssh']
    CMD.append('ubuntu@%s' % (ip))
    CMD.append('-i')
    CMD.append('/home/wolf/Dropbox/Keys/wolfstack.pem')
    CMD.append('-o')
    CMD.append('UserKnownHostsFile=/dev/null')
    CMD.append('-o')
    CMD.append('StrictHostKeyChecking=no')

    if command != None:
        CMD.append(command)

    return call(CMD)

def poll_instance_status(client, instance_id):
    status = None

    while status != 'ACTIVE':
        sleep(3)
        server = client.servers.get(instance_id)
        status = server.status
        print '\t%s' % (status)

    host = getattr(server, 'OS-EXT-SRV-ATTR:hypervisor_hostname')
    host = host.split('.')[0]
    return host

def start_instance(client, name, image, flavor, keypair):
    server = client.servers.create(name=name,
                                   image=image,
                                   flavor=flavor,
                                   key_name=keypair)
    return server.id

def terminate_instance(client, instance):
    client.servers.delete(instance)

def get_image_name(client, image_id):
    name = client.images.get(image_id).name
    return name

if __name__ == '__main__':
    pw = getpass()
    c = client.Client(USER, pw, TENANT, URL, service_type='compute')

    print_section('Connected to OpenStack Controller')
    im_name = get_image_name(c, IMAGE)
    
    instance = start_instance(c, NAME, IMAGE, FLAVOR, KEYPAIR)
    print_section('Spawning Instance', image=im_name, name=NAME)
    
    print_section('Wait for Instance Boot', instance=instance)
    host = poll_instance_status(c, instance)

    print_section('Assigning Public IP', ip=PUBLIC_IP)
    assign_public_ip(c, instance, PUBLIC_IP)

    print_section('Activate Introspection', instance=instance)
    activate_introspection(c, instance)

    print_section('Introspection URL',
            URL='http://crimson.aura.cs.cmu.edu:8000/%s/%s' % (host, instance))

    print_section('SSHing to Instance', ip=PUBLIC_IP)
    ssh_to_instance(PUBLIC_IP)

    print_section('Terminating Instance', instance=instance)
    terminate_instance(c, instance)
