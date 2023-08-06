PROVIDER_CONFIGS = {
    'wunderlist': ['access-token', 'folder-name', 'client-id']
}


def get_provider_config(provider_name):
    return PROVIDER_CONFIGS.get(provider_name)

def get_supported_providers():
    return PROVIDER_CONFIGS.keys()
