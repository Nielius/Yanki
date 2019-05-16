# configfile.py --- parse the config file
#
# For the currently supported options, see the readme.

import yaml
import os.path
from collections import ChainMap

# List of places where the config files could be store,
# in order of priority: a file has priority over the files that follow it.
possibleconfigfiles = [os.path.expanduser("~/.yanki.yml"),
                       os.path.expanduser("~/.local/share/Yanki/config.yml"),
                       "/etc/yanki.conf"]

def expandpath(path):
    """Expands a path using os.path.expandvars and os.path.expanduser. If the input
    is a list, assume it is a list of paths that need to be expanded and return
    the list of expanded paths.
"""
    if isinstance(path, list):
        return [expandpath(x) for x in path]
    else:
        return os.path.expanduser(os.path.expandvars(path))

def globalConfig():
    """Returns a ChainMap with the global configuration options."""
    res = ChainMap({})

    for configfile in possibleconfigfiles:
        if os.path.exists(configfile) and os.path.isfile(configfile):
            with open(configfile, 'r') as ifile:
                res.maps.append(yaml.load(ifile))

    # Expand the path options
    pathoptions = ['templateDirs', 'collection', 'ankisource']

    for k,v in filter(lambda kv: kv[0] in pathoptions, res.items() ):
        res[k] = expandpath(v)

    return res
