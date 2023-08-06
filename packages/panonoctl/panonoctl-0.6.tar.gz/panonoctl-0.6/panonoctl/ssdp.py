# Copyright 2016 Florian Lehner. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import socket
import struct

class ssdpNotify:
    def getLocation(self, data):
        ws = None
        lines = data.decode().split("\r\n")
        for line in lines:
            if line.startswith("LOCATION:"):
                content = line.split(" ")
                ws = content[1]
                break
        return ws

    def getApiVersion(self, data):
        vers = None
        lines = data.decode().split("\r\n")
        for line in lines:
            if line.startswith("APIVERSION:"):
                content = line.split(" ")
                vers = content[1]
                break
        return vers

    def getUsn(self, data):
        usn = None
        lines = data.decode().split("\r\n")
        for line in lines:
            if line.startswith("USN:"):
                content = line.split(" ")
                usn = content[1]
                break
        return usn

    def getSrv(self, data):
        srv = None
        lines = data.decode().split("\r\n")
        for line in lines:
            if line.startswith("SERVER:"):
                content = line.split(" ")
                srv = content[1]
                break
        return srv

    @staticmethod
    def discover(self):
        ws      = None
        usn     = None
        apiV    = None
        srv     = None
        req =  ('M-SEARCH * HTTP/1.1\r\n' +
                'MX: 10\r\n' +
                'HOST: 239.255.255.250:1900\r\n' +
                'MAN: \"ssdp:discover\"\r\n' +
                'NT: panono:ball-camera\r\n' +
                '\r\n')
        ws = None
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.settimeout(7)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        mcast = struct.pack('4sL', socket.inet_aton('239.255.255.250') , socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mcast)
        sock.bind(('', 1900))
        try:
            sock.sendto( req.encode(), ('239.255.255.250', 1900))
        except socket.error as e:
            print(e)
            return (None, None, None)
        for _ in range(5):
            try:
                data, addr = sock.recvfrom(1024)
                if not data: continue
                ws = ssdpNotify().getLocation(data)
                if ws is None: continue
                usn = ssdpNotify().getUsn(data)
                apiV = ssdpNotify().getApiVersion(data)
                srv = ssdpNotify().getSrv(data)
                break
            except socket.error as e:
                print(e)
                break
        sock.close()
        return (ws, usn, apiV, srv)
