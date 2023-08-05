# =============================================================================
# asr9k
#
# Copyright (c)  2016, Cisco Systems
# All rights reserved.
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
from csmpe.plugins import CSMPlugin
from plugin_lib import parse_show_platform


class Plugin(CSMPlugin):
    """This plugin checks the states of all nodes"""
    name = "Node Status Check Plugin"
    platforms = {'ASR9K', 'NCS1K', 'NCS5K', 'NCS5500', 'NCS6K'}
    phases = {'Pre-Upgrade', 'Post-Upgrade'}
    os = {'eXR'}

    def run(self):
        output = self.ctx.send("show platform")

        inventory = parse_show_platform(output)
        valid_state = [
            'IOS XR RUN',
            'PRESENT',
            'READY',
            'FAILED',
            'OK',
            'DISABLED',
            'UNPOWERED',
            'ADMIN DOWN',
            'OPERATIONAL',
            'NOT ALLOW ONLIN',  # This is not spelling error
        ]
        for key, value in inventory.items():
            if 'CPU' in key:
                if value['state'] not in valid_state:
                    self.ctx.warning("{}={}: {}".format(key, value, "Not in valid state for upgrade"))
                    break
        else:
            self.ctx.save_data("inventory", inventory)
            self.ctx.info("All nodes in valid state for upgrade")
            return True

        self.ctx.error("Not all nodes in correct state. Upgrade can not proceed")
