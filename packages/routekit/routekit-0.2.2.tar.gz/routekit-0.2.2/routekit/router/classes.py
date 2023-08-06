import netaddr
import collections

from .util import *


RouteAction = collections.namedtuple('RouteAction', 'table dst prefix hop')

class Table(collections.Set):

    def __init__(self, id=None, name=None):
        self._routes = []
        self._defroute = False
        self._id = None
        self._name = None

        self.id = id
        self.name = name

    def __iter__(self):
        return iter(self.routes)

    def __contains__(self, item):
        return item in self.routes

    def __len__(self):
        return len(self.routes)

    def __str__(self):
        return repr("<Table '{}', id {}, {} routes>".
                    format(self.name, self.id, len(self.routes)))

    def find(self, item):
        """
        Route membership test
        :param item: Route to look up
        :return: Route or None
        """
        return item if item in self._routes else None

    def find_dsthash(self, item):
        """
        Helper method to look up a route in the table by its destination hash
        :param item: Route to look up
        :return: First matching route or None
        """
        try:
            return next(r for r in self._routes if r.dst_equals(item))
        except StopIteration:
            return None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if id is not None:
            self._id = int(id)

            # Look up a name from rt_tables if _name is not set
            if self._name is None:
                tbl_name = table_id_name(id)
                self._name = 'unknown' if tbl_name is None else tbl_name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if name is not None:
            self._name = name

            # Look up the id from rt_tables if _id not set
            if self._id is None:
                self._id = table_name_id(name)

    @property
    def routes(self):
        return self._routes

    @routes.setter
    def routes(self, iterable):
        for value in iterable:
            if type(value) is not Route:
                raise RouterException('Cannot add non-Route object to table')

            # Allow only a single default route per Table
            # TODO: Configuration format for iproute2 metric support
            if value.default and self._defroute is False:
                self._defroute = True
            elif value.default and self._defroute is True:
                raise RouterException('Cannot add multiple default routes to table')

            if self.find_dsthash(value) is None:
                self._routes.append(value)


class Route(object):

    def __init__(self, dst='', hop=''):
        self._dsthash = None

        self._dst = None
        self._hop = None

        self._prefixlen = None
        self._version = None

        self.dst = dst
        self.hop = hop

    def __str__(self):
        return repr("<Route '{}/{}' via '{}', default {}>"
                    .format(self.dst, self.prefixlen, self.hop, self.default))

    def __hash__(self):
        return hash((self._dst, self._prefixlen, self._hop))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def _run_dsthash(self):
        self._dsthash = hash((self._dst, self._prefixlen))

    def dst_equals(self, other):
        return self._dsthash == other._dsthash

    def action_tuple(self, tableid=None):
        """
        Converts a Route object into an action tuple we can easily feed into pyroute2.
        Automatically transforms 'default' dst into 0.0.0.0
        :param tableid: numeric id of the table to act upon
        :return: RouteAction tuple
        """

        if tableid is None:
            raise RouterException('route_action_tuple expects tableid')

        dst = '0.0.0.0' if self.dst == 'default' else self.dst

        return RouteAction(table=tableid, dst=dst, prefix=self.prefixlen, hop=self.hop)

    @property
    def default(self):
        return True if self.dst == 'default' else False

    @property
    def prefixlen(self):
        return self._prefixlen

    @property
    def dst(self):
        return self._dst

    @dst.setter
    def dst(self, value):
        self._dst = value if value == 'default' else str(netaddr.IPNetwork(value).ip)
        self._prefixlen = 0 if value == 'default' else netaddr.IPNetwork(value).prefixlen
        self._run_dsthash()

    @property
    def hop(self):
        return self._hop

    @hop.setter
    def hop(self, value):
        self._hop = value

        if value != 'preserve':
            self._version = netaddr.IPAddress(value).version


class RouterException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ConfigException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
