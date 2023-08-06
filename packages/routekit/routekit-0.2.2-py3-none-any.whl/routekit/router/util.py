from collections import Counter
import socket
import hashlib
import netaddr

import routekit.router


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    Taken from http://stackoverflow.com/questions/38987
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def table_name_id(table_name):
    """
    Look up a table name's id from rt_tables. Generates one deterministically if no match was found.
    :param table_name: table name to get id for
    :return: int
    """

    rt_lookup = routekit.router.rt_tables.get(table_name, None)

    if rt_lookup is None:
        m = hashlib.md5(table_name.encode('utf-8'))
        return int(m.hexdigest()[:8], 16)
    else:
        return int(rt_lookup)


def table_id_name(table_id):
    """
    Look up the first name in rt_tables that has the given id associated with it.
    :param table_id: id of table to look up
    :return: str
    """

    try:
        return next(name for name, id in routekit.router.rt_tables.items() if id == int(table_id))
    except StopIteration:
        return None


def check_route(route):
    """
    Sanity check of route tuples.
    Returns True when default gateway, throws exception on error
    :param route: tuple of (destination, hop)
    :return: True
    """
    defgw = False

    if routekit.router.debug: print('check_route: checking {}'.format(route))

    if not isinstance(route, list) and not isinstance(route, tuple):
        raise routekit.router.RouterException('Expecting tuple for route entry "{}"'.format(route))

    if len(route) < 2:
        raise routekit.router.RouterException('Need at least 2 members in route entry "{}"'.format(route))

    # Destination network
    # Supports one magic value, 'default'
    if route[0] == 'default':
        defgw = True
    else:
        # Entry is not a default gateway
        # Try to create an IPNetwork object out of the destination
        try:
            if routekit.router.debug:
                print('check_route: applying netaddr transformations to {}'.format(route[0]))

            net = netaddr.IPNetwork(route[0])

            # Compare input value (without prefix) to the parsed IPNetwork network address to make sure
            # the input value was a network address (this passes for /32 etc.)
            if net.ip != net.network:
                raise routekit.router.RouterException('Destination address {} must be a valid network'.format(route[0]))

        except netaddr.core.AddrFormatError as e:
            raise routekit.router.RouterException('Caught netaddr exception: {}'.format(e))

    # Validate nexthop address
    if route[1] != 'preserve':
        netaddr.IPAddress(route[1])

    return defgw


def parse_routes(routes):
    """
    Transforms a list of routing table entries into a list
    of Route objects and performs a sanity check.
    :param routes: list of routes in tuple format
    :return: list of routes in Route() object format
    """
    obj_routes = []

    for r in routes:
        check_route(r)
        obj_routes.append(routekit.router.Route(r[0], r[1]))

    return obj_routes


def count_tables(ipr, family=socket.AF_UNSPEC):
    """
    Counts the routes in all tables in the system.
    Filters AF_UNSPEC family by default
    :param ipr: IPRoute instance
    :param family: Defaults to socket.AF_UNSPEC
    :return: Counter [tableid, count]
    """
    routes = ipr.get_routes(family=family)

    cnt = Counter()

    for r in routes:
        cnt[r.get('table')] += 1

    return cnt
