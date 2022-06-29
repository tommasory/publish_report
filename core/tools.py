import json

def read_json_file(path : str):
    '''Method to load JSON file
    :param path: (str): File path.
    :return: Boolean, JSON file in dictionary format
    '''
    data = {}
    try:
        with open(path) as file:
            data = json.load(file)
        return True, data
    except FileNotFoundError as err:
        return False, err