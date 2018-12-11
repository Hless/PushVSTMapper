''' File extensions '''
import os
import json
from .config import APP_DIR
from .memoize import cached

def ensure_path(path):
    ''' Ensure that given path exists, or create it '''
    os.makedirs(os.path.dirname(path), exist_ok=True)


def config_path(device, name):
    return os.path.join(APP_DIR, device, name + '.json')

@cached("name", namespace="{device}")
def load_from_json(device, name):
    file_path = config_path(device, name)

    with open(file_path) as file_handle:
        return json.load(file_handle)

def save_as_json(device, name, data):
    '''
    Save as json
    device: Device name (str)
    name: File name (str)
    data: Serializable object (simple type, list, dict)
    '''

    file_path = os.path.join(APP_DIR, device, name + '.json')
    ensure_path(file_path)

    with open(file_path, 'w') as file_handle:
        json.dump(data, file_handle)
