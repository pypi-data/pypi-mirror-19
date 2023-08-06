import getopt
from bucketlist import speedyio
from bucketlist.providers import get_current_provider


class AddCommand:
    __command_name__ = 'add'

    def __init__(self):
        pass

    def execute(self, argv):
        Provider = get_current_provider()

        optlist, args = getopt.getopt(argv, 'm:c:')
        optmap = {
            opt[0].lstrip('-'):opt[1]
            for opt in optlist
        }

        if 'c' not in optmap:
            optmap['c'] = speedyio.askfor('category', empty_allowed=False)

        if 'm' not in optmap:
            optmap['m'] = speedyio.askfor('message', empty_allowed=False)

        bucketlist_item = Provider.add(optmap['c'], optmap['m'])
        speedyio.success("'{}' added successfully \u2713".format(bucketlist_item.message))
