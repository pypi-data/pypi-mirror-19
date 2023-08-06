from bucketlist import appconfig
from bucketlist.decorators import dumptime
from bucketlist.errors import BucketlistError
from bucketlist.entities import BucketlistItem
from bucketlist.providers.wunderlist import wunderlist_api
from bucketlist.providers.wunderlist import WRequests as wrequests


class Wunderlist:
    @staticmethod
    @dumptime
    def add(category, message):
        folder_name = appconfig.get('provider_config', 'folder-name')

        try:
            folder = wunderlist_api.get_folder(folder_name)
        except BucketlistError:
            wlist = wunderlist_api.create_list(None, category)
            folder = wunderlist_api.create_folder(folder_name, [wlist.get('id')])

        try:
            wlist = wunderlist_api.get_list(folder, category)
        except BucketlistError:
            wlist = wunderlist_api.create_list(folder, category)

        task = wunderlist_api.create_task(wlist, message)
        return BucketlistItem(task['id'], task['title'], task['completed'])

    @staticmethod
    @dumptime
    def get(category, completed=False):
        folder_name = appconfig.get('provider_config', 'folder-name')

        try:
            folder = wunderlist_api.get_folder(folder_name)
        except BucketlistError:
            wlist = wunderlist_api.create_list(None, category)
            folder = wunderlist_api.create_folder(folder_name, [wlist.get('id')])

        wlist = wunderlist_api.get_list(folder, category)
        tasks = wunderlist_api.get_tasks(wlist, completed=completed)

        return [BucketlistItem(task['id'], task['title'], task['completed']) for task in tasks]

    @staticmethod
    @dumptime
    def mark_as_complete(bucketlist_item_id):
        task = wunderlist_api.update_task(bucketlist_item_id, completed=True)
        return BucketlistItem(task['id'], task['title'], task['completed'])
