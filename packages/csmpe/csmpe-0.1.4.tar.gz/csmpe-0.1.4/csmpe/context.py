# =============================================================================
# Context
#
# Copyright (c)  2016, Cisco Systems
# All rights reserved.
#
# # Author: Klaudiusz Staniek
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
# =============================================================================

import logging
import os
import re
from time import time

import condoor

from decorators import delegate


class PluginError(Exception):
    pass


class InstallContext(object):
    _storage = {}

    def __init__(self):
        self.hostname = "Hostname"

    def post_status(self, message):
        print("[CSM Status] {}".format(message))

    def save_data(self, key, value):
        #  print("Saving [{}]={}".format(key, str(value[0])))
        self._storage[key] = value

    def load_data(self, key):
        #  print("Loading [{}]".format(key))
        return self._storage.get(key, (None, None))

    @property
    def custom_commands(self):
        return ["show isis neighbor", "show ospf neighbor", "show bgp summary", "show install inactive summary",
                "show install active summary"]


class Host(object):
    pass


@delegate("_csm", ("post_status",), ("custom_commands", "success", "operation_id", "server_repository_url",
                                     "software_packages", "hostname", "log_directory", "migration_directory",
                                     "get_server", "get_host"))
@delegate("_connection", ("connect", "disconnect", "reconnect", "discovery", "send", "run_fsm", "reload"),
          ("family", "prompt", "os_type", "os_version"))
class PluginContext(object):
    """ This is a class passed to the constructor during plugin instantiation.
    Thi class provides the API for the plugins to allow the communication with the CMS Server and device.
    """
    def __init__(self, csm=None):
        self._csm = csm
        self.current_plugin = ""
        if csm is not None:
            self._connection = condoor.Connection(
                self._csm.hostname,
                self._csm.host_urls,
                log_dir=self._csm.log_directory
            )
            self._set_logging(hostname=self._csm.hostname, log_dir=self._csm.log_directory, log_level=logging.DEBUG)
            self._device_detect()
        else:
            self._connection = None
            self._set_logging()

    def _set_logging(self, hostname="host", log_dir=None, log_level=logging.NOTSET):
        self._logger = logging.getLogger("{}.plugin_manager".format(hostname))
        formatter = logging.Formatter('%(asctime)-15s %(levelname)8s: %(message)s')
        if log_dir:
            if not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir)
                except IOError:
                    log_dir = "./"
            log_filename = os.path.join(log_dir, 'plugins.log')
            handler = logging.FileHandler(log_filename)

        else:
            handler = logging.StreamHandler()

        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(log_level)

    @property
    def TIMEOUT(self):
        return condoor.TIMEOUT

    @property
    def CommandTimeoutError(self):
        return condoor.CommandTimeoutError

    @property
    def phase(self):
        """
        :return: string representing the installation phase.
        """
        try:
            return self._csm.requested_action
        except AttributeError:
            pass
            # raise AssertionError("Requested action not provided")

    def _device_detect(self):
        """Connect to device using condoor"""
        self.info("Phase: Device Discovery")
        self.post_status("Device Discovery")
        self.discovery()
        self.info("Hostname: {}".format(self._connection.hostname))
        self.info("Hardware family: {}".format(self._connection.family))
        self.info("Hardware platform: {}".format(self._connection.platform))
        self.info("OS type: {}".format(self._connection.os_type))
        self.info("Version: {}".format(self._connection.os_version))
        self.info("Connection type: {}".format("console" if self._connection.is_console else "vty"))

        self._csm.save_data("device_info", self._connection.device_info)
        self._csm.save_data("udi", self._connection.udi)

    def _format_log(self, message):
        return "[{}] {}".format(self.current_plugin, message) if self.current_plugin else "{}".format(message)

    def info(self, message):
        """Log INFO message"""
        self._logger.info(self._format_log(message))

    def error(self, message):
        """Log ERROR message"""
        self._logger.error(self._format_log(message))
        self._connection.disconnect()
        raise PluginError
        pass

    def warning(self, message):
        """Log WARNING message"""
        self._logger.warning(self._format_log(message))

    # Storage API
    def save_data(self, key, data):
        """
        Stores (data, timestamp) tuple for key adding timestamp
        """
        self._csm.save_data(key, [data, time()])
        self.info("Key '{}' saved in CSM storage".format(key))

    def load_data(self, key):
        """
        Loads (data, timestamp) tuple for the key
        """
        result = self._csm.load_data(key)
        if result:
            self.info("Key '{}' loaded from CSM storage".format(key))
            if isinstance(result, list):
                return tuple(result)
            else:
                return result, None
        return None, None

    def normalize_filename(self, name):
        filename = re.sub(r"\W+", '-', name)
        filename += ".txt"
        return filename

    def save_to_file(self, name, data):
        """
        Save data to filename in the log_directory provided by CSM
        """

        store_dir = self._csm.log_directory
        file_name = self.normalize_filename(name)
        full_path = os.path.join(store_dir, file_name)
        with open(full_path, "w") as f:
            f.write(data)
            self.info("File '{}' saved in CSM log directory".format(file_name))
            return file_name
        return None

    def load_from_file(self, file_name):
        """
        Load data from file where full path is provided as file_name
        """
        full_path = file_name
        with open(full_path, "r") as f:
            data = f.read()
            self.info("File '{}' loaded from CSM directory".format(os.path.basename(file_name)))
            return data
        return None
