import sys
from bucketlist import appconfig, speedyio
from bucketlist.providers.wunderlist.wunderlist import Wunderlist


provider = appconfig.get('provider', 'name')

if provider is None:
    Provider = None
else:
    Provider = {
        'wunderlist': Wunderlist
    }.get(provider)


if Provider is None:
    speedyio.error("Provider is not set. Please check your config.")
    sys.exit(2)
