import getopt

from bucketlist import speedyio
from bucketlist.utils import convert_int
from bucketlist.providers import Provider


class ViewCommand:
    __command_name__ = 'view'

    def __init__(self):
        pass

    def execute(self, argv):
        optlist, args = getopt.getopt(argv, 'c:', ['count=', 'completed'])
        optmap = {
            opt[0].lstrip('-'):opt[1]
            for opt in optlist
        }

        if 'c' not in optmap:
            optmap['c'] = speedyio.askfor(str, 'category', empty_allowed=False)

        if 'completed' in optmap:
            bucketlist_items = Provider.get(optmap['c'], completed=True)
        else:
            bucketlist_items = Provider.get(optmap['c'], completed=False)

        count = optmap.get('count')
        if count is not None:
            count = convert_int(count)
            if count is None:
                speedyio.error("'count' should be a number")
                return
            bucketlist_items = bucketlist_items[:count]

        for bucketlist_item in bucketlist_items:
            speedyio.bold_print(" - {}".format(bucketlist_item.message))
