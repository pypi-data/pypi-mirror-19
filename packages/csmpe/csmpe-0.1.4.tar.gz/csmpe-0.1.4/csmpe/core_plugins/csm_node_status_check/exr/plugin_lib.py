# =============================================================================
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
import re


def parse_show_platform(output):
    """
    :param output: output from 'show platform'
    :return: dictionary of nodes

    Platform: NCS6K
    RP/0/RP0/CPU0:Deploy#show platform
    Node              Type                       State             Config state
    --------------------------------------------------------------------------------
    0/2/CPU0          NC6-10X100G-M-P            IOS XR RUN        NSHUT
    0/RP0/CPU0        NC6-RP(Active)             IOS XR RUN        NSHUT
    0/RP1/CPU0        NC6-RP(Standby)            IOS XR RUN        NSHUT

    Platform: ASR9K-X64
    Node              Type                       State             Config state
    --------------------------------------------------------------------------------
    0/RSP0/CPU0       A9K-RSP880-SE(Active)      IOS XR RUN        NSHUT
    0/RSP1/CPU0       A9K-RSP880-SE(Standby)     IOS XR RUN        NSHUT
    0/FT0             ASR-9904-FAN               OPERATIONAL       NSHUT
    0/0/CPU0          A9K-8X100GE-L-SE           IOS XR RUN        NSHUT
    0/PT0
    """
    inventory = {}
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        if len(line) > 0 and line[0].isdigit():
            states = re.split('\s\s+', line)

            if not re.search('CPU\d+$', states[0]):
                continue

            node, node_type, state, config_state = states

            entry = {
                'type': node_type,
                'state': state,
                'config_state': config_state
            }
            inventory[node] = entry

    return inventory
