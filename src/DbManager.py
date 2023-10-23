import sqlite3,os,pprint
import yaml


import random as rnd
# this is custom package will be present in learning respository
# from python_learned.Sqlite import SqliteDefs
from src.utils.SQLITE import SqliteDefs

from src.utils.constants import *

'''
What this module does 
 * Everything related to data
 * read settings.yaml file
 * use that as query to search table
 * return one exercise 

'''


class ConfigReader:
    def __init__(self, config_file_path=None):
        self.config_file_path = config_file_path

    def read_config_file(self) -> dict:
        """
        Read and parse the configuration file in YAML format.

        Returns:
            dict: A dictionary containing the parsed configuration data.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            yaml.YAMLError: If there is an error parsing the YAML file.
            ValueError: If the configuration data is invalid or empty.

        Returns an empty dictionary if errors occur during the process.
        """
        try:
            with open(self.config_file_path, 'r') as config_file:
                loaded_data = yaml.safe_load(config_file)
                if loaded_data is not None and isinstance(loaded_data, dict):
                    return loaded_data
                else:
                    raise ValueError("Invalid or empty configuration data in the YAML file.")
        except FileNotFoundError:
            print(f"Config file not found: {self.config_file_path}")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return {}  # Return an empty dictionary in case of errors

    def write_config_file(self, data: dict):
        """
        Write data to the configuration file in YAML format.
        Args:
            data (dict): The data to be written to the file.
        """
        with open(self.config_file_path, 'a') as config_file:
            yaml.dump(data, config_file,
                      default_flow_style=False, sort_keys=True,indent=4)
            print('done writing configuration')

    def update_or_create_yaml_file(self,file_path, data_to_update):
        """
        Update a YAML file with key-value pairs or create the file if it doesn't exist.

        Args:
            file_path (str): The path to the YAML file.
            data_to_update (dict or str): A dictionary of key-value pairs to update or a single key (str).
                If a single key is provided, it will be updated with an empty string.

        Returns:
            bool: True if the update was successful, False if there was an error.
        """
        try:
            # Check if the file exists, and if not, create it
            if not os.path.exists(file_path):
                with open(file_path, 'w') as new_file:
                    new_file.write('')  # Create an empty file

            # Read the existing YAML data
            with open(file_path, 'r') as file:
                existing_data = yaml.safe_load(file) or {}

            if isinstance(data_to_update, dict):
                # If data_to_update is a dictionary, update the existing data with its contents
                existing_data.update(data_to_update)
            elif isinstance(data_to_update, str):
                # If data_to_update is a string, treat it as a single key and update it with an empty string
                existing_data[data_to_update] = ''

            # Write the updated data back to the file
            with open(file_path, 'w') as file:
                yaml.dump(existing_data, file, default_flow_style=False)

            return True  # Successful update

        except Exception as e:
            print(f"Error updating or creating YAML file: {e}")
            return False  # Error occurred during update or creation

    


    # def update_or_create_yaml_file(file_path, key, new_value):
    #     """
    #     Update a value in a YAML file or create the file if it doesn't exist.

    #     Args:
    #         file_path (str): The path to the YAML file.
    #         key (str): The key to update in the YAML data.
    #         new_value: The new value to set for the specified key.

    #     Returns:
    #         bool: True if the update was successful, False if there was an error.
    #     """
    #     try:
    #         # Check if the file exists, and if not, create it
    #         if not os.path.exists(file_path):
    #             with open(file_path, 'w') as new_file:
    #                 new_file.write('')  # Create an empty file

    #         # Read the existing YAML data
    #         with open(file_path, 'r') as file:
    #             data = yaml.safe_load(file) or {}

    #         # Update the data
    #         data[key] = new_value

    #         # Write the updated data back to the file
    #         with open(file_path, 'w') as file:
    #             yaml.dump(data, file, default_flow_style=False)

    #         return True  # Successful update

    #     except Exception as e:
    #         print(f"Error updating or creating YAML file: {e}")
    #         return False  # Error occurred during update or creation
 




class DbManager:
    def __init__(self):
        # initialize
        self.config_file_path       = SETTINGS_YAML_PATH
        self.exercise_database_path = EXERCISE_DB_PATH
        self.exercise_log_path      = EXERCISE_LOG_PATH

    def give_me_a_exercise(self) -> dict:
        '''
        Returns a dictionary of exercise based on the settings and last exercised value
        '''


        # get user preference from settings.yaml
        user_preference_dict = ConfigReader(self.config_file_path).read_config_file()
        user_preference_dict = user_preference_dict['database']

        if user_preference_dict['muscle'] == 'default': 
            # if default, cycle through exercises

            if not os.path.exists(self.exercise_log_path): 
                # if log db doesn't exist, program launched for the first time
                # so add random exercise
                user_preference_dict['muscle'] = 'chest' 

            else:
                user_preference_dict['muscle'] = ExerciseDatabase().next_muscle()

        # process the settings which is dict and convert as a query for searching
        user_preference_for_query = self.process_settings(user_preference_dict)

        exercise = ExerciseDatabase().select_matching(user_preference_for_query,only_one=True, random=True)
        return exercise

    def process_settings(self, setting_dict) -> list:
        '''
        returns list of conditions which will be used further to create query conditions
        '''
        condition_list = []

        # check if user selected stretches
        # print('stretches' in setting_dict.values())

        for key, value in setting_dict.items():

            condition_list.append(f"{key}='{value}'")
        print(condition_list)
        return condition_list
class ExerciseDatabase:
    def __init__(self):
        self.exercise_db_path = EXERCISE_DB_PATH
        self.exercise_log_path = EXERCISE_LOG_PATH
        self.exercise_log_table_name = EXERCISE_LOG_TABLE_NAME

    def next_muscle(self)-> str:
        '''Returns the next exercise
        - First check the log_database for the last exercise 
        - Second from the ExerciseDatabase get the name of next muscle group
        
        Return: name of next muscle group
        '''
        # check what was the last muscle targetted
        last_log_entry = SqliteDefs.get_latest_row_as_dict(self.exercise_log_path,self.exercise_log_table_name)
        last_muscle_targetted = last_log_entry['muscle']
        # Id of last muscle
        last_muscle_targetted_dict= SqliteDefs.retrieve_data_as_dict(self.exercise_db_path,'Muscles',[f"muscle = '{last_muscle_targetted}'"])
        # last_muscle_targetted_dict = 
        last_muscle_id = last_muscle_targetted_dict[0]['muscle_id'] # list of dictionaries so to remove the list
    
        next_muscle_dict = SqliteDefs.get_next_entry(self.exercise_db_path,'Muscles','muscle_id',last_muscle_id)
        print('next_muscle_dicct',next_muscle_dict)
        return next_muscle_dict['muscle']

    def select_matching(self,query_conditions, only_one=False, random=False) -> dict:
        exercises_matching_condition = SqliteDefs.retrieve_data_as_dict(self.exercise_db_path,
                                                                        'Exercise',
                                                                       query_conditions)
            ## IF NO EXERCISE FOUND WITH GIVEN DIFFICULTY REMOVE DIFFICULTY AND SERCHISE
        if not exercises_matching_condition:
            query_with_removed_difficiculty = [item for item in query_conditions if not item.startswith("difficulty=")]
            exercises_matching_condition = SqliteDefs.retrieve_data_as_dict(self.exercise_db_path,
                                                                        'Exercise',
                                                                       query_with_removed_difficiculty)


        print('Query conditions:', query_conditions)
        if only_one and exercises_matching_condition and not random:
            return exercises_matching_condition[0]  # return first element
        elif only_one and random and exercises_matching_condition:  # return random
            # [0] because retrieve_data_as_dict gives list of dicts
            return rnd.choices(exercises_matching_condition)[0]
        else:
            return exercises_matching_condition  # returns all matching
if __name__ == '__main__':
   
    exercise = DbManager().give_me_a_exercise()
    # pprint.pprint(exercise)

    # ➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # db_path = 'data\exercise_database.sqlite'
    # conn = sqlite3.connect(db_path)

    # cursor = conn.cursor()
    # # ➖➖➖➖➖➖➖➖➖➖➖➖ ACTIONS PEFORMED ON SCRAPED DATABASE ➖➖➖➖➖➖➖➖➖➖➖➖
    # # SqliteDefs.create_new_table_from_a_column_of_existing_table(cursor,'Exercise','muscle',"Muscles",'muscle')
    # # SqliteDefs.add_foreign_key(cursor,'Exercise','name','Muscles','name')
    # # SqliteDefs.populate_foreign_keys_based_on_condition(cursor,'Exercise','name',
    # #                                                     'Muscles','name',
    # #                                                     'Exercise.muscle = Muscles.muscle')
    # # ➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # # Commit the changes and close the cursor and the connection
    # conn.commit()
    # cursor.close()
    # conn.close()
