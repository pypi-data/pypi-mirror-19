#    Copyright 2016 Mirantis, Inc.
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

from oslo_messaging._drivers.zmq_driver import zmq_async
from oslo_messaging._drivers.zmq_driver import zmq_socket

zmq = zmq_async.import_zmq()


class SocketsManager(object):

    def __init__(self, conf, matchmaker, socket_type):
        self.conf = conf
        self.matchmaker = matchmaker
        self.socket_type = socket_type
        self.zmq_context = zmq.Context()
        self.socket_to_publishers = None
        self.socket_to_routers = None

    def get_socket(self):
        socket = zmq_socket.ZmqSocket(self.conf, self.zmq_context,
                                      self.socket_type, immediate=False)
        return socket

    def get_socket_to_publishers(self, identity=None):
        if self.socket_to_publishers is not None:
            return self.socket_to_publishers
        self.socket_to_publishers = zmq_socket.ZmqSocket(
            self.conf, self.zmq_context, self.socket_type,
            immediate=self.conf.oslo_messaging_zmq.zmq_immediate,
            identity=identity)
        publishers = self.matchmaker.get_publishers()
        for pub_address, fe_router_address in publishers:
            self.socket_to_publishers.connect_to_host(fe_router_address)
        return self.socket_to_publishers

    def get_socket_to_routers(self, identity=None):
        if self.socket_to_routers is not None:
            return self.socket_to_routers
        self.socket_to_routers = zmq_socket.ZmqSocket(
            self.conf, self.zmq_context, self.socket_type,
            immediate=self.conf.oslo_messaging_zmq.zmq_immediate,
            identity=identity)
        routers = self.matchmaker.get_routers()
        for be_router_address in routers:
            self.socket_to_routers.connect_to_host(be_router_address)
        return self.socket_to_routers
