# Copyright 2014 Carnegie Mellon University
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Introspection API support.
"""

from novaclient import base


class IntrospectionInterface(base.Resource):
    def __init__(self, manager, data):
        self.drive_id = data['drive_id']
        self.target = data['target']
        self.id = data['introspected_entity_id']

    def __repr__(self):
        return 'IntrospectedEntity <drive_id="%s", target="%s", id="%s">' % \
               (self.drive_id, self.target, self.id)


class IntrospectionManager(base.ManagerWithFind):
    resource_class = IntrospectionInterface 

    def list(self, instance_id):
        return self._list('/servers/%s/os-introspection' % instance_id,
                          'introspected_entities')

    def get(self, instance_id, id):
        return self._get('/servers/%s/os-introspection/%s' % (instance_id, id),
                         'introspection_entity')

    def create(self, instance_id, **kwargs):
        body = {'introspected_entity' : kwargs}
        return self._create('/servers/%s/os-introspection' % instance_id,
                            body, 'introspection_entity')

    def delete(self, instance_id, id):
        self._delete('/servers/%s/os-introspection/%s' % (instance_id, id))
