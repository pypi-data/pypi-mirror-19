from bucketlist import appconfig


class InitCommand:
    __command_name__ = 'init'

    def __init__(self):
        pass

    def execute(self, argv):
        if not appconfig.config_exists():
            appconfig.init()
