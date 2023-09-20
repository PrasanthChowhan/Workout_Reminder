import json
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