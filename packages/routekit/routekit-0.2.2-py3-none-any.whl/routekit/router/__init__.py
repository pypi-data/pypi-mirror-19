# Pull all module objects into 'router' namespace
from .util import *
from .classes import *
from .core import *


# Turn on debug mode for package
debug = False

# Don't touch or display these tables, ever
global_ignore_tables = [0]

# Do not consider these tables for removal when missing from config
remove_ignore_tables = [254]

# Table name-to-id mappings defined in rt_tables(.d)
rt_tables = {'main': 254}

# Python3 hash merging, 3.4 compat
rt_tables = merge_dicts(rt_tables, read_rt_tables())
