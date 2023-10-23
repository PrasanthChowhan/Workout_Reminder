import json

def get_nested_dict_value(d, key_to_find):
    """
    Recursively search for a key in a nested dictionary and return its value.

    Args:
        d (dict): The nested dictionary to search.
        key_to_find (str): The key to search for.

    Returns:
        Any: The value associated with the specified key, or None if the key is not found.
    """

    for key, value in d.items():
        if key == key_to_find:
            return value
        elif isinstance(value, dict):
            result = get_nested_dict_value(value, key_to_find)
            if result is not None:
                return result

    return None  # Key not found in the nested dictionary
def open_json_file(path):
    """
    Load existing JSON data from 'data.json' file.

    Returns:
        dict: A dictionary containing the loaded JSON data.

    If the 'data.json' file is not found, an empty dictionary is returned.
    """
    # json_location = os.path.join(self.current_folder.get(),JSON_NAME)
    json_location = path
    try:
        with open(json_location, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}


if __name__ == '__main__':
    dict = open_json_file('data\exersises.json')
    for key, value in dict['Calisthenics']['Exercises']['Chest'].items():
        print(key)
