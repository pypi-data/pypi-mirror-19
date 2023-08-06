import sys
import logging

from bucketlist import configio
from bucketlist.errors import BucketlistError


appconfig = configio.Config()

if not appconfig.config_exists():
    appconfig.init()

# Validate provider name
try:
    appconfig.get('provider', 'name')
except BucketlistError as e:
    print("Unsupported provider")
    print("Only following provider(s) are spported.")
    for provider_name in configio.get_supported_providers():
        print(" - {}".format(provider_name))
    sys.exit(2)

io = appconfig.get('io', 'mode') or 'basic'
if io == 'basic':
    import speedyio.basic as speedyio
elif io == 'interactive':
    import speedyio.interactive as speedyio
else:
    import speedyio.basic as speedyio


logger = logging.getLogger(__name__)

def configure_logger(logger):
    logfile = appconfig.get('logging', 'file') or '/var/log/bucket-list.log'

    loglevel_map = {
        'error': logging.ERROR,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'critical': logging.CRITICAL
    }

    loglevel_str = appconfig.get('logging', 'level') or 'error'
    loglevel = loglevel_map.get(loglevel_str) or logging.ERROR
    logger.setLevel(loglevel)

    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger.addHandler(fh)


configure_logger(logger)
