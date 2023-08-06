import json
import getopt

from bucketlist import speedyio, appconfig, logger
from bucketlist.providers import get_current_provider
from bucketlist.errors import BucketlistError


class RestoreCommand:
    __command_name__ = 'restore'

    def __init__(self):
        pass

    def read(self, file_path):
        with open(file_path, 'r') as f:
            return json.loads(f.read())

    def execute(self, argv):
        Provider = get_current_provider()

        optlist, args = getopt.getopt(argv, '', ['file='])
        optmap = {
            opt[0].lstrip('-'):opt[1]
            for opt in optlist
        }

        if 'file' not in optmap:
            optmap['file'] = speedyio.askfor('file', empty_allowed=False)

        provider_name = appconfig.get('provider', 'name')
        backedup_data = self.read(optmap['file'])

        if backedup_data.get('provider') != provider_name:
            raise BucketlistError("Restore can only work with same providers {} and {} dont match".format(backedup_data.get('provider'), provider_name))

        try:
            Provider.clean()
            speedyio.info("Cleanup done")

            Provider.init()
            speedyio.info("Provider initialized")

            for category_name, items in backedup_data.get('data').items():
                speedyio.info("Restoring data for category {}".format(category_name))
                category = Provider.get_category(category_name)
                if category is None:
                    category = Provider.create_category(category_name)

                for item in items:
                    bucketlist_item = Provider.get_item_by_id(item['id'])
                    if bucketlist_item is None:
                        bucketlist_item = Provider.add(category.name, item['message'])

                    if bucketlist_item.is_completed == False and item['is_completed'] == True:
                        Provider.mark_as_complete(bucketlist_item.id)
        except BucketlistError as e:
            speedyio.error("Data restored failed from {}. Please clean up and try again.".format(optmap['file']))
            speedyio.error(e.description)
        except Exception as e:
            logger.exception(e)
            speedyio.error("Data restored failed from {}. Please clean up and try again.".format(optmap['file']))
        else:
            speedyio.success("Data restored from {}".format(optmap['file']))
