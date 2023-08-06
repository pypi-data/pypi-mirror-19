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

import websocket
import simplejson as json

from .ssdp import ssdpNotify as ssdp

def __execute_request__(websocket=None, data=None):
    if data == None:
        return None
    print(data)
    try:
        websocket.send(data)
    except:
        print("An error occured on sending")
        return None

def __check_response__(websocket=None, count=0):
    while True:
        try:
            response = websocket.recv()
            rep = json.loads(response)
            if "error" in rep:
                return rep
            elif "id" in rep:
                if rep["id"] == count:
                    return rep
            elif rep["method"] == "status_update":
                continue
            else:
                # Unknown return
                return rep
        except:
            print("An error occured on receiving")
            return None

class panono:

    def __init__(self, ip=None, port=None, path=None):
        """

        Your Panono camera

        :param ip:      IP of the device you want to connect to
        :param port:    Port you want to connect to
        :param path:    Path you want to connect to
        """
        self.ip     = ip
        self.port   = port
        self.path   = path
        self.ws     = None
        self.usn    = None
        self.apiV   = None
        self.srv    = None
        self.count  = 1

    def connect(self):
        """

        Opens a connection

        """
        ws = None
        # Let us discover, where we need to connect to
        if self.ip == None or self.port == None:
            (ws, self.usn, self.apiV, self.srv) = ssdp.discover(None)
        else:
            ws = "ws://%s" % self.ip
            if not self.port is None:
                ws = "{}:{}".format(ws, self.port)
            if not self.path is None:
                ws = "{}/{}".format(ws, self.path)
        if ws == None:
            return False
        self.ws = websocket.create_connection(ws)
        return True

    def disconnect(self):
        """

        Close a connection

        """
        self.ws.close()
        return

    def getApiVersion(self):
        """
        Returns the API version
        """
        return self.apiV

    def getUsn(self):
        """
        Returns the USN
        """
        return self.usn

    def getServer(self):
        """
        Returns the server
        """
        return self.srv

    def getUpfs(self):
        """

        Get information about all upfs from your Panono.

        Returns all information about all upfs on your Panono.
        """
        data = json.dumps({"id":self.count, "method":"get_upf_infos", "jsonrpc":"2.0"})
        __execute_request__(self.ws, data)
        rep = __check_response__(self.ws, self.count)
        self.count = self.count + 1
        return rep

    def deleteUpf(self, upf=None):
        """

        Delete one upd

        :param upf:     The upf to delete
        """
        if upf == None:
            return None
        data = json.dumps({"id":self.count, "method":"delete_upf", "params":{"image_id":upf},"jsonrpc":"2.0"})
        __execute_request__(self.ws, data)
        rep = __check_response__(self.ws, self.count)
        self.count = self.count + 1
        return rep

    def getStatus(self):
        """

        Get the status of your Panono.

        This includes the version of the firmware, the device_id,
        current state of the battery and more.
        """
        data = json.dumps({"id":self.count, "method":"get_status", "jsonrpc":"2.0"})
        __execute_request__(self.ws, data)
        rep = __check_response__(self.ws, self.count)
        self.count = self.count + 1
        return rep

    def getOptions(self):
        """

        Get the options of your Panono.

        This includes the color temperature and the image type.
        """
        data = json.dumps({"id":self.count, "method":"get_options", "jsonrpc":"2.0"})
        __execute_request__(self.ws, data)
        rep = __check_response__(self.ws, self.count)
        self.count = self.count + 1
        return rep

    def capture(self):
        """

        Capture a photo with your Panono.

        """
        data = json.dumps({"id":self.count, "method":"capture", "jsonrpc":"2.0"})
        __execute_request__(self.ws, data)
        rep = __check_response__(self.ws, self.count)
        self.count = self.count + 1
        return rep

    def auth(self):
        data = json.dumps({"id":self.count, "method":"auth", "params":{"device":"test","force":"test"},"jsonrpc":"2.0"})
        __execute_request__(self.ws, data)
        rep = __check_response__(self.ws, self.count)
        self.count = self.count + 1
        return rep

    def getAuthToken(self):
        """

        Request a token for authentication from your Panono.

        """
        data = json.dumps({"id":self.count, "method":"get_auth_token", "params":{"device":"test","force":"test"},"jsonrpc":"2.0"})
        __execute_request__(self.ws, data)
        rep = __check_response__(self.ws, self.count)
        self.count = self.count + 1
        return rep

    def experimental(self, cmd=None, payload=None):
        """

        Send your own command to your Panono.

        :param cmd:         The command to execute
        :param payload:     The payload, a json object, of your command
        """
        if cmd == None:
            return None
        if payload == None:
            data = json.dumps({"id":self.count, "method":cmd, "jsonrpc":"2.0"})
        else:
            data = json.dumps({"id":self.count, "method":cmd, "params":payload, "jsonrpc":"2.0"})
        __execute_request__(self.ws, data)
        rep = __check_response__(self.ws, self.count)
        self.count = self.count + 1
        return rep
