from bucketlist import appconfig
from bucketlist.decorators import dumptime
from bucketlist.errors import BucketlistError
from bucketlist.entities import BucketlistItem, BucketlistCategory
from bucketlist.providers.wunderlist import wunderlist_api
from bucketlist.providers.wunderlist import WRequests as wrequests


class Wunderlist:
    @staticmethod
    @dumptime
    def add(category, message):
        folder_name = appconfig.get('provider_config', 'folder-name')
        folder = wunderlist_api.get_folder(folder_name)

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
        folder = wunderlist_api.get_folder(folder_name)

        wlist = wunderlist_api.get_list(folder, category)
        tasks = wunderlist_api.get_tasks(wlist, completed=completed)

        return [BucketlistItem(task['id'], task['title'], task['completed']) for task in tasks]

    @staticmethod
    @dumptime
    def get_categories():
        folder_name = appconfig.get('provider_config', 'folder-name')
        folder = wunderlist_api.get_folder(folder_name)

        return [BucketlistCategory(l.get('title')) for l in wunderlist_api.get_lists(folder)]

    @staticmethod
    @dumptime
    def get_category(category_name):
        categories = Wunderlist.get_categories()
        for category in categories:
            if category.name == category_name:
                return category
        return None

    @staticmethod
    @dumptime
    def create_category(category_name):
        folder_name = appconfig.get('provider_config', 'folder-name')
        folder = wunderlist_api.get_folder(folder_name)

        try:
            wlist = wunderlist_api.get_list(folder, category_name)
        except BucketlistError:
            wlist = wunderlist_api.create_list(folder, category_name)

        return BucketlistCategory(wlist.get('title'))

    @staticmethod
    @dumptime
    def mark_as_complete(bucketlist_item_id):
        task = wunderlist_api.update_task(bucketlist_item_id, completed=True)
        return BucketlistItem(task['id'], task['title'], task['completed'])

    @staticmethod
    @dumptime
    def get_item_by_id(bucketlist_item_id):
        task = wunderlist_api.get_task(bucketlist_item_id)
        if task is None:
            return None
        return BucketlistItem(task['id'], task['title'], task['completed'])

    @staticmethod
    @dumptime
    def clean():
        folder_name = appconfig.get('provider_config', 'folder-name')
        folder = wunderlist_api.get_folder(folder_name)

        wlists = wunderlist_api.get_lists(folder)
        for l in wlists:
            wunderlist_api.delete_list(l['id'])

    @staticmethod
    @dumptime
    def init():
        folder_name = appconfig.get('provider_config', 'folder-name')
        try:
            folder = wunderlist_api.get_folder(folder_name)
        except BucketlistError:
            wlist = wunderlist_api.create_dummy_list()
            folder = wunderlist_api.create_folder(folder_name, [wlist.get('id')])
