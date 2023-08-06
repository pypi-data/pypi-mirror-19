import os
import json
import configparser

from bucketlist.errors import BucketlistError
from bucketlist.providers import get_provider_config


class Config:
    folder_name = '.bucket-list'
    config_filename = 'config'

    def __init__(self):
        self.config_folder_path = os.path.join(os.environ.get('HOME'),
                                               Config.folder_name)
        self.config_filepath = os.path.join(self.config_folder_path,
                                            Config.config_filename)

        self.allconfig = configparser.ConfigParser()

        if not os.path.exists(self.config_folder_path):
            os.makedirs(self.config_folder_path)

        if not os.path.exists(self.config_filepath):
            for section_name in Config.get_config_map(None).keys():
                self.allconfig.add_section(section_name)

            with open(self.config_filepath, 'w') as config_file:
                self.allconfig.write(config_file)

            self.put('provider', 'name', 'wunderlist')
            self.put('io', 'mode', 'interactive')
            self.put('logging', 'level', 'error')
            self.put('logging', 'file', os.path.join(self.config_folder_path, 'bucketlist.log'))

        self.allconfig.read(self.config_filepath)


    @staticmethod
    def get_config_map(provider_name):
        provider_config = get_provider_config(provider_name)
        if provider_config is None:
            raise BucketlistError("{} provider is not supported yet.".format(provider_name))

        return {
            'provider': ['name'],
            'io': ['mode'],
            'logging': ['level', 'file'],
            'provider_config': provider_config
        }

    def get(self, *args, **kwargs):
        if len(args) == 0:
            raise BucketlistError("At least 1 argument is required")

        try:
            provider_name = self.allconfig.get('provider', 'name')
        except configparser.NoOptionError as e:
            provider_name = None

        config_map = Config.get_config_map(provider_name)

        if args[0] not in config_map:
            raise BucketlistError("Invalid config {}".format(args[0]))

        if args[1] not in config_map[args[0]]:
            raise BucketlistError("Invalid config {} under {}".format(args[1], args[0]))

        try:
            return self.allconfig.get(*args, **kwargs)
        except configparser.NoOptionError as e:
            return None

    def get_all(self, section):
        return self.allconfig.items(section)

    def put(self, *args):
        if len(args) == 1:
            raise BucketlistError("At least 2 arguments are required")

        if args[0] == 'provider' and args[1] == 'name':
            raise BucketlistError("You cannot change the provider like this.")

        try:
            provider_name = self.allconfig.get('provider', 'name')
        except configparser.NoOptionError as e:
            provider_name = None

        config_map = Config.get_config_map(provider_name)

        if args[0] not in config_map:
            raise BucketlistError("Invalid config {}".format(args[0]))

        if args[1] not in config_map[args[0]]:
            raise BucketlistError("Invalid config {} under {}".format(args[1], args[0]))

        self.allconfig.set(*args)

        with open(self.config_filepath, 'w') as config_file:
            self.allconfig.write(config_file)
