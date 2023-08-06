import os
import re

import routekit.router


def read_rt_tables():
    """
    Returns a dict of contents of rt_tables file in [ name, id ] format for easy name-to-id lookups
    Just like the iproute2 toolset does, will overwrite duplicate entries as they are read from disk
    :return: rt_tables dict
    """

    rt_tables = {}

    rtd_path = '/etc/iproute2/rt_tables.d'

    files = ['/etc/iproute2/rt_tables']

    def parse_id_name(line):
        """Parses a line of rt_tables entries, strips comments and newlines"""
        if not line.startswith(('#', '\n')):
            return re.split('[\s|\t]+', line.strip('\n'))

    def read_rt_tables_file(filename=None):
        """Parse every line of an rt_tables file and write to rt_tables dict"""
        if os.path.isfile(filename):
            with open(filename, 'r') as rtt:
                for l in rtt.readlines():
                    p = parse_id_name(l)
                    if p is not None:
                        rt_tables[p[1]] = int(p[0])

    # Find all files that end in '.conf. in rt_tables.d/ and append absolute paths to files list
    if os.path.isdir(rtd_path):
        rtd_files = [os.path.join(rtd_path, f) for f in os.listdir(rtd_path) if f.endswith('.conf')]
        files.extend(rtd_files)

    # Parse rt_tables and every file found in rt_tables.d/
    for file in files:
        read_rt_tables_file(file)

    return rt_tables


def route_delta(current, desired):
    """
    Given a set of desired routes and the current state of the system,
    generate 2 lists of actions to be taken to achieve the desired state.
    :param current: Dict of tables in the system
    :param desired: Dict of tables in the configuration (desired state)
    :return: (deploy, delete)
    """
    deploy = []
    delete = []

    # Deploy Routes
    # Iterate over all desired routes and find a 'current' counterpart
    for (kt_desired, t_desired) in desired.items():
        if kt_desired in current:
            for r_desired in t_desired:
                # Search for routes that exactly match the intended ones and ignore them
                # Since we're using Netlink route replace, this is all we need to filter
                full_search = current[kt_desired].find(r_desired)
                if full_search is None:
                    deploy.append(r_desired.action_tuple(tableid=t_desired.id))
        else:
            # Fast path when table is missing completely, no searches required
            for r_desired in t_desired:
                deploy.append(r_desired.action_tuple(tableid=t_desired.id))

    # Delete Routes
    # Look for missing counterparts in the intended config and issue a delete for them
    for (kt_current, t_current) in current.items():
        if kt_current in desired:
            # Table already in system, compare individual rules by destination hash
            # Comparing destination hashes prevents deleting routes that are going to be replaced,
            # eg. when modifying a default route. (same dsthash but other fullhash)
            for r_current in t_current:
                dst_search = desired[kt_current].find_dsthash(r_current)
                if dst_search is None:
                    delete.append(r_current.action_tuple(tableid=t_current.id))
        else:
            # Table not in system, remove all entries except for those on blacklist
            if t_current.id not in routekit.router.remove_ignore_tables:
                for r_current in t_current:
                    delete.append(r_current.action_tuple(tableid=t_current.id))

    # Filter results that have 'preserve' set as the hop
    deploy = [r for r in deploy if r.hop != 'preserve']
    delete = [r for r in delete if r.hop != 'preserve']

    return deploy, delete
