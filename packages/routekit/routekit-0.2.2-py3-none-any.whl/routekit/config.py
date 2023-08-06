import errno
import yaml
import os

from time import time
from pyroute2 import iproute, netlink

import routekit


class RKConfig(object):

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, debug=False):
        if debug is not self._debug:
            self._debug = debug

            # Set debug flags on modules
            routekit.router.debug = debug

            print("Toggled debug logging {}".format('on' if debug else 'off'))

    def __init__(self):
        self.tables = {}
        self.rules = []

        self._debug = False

    def __str__(self):
        return repr("<RKConfig with {} tables and {} rules>"
                    .format(len(self.tables), len(self.rules)))


def first_found_config(config_paths, filename):
    """
    Returns a dictionary of the first-found configuration as first return value
    Returns the path of the configuration that was selected as second return value
    Returns None, None if no configuration files were found
    The first return value can be None if the file is empty (or broken)
    :return: (dict, string) or (None, None)
    """

    # Wrap input parameter in a list in case it is a string
    if isinstance(config_paths, str):
        config_paths = [config_paths]

    for abs_path in [os.path.join(p, filename) for p in config_paths]:
        if routekit.router.debug is True:
            routekit.click_print('Looking for configuration in {}'.format(abs_path))

        try:
            with open(abs_path) as cfgfile:
                cfg = yaml.load(cfgfile)

            if routekit.router.debug is True:
                routekit.click_green('Found configuration in {}'.format(path))

            return cfg, abs_path

        except IOError:
            if routekit.router.debug:
                routekit.click_yellow('{} not found.'.format(path))

    return None, None


def read_config_routes(consul, config):
    """
    Reads one of two route configuration formats.
    Builds a router object tree in a RKConfig object.
    :return: RKConfig
    """

    rtables = {}

    if routekit.router.debug:
        print('Reading routes in read_config_routes()')

    if not isinstance(config, dict):
        raise routekit.router.ConfigException('Config object is not a dictionary, aborting configuration parsing.')

    # Ensure 'routes' element exists in configuration
    if config.get('routes') is None:
        raise routekit.router.ConfigException('No route definition found in configuration, aborting configuration parsing.')

    # Route list format
    # Insert routes into main routing table
    if isinstance(config['routes'], list):
        if routekit.router.debug:
            print('Found list in route config file, adding routes to default table (254):')

        tbl = routekit.router.Table(id=254)
        tbl.routes = routekit.router.parse_routes(config['routes'])
        rtables[tbl.id] = tbl

    # Route dict format
    # Build tree of routing tables and entries
    elif isinstance(config['routes'], dict):
        if routekit.router.debug:
            print('Found dict object in route config file')

        # iterate over routing tables in `routes`
        for ltable, lroutes in config['routes'].items():

            # Allocate table according to type of input value
            if type(ltable) is str:
                tbl = routekit.router.Table(name=ltable)
            elif type(ltable) is int:
                tbl = routekit.router.Table(id=ltable)

            # Insert routes and append to list
            tbl.routes = routekit.router.parse_routes(lroutes)
            rtables[tbl.id] = tbl
    else:
        raise routekit.router.ConfigException('Unrecognized route format, use list or dict')

    return rtables


def read_system_routes(ipr):
    """
    Returns a list of routing tables and routes currently in the kernel.
    :return: list
    """

    rtables = {}

    routes = ipr.get_routes(family=iproute.AF_INET)

    for r in routes:
        rta_len = r.get('dst_len')
        rta_dst = r.get_attr('RTA_DST')
        rta_gw = r.get_attr('RTA_GATEWAY')
        rta_table = r.get_attr('RTA_TABLE')

        if rta_dst is None:
            # None entries in destination field are default gateways
            dst = 'default'
        else:
            # Assemble a net/prefix string
            dst = "{}/{}".format(rta_dst, rta_len)

        if rta_table not in routekit.router.global_ignore_tables and rta_gw is not None:
            # Initialize table if it doesn't exist
            if rtables.get(rta_table) is None:
                rtables[rta_table] = routekit.router.Table(id=rta_table)

            rtables[rta_table].routes.append(routekit.router.Route(dst=dst, hop=rta_gw))

    return rtables


def apply_routes(ipr, deploy, delete):
    """
    Execute all RouteActions specified in deploy and delete
    Raises exception when inner exception is unhandled.
    Returns True on success
    :param deploy: list of routes to deploy onto the system
    :param delete: list of routes to delete
    :return: None
    """

    success = True

    for r in deploy:
        try:
            if routekit.router.debug:
                print('Replacing route {}'.format(r))
            ipr.route('replace', table=r.table, dst=r.dst, mask=r.prefix, gateway=r.hop)
        except netlink.NetlinkError as e:
            success = False

            if getattr(e, 'code', 0) == errno.EPERM:
                routekit.eprint('Netlink permission error encountered while replacing route {}. Are you root?'.format(r))
            elif getattr(e, 'code', 0) == errno.ENETUNREACH:
                routekit.eprint('Cannot add {}/{} via {}, hop not directly connected'.format(r.dst, r.prefix, r.hop))
            else:
                routekit.eprint('Unexpected Netlink error while replacing route {}: {}'.format(r, e))

    for r in delete:
        try:
            if routekit.router.debug:
                print('Deleting route {}'.format(r))
            ipr.route('delete', table=r.table, dst=r.dst, mask=r.prefix, gateway=r.hop)
        except netlink.NetlinkError as e:
            success = False

            if getattr(e, 'code', 0) == errno.EPERM:
                routekit.eprint('Netlink permission error encountered while deleting route {}. Are you root?'.format(r))
            else:
                routekit.eprint('Unexpected Netlink error while deleting route {}: {}'.format(r, e))

    return success
