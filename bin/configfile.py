# configfile.py --- parse the config file
#
# Currently supported

import yaml
import os.path
from collections import ChainMap

# List of places where the config files could be store,
# in order of priority: a file has priority over the files that follow it.
possibleconfigfiles = [os.path.expanduser("~/.yanki.yml"),
                       os.path.expanduser("~/.local/share/Yanki/config.yml"),
                       "/etc/yanki.conf"]

def globalConfig():
    """Returns a ChainMap with the global configuration options."""
    res = ChainMap({})

    for configfile in possibleconfigfiles:
        if os.path.exists(configfile) and os.path.isfile(configfile):
            with open(configfile, 'r') as ifile:
                res.maps.append(yaml.load(ifile))

    return res
