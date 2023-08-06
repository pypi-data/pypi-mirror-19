import getopt

from bucketlist import speedyio
from bucketlist.providers import Provider


class MarkCommand:
    __command_name__ = 'mark'

    def __init__(self):
        pass

    def execute(self, argv):
        optlist, args = getopt.getopt(argv, 'c:')
        optmap = {
            opt[0].lstrip('-'):opt[1]
            for opt in optlist
        }

        if 'c' not in optmap:
            optmap['c'] = speedyio.askfor(str, 'category', empty_allowed=False)

        bucketlist_items = Provider.get(optmap['c'], completed=False)
        options = [speedyio.Item(bucketlist_item.message, bucketlist_item.id) for bucketlist_item in bucketlist_items]

        if not options:
            return

        bucketlist_item_id = speedyio.chooseone(options, message="Mark as complete")
        bucketlist_item = Provider.mark_as_complete(bucketlist_item_id)

        speedyio.success("Marked as completed \u2713")
