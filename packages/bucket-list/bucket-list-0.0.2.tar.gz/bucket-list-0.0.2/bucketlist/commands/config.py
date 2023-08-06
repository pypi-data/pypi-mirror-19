import os
import json
import getopt

from bucketlist import appconfig, speedyio
from bucketlist.errors import BucketlistError
from bucketlist.providers.wunderlist import Wunderlist


def render_config(config, title=None):
    for key, value in config:
        speedyio.plain_print("{}.{}: {}".format(title, key, value))


class ConfigCommand:
    __command_name__ = 'config'

    def execute(self, argv):
        optlist, args = getopt.getopt(argv, '', ['set=', 'get=', 'get-all'])
        optmap = {
            opt[0].lstrip('-'):opt[1]
            for opt in optlist
        }

        if 'set' in optmap:
            if len(args) == 0:
                raise BucketlistError("Value for config '{}' not provided.".format(optmap['set']))

            config_name = optmap['set']
            tokens = config_name.split('.')

            if len(tokens) != 2:
                raise BucketlistError("Invalid config '{}'.".format(optmap['set']))

            appconfig.put(tokens[0], tokens[1], args[0])

        elif 'get-all' in optmap:
            config_map = appconfig.__class__.get_config_map(appconfig.get('provider', 'name'))
            for section, m in config_map.items():
                render_config(appconfig.get_all(section), title=section)

        elif 'get' in optmap:
            config_name = optmap['get']

            tokens = config_name.split('.')
            if len(tokens) != 2:
                raise BucketlistError("Invalid config '{}'".format(config_name))

            speedyio.plain_print(appconfig.get(tokens[0], tokens[1]))
