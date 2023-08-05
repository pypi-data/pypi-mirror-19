from . import mesh
from .utils import (inherit_doc, getUTC, sanitize_packet)
from .base import (flags, to_base_58, from_base_58)

try:
    from .cbase import protocol
except:
    from .base import protocol

from collections import namedtuple

default_protocol = protocol('sync', "Plaintext")  # SSL")


class metatuple(namedtuple('meta', ('owner', 'timestamp'))):
    """This class is used to store metadata for a particular key"""
    pass


class sync_socket(mesh.mesh_socket):
    """This class is used to sync dictionaries between programs. It extends
    :py:class:`py2p.mesh.mesh_socket`

    Because of this inheritance, this can also be used as an alert network

    This also implements and optional leasing system by default. This leasing
    system means that if node A sets a key, node B cannot overwrite the value
    at that key for an hour.

    This may be turned off by adding ``leasing=False`` to the constructor.
    """
    def __init__(self, addr, port, prot=default_protocol, out_addr=None,
                 debug_level=0, leasing=True):
        protocol_used = protocol(prot[0] + str(int(leasing)), prot[1])
        self.__leasing = leasing
        super(sync_socket, self).__init__(
            addr, port, protocol_used, out_addr, debug_level)
        self.data = {}
        self.metadata = {}
        self.register_handler(self.__handle_store)

    def __store(self, key, new_data, new_meta, error=True):
        """Private API method for storing data. You have permission to store
        something if:

        - The network is not enforcing leases, or
        - There is no value at that key, or
        - The lease on that key has lapsed (not been set in the last hour), or
        - You are the owner of that key

        Args:
            key:        The key you wish to store data at
            new_data:   The data you wish to store in said key
            new_meta:   The metadata associated with this storage
            error:      A boolean which says whether to raise a
                            :py:class:`KeyError` if you can't store there

        Raises:
            KeyError: If someone else has a lease at this value, and ``error``
                          is ``True``
        """
        meta = self.metadata.get(key, None)
        if ((not meta) or
                (meta.owner == new_meta.owner) or
                (meta.timestamp < getUTC() - 3600) or
                (meta.timestamp == new_meta.timestamp and
                    meta.owner > new_meta.owner) or
                (meta.timestamp < new_meta.timestamp and
                    not self.__leasing)):
            if new_data not in ('', b''):
                self.metadata[key] = new_meta
                self.data[key] = new_data
            else:
                del self.data[key]
                del self.metadata[key]
        elif error:
            raise KeyError("You don't have permission to change this yet")

    def _send_handshake_response(self, handler):
        """Shortcut method to send a handshake response. This method is
        extracted from :py:meth:`.__handle_handshake` in order to allow
        cleaner inheritence from :py:class:`py2p.sync.sync_socket`
        """
        super(sync_socket, self)._send_handshake_response(handler)
        for key in self:
            meta = self.metadata[key]
            handler.send(flags.whisper, flags.store, key, self[key],
                         meta.owner, to_base_58(meta.timestamp))

    def __handle_store(self, msg, handler):
        """This callback is used to deal with data storage signals. Its two
        primary jobs are:

             - store data in a given key
             - delete data in a given key

             Args:
                msg:        A :py:class:`~py2p.base.message`
                handler:    A :py:class:`~py2p.mesh.mesh_connection`

             Returns:
                Either ``True`` or ``None``
        """
        packets = msg.packets
        if packets[0] == flags.store:
            meta = metatuple(msg.sender, msg.time)
            if len(packets) == 5:
                if self.data.get(packets[1]):
                    return
                meta = metatuple(packets[3], from_base_58(packets[4]))
            self.__store(packets[1], packets[2], meta, error=False)
            return True

    def __setitem__(self, key, data):
        """Updates the value at a given key.

        Args:
            key:    The key that you wish to update. Must be a :py:class:`str`
                        or :py:class:`bytes`-like object
            value:  The value you wish to put at this key. Must be a
                        :py:class:`str` or :py:class:`bytes`-like object

        Raises:
            KeyError: If you do not have the lease for this slot. Lease is
                          given automatically for one hour if the slot is open.
        """
        new_meta = metatuple(self.id, getUTC())
        key = sanitize_packet(key)
        data = sanitize_packet(data)
        self.__store(key, data, new_meta)
        if data in ('', b''):
            self.send(key, '', type=flags.store)
        else:
            self.send(key, data, type=flags.store)

    @inherit_doc(__setitem__)
    def set(self, key, data):
        self.__setitem__(key, data)

    def update(self, update_dict):
        """Equivalent to :py:meth:`dict.update`

        This calls :py:meth:`.sync_socket.__setitem__` for each key/value
        pair in the given dictionary.

        Args:
            update_dict: A :py:class:`dict`-like object to extract key/value
                             pairs from. Key and value be a :py:class:`str`
                             or :py:class:`bytes`-like object

        Raises:
            KeyError: If you do not have the lease for this slot. Lease is
                          given automatically for one hour if the slot is open.
        """
        for key in update_dict:
            value = update_dict[key]
            self.__setitem__(key, value)

    def __getitem__(self, key):
        """Looks up the value at a given key.

        Args:
            key: The key that you wish to check. Must be a :py:class:`str` or
                    :py:class:`bytes`-like object

        Returns:
            The value at said key

        Raises:
            KeyError: If there is no value assigned at that key
        """
        key = sanitize_packet(key)
        return self.data[key]

    def get(self, key, ifError=None):
        """Retrieves the value at a given key.

        Args:
            key:     The key that you wish to check. Must be a :py:class:`str` or
                        :py:class:`bytes`-like object
            ifError: The value you wish to return on exception (default: ``None``)

        Returns:
            The value at said key, or the value at ifError if there's an Exception
        """
        key = sanitize_packet(key)
        return self.data.get(key, ifError)

    def __len__(self):
        return len(self.data)

    def __delitem__(self, key):
        self[key] = ''

    def keys(self):
        """Returns an iterator of the underlying :py:class:`dict`s keys"""
        if hasattr(self.data, 'iterkeys'):
            return (key for key in self.data.keys() if key in self.data)
        return (key for key in tuple(self.data.keys()) if key in self.data)

    @inherit_doc(keys)
    def __iter__(self):
        return self.keys()

    def values(self):
        """Returns an iterator of the underlying :py:class:`dict`s values"""
        return (self[key] for key in self.keys())

    def items(self):
        """Returns an iterator of the underlying :py:class:`dict`s items"""
        return ((key, self[key]) for key in self.keys())

    def pop(self, key, *args):
        """Returns a value, with the side effect of deleting that association

        Args:
            Key:        The key you wish to look up. Must be a :py:class:`str`
                            or :py:class:`bytes`-like object
            ifError:    The value you wish to return on Exception
                            (default: raise an Exception)

        Returns:
            The value of the supplied key, or ``ifError``

        Raises:
            KeyError:       If the key does not have an associated value
        """
        if len(args):
            ret = self.get(key, args[0])
            if ret != args[0]:
                del self[key]
        else:
            ret = self[key]
            del self[key]
        return ret

    def popitem(self):
        """Returns an association, with the side effect of deleting that
        association

        Returns:
            An arbitrary association
        """
        key, value = next(self.items())
        del self[key]
        return (key, value)

    def copy(self):
        """Returns a :py:class:`dict` copy of this synchronized hash table"""
        return self.data.copy()
