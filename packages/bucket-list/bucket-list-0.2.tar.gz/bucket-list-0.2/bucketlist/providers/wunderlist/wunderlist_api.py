from bucketlist.errors import BucketlistError
from bucketlist.decorators import dumptime
from bucketlist.providers.wunderlist import WRequests


@dumptime
def get_folder(folder_name):
    folder_id = None

    all_folders = WRequests.get('https://a.wunderlist.com/api/v1/folders')
    for f in all_folders:
        if f.get('title') == folder_name:
            folder_id = f.get('id')
            break

    if folder_id is None:
        raise BucketlistError("Folder with name '{}' does not exist on Wunderlist".format(folder_name))

    return WRequests.get('https://a.wunderlist.com/api/v1/folders/{}'.format(folder_id))


@dumptime
def get_lists(folder):
    return [
        WRequests.get('https://a.wunderlist.com/api/v1/lists/{}'.format(list_id))
        for list_id in folder.get('list_ids')
    ]


@dumptime
def get_list(folder, list_name):
    lists = [l for l in get_lists(folder) if l.get('title') == list_name]
    if len(lists) > 0:
        return lists[0]

    raise BucketlistError("List with name '{}' does not exist on Wunderlist".format(list_name))


@dumptime
def get_tasks(wlist, completed=False):
    params = {
        'list_id': wlist.get('id'),
        'completed': completed
    }
    return WRequests.get('https://a.wunderlist.com/api/v1/tasks', params=params)


@dumptime
def get_task(task_id):
    return WRequests.get('https://a.wunderlist.com/api/v1/tasks/{}'.format(task_id))


@dumptime
def update_task(task_id, completed=None):
    task = get_task(task_id)

    payload = {
        'revision': task.get('revision'),
        'completed': completed == True
    }
    return WRequests.patch('https://a.wunderlist.com/api/v1/tasks/{}'.format(task_id), json=payload)


@dumptime
def create_folder(folder_name, list_ids):
    folder = WRequests.post('https://a.wunderlist.com/api/v1/folders', json={
        'title': folder_name,
        'list_ids': list_ids
    })
    return get_folder(folder_name)


@dumptime
def create_list(folder, list_name):
    wlist = WRequests.post('https://a.wunderlist.com/api/v1/lists', json={
        'title': list_name
    })
    if folder:
        resp = WRequests.patch('https://a.wunderlist.com/api/v1/folders/{}'.format(folder.get('id')), json={
            'list_ids': folder.get('list_ids') + [wlist.get('id')],
            'revision': folder.get('revision')
        })
    return wlist


@dumptime
def create_task(wlist, message):
    task = WRequests.post('https://a.wunderlist.com/api/v1/tasks', json={
        'list_id': wlist.get('id'),
        'title': message,
        'completed': False
    })
    return task
