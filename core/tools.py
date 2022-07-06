import json
from datetime import datetime as dt

DATE = dt.today()

def message(text=""):
    print(f"[{DATE}] : "+text)

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

def write_json_file(path:str, data:dict):
    '''update a json file
    :param path: file path
    :param data: file data
    :return:
    '''
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
        return True, ""
    except FileNotFoundError as err:
        return False, err