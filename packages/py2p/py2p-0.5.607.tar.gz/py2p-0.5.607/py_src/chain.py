from __future__ import print_function
from __future__ import absolute_import

import hashlib
import json
import random
import select
import socket
import struct
import sys
import time
import traceback
import warnings

try:
    from .cbase import protocol
except:
    from .base import protocol

from .base import (flags, compression, to_base_58, from_base_58,
                base_connection, message, base_daemon, base_socket,
                InternalMessage, json_compressions)
from .mesh import mesh_socket
from .utils import (getUTC, get_socket, intersect, awaiting_value, most_common)

default_protocol = protocol('chain', "Plaintext")  # SSL")


class tx(object):
    pass


class block(object):
    pass


class chain_socket(mesh_socket):
    def __init__(self, addr, port, prot=default_protocol, out_addr=None,
                 debug_level=0):
        """Initializes a chain socket

        Args:
            addr:           The address you wish to bind to (ie: "192.168.1.1")
            port:           The port you wish to bind to (ie: 44565)
            prot:           The protocol you wish to operate over, defined by
                                a :py:class:`py2p.base.protocol` object
            out_addr:       Your outward facing address. Only needed if you're
                                connecting over the internet. If you use
                                '0.0.0.0' for the addr argument, this will
                                automatically be set to your LAN address.
            debug_level:    The verbosity you want this socket to use when
                                printing event data

        Raises:
            socket.error:   The address you wanted could not be bound, or is
                                otherwise used
        """
        super(chain_socket, self).__init__(
            addr, port, prot, out_addr, debug_level)
