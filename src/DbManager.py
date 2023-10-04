import sqlite3
import yaml
import pprint
import random as rnd
# this is custom package will be present in learning respository
# from python_learned.Sqlite import SqliteDefs
from utils.SQLITE import SqliteDefs

'''
What this module does 
 * read settings.yaml file
 * use that as query to search table
 * return one exercise 

'''


class ConfigReader:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def read_config_file(self) -> dict:
        """
        Read and parse the configuration file in YAML format.
        Returns:
            dict: A dictionary containing the parsed configuration data.
        """
        with open(self.config_file_path) as config_file:
            loaded_data = yaml.safe_load(config_file)
        return loaded_data

    def write_config_file(self, data: dict):
        """
        Write data to the configuration file in YAML format.
        Args:
            data (dict): The data to be written to the file.
        """
        with open(self.config_file_path, 'w') as config_file:
            yaml.dump(data, config_file,
                      default_flow_style=False, sort_keys=False)


class DataSelector:
    def __init__(self, database_path, table, query_conditions):
        # initialize
        self.database_path = database_path
        self.query_conditions = query_conditions
        self.table = table

    def select_matching(self, only_one=False, random=False) -> dict:
        exercises_matching_condition = SqliteDefs.retrieve_data_as_dict(self.database_path,
                                                                        self.table,
                                                                        self.query_conditions)
        if only_one and exercises_matching_condition and not random:
            return exercises_matching_condition[0]  # return first element
        elif only_one and random and exercises_matching_condition:  # return random
            return rnd.choices(exercises_matching_condition)[0]  # [0] because retrieve_data_as_dict gives list of dicts 
        else:
            return exercises_matching_condition # returns all matching 


class DbManager:
    def __init__(self, config_file_path, exercise_database_path):
        # initialize
        self.config_file_path = config_file_path
        self.exercise_database_path = exercise_database_path

    def give_me_a_exercise(self):
        # getting settings from the file
        user_preference_dict = ConfigReader(
            self.config_file_path).read_config_file()

        # process the settings which is dict and convert as a query for searching
        user_preference_for_query = self.process_settings(user_preference_dict)

        exercise = DataSelector(self.exercise_database_path, 'Exercise', user_preference_for_query
                                ).select_matching(only_one=True, random=True)
        return exercise

    def process_settings(self, setting_dict) -> list:
        '''
        returns list of conditions which will be used further to create queiry conditions
        '''
        condition_list = []

        # check if user selected stretches
        # print('stretches' in setting_dict.values())

        for key, value in setting_dict.items():

            condition_list.append(f"{key}='{value}'")
    
        return condition_list


class UserLogs:
    pass


if __name__ == '__main__':
    exercise = DbManager('data\settings.yaml',
              'data\exercise_database.sqlite').give_me_a_exercise()
    pprint.pprint(exercise)


    #➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # db_path = 'data\exercise_database.sqlite'
    # conn = sqlite3.connect(db_path)

    # cursor = conn.cursor()
    # # ➖➖➖➖➖➖➖➖➖➖➖➖ ACTIONS PEFORMED ON SCRAPED DATABASE ➖➖➖➖➖➖➖➖➖➖➖➖
    # # SqliteDefs.create_new_table_from_a_column_of_existing_table(cursor,'Exercise','muscle',"Muscles",'muscle')
    # # SqliteDefs.add_foreign_key(cursor,'Exercise','muscle_id','Muscles','muscle_id')
    # # SqliteDefs.populate_foreign_keys_based_on_condition(cursor,'Exercise','muscle_id',
    # #                                                     'Muscles','muscle_id',
    # #                                                     'Exercise.muscle = Muscles.muscle')
    # # ➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
    # # Commit the changes and close the cursor and the connection
    # conn.commit()
    # cursor.close()
    # conn.close()
