import sqlite3,os,pprint
import yaml
from dataclasses import dataclass
from datetime import datetime
import random as rnd
# this is custom package will be present in learning respository
# from python_learned.Sqlite import SqliteDefs
from utils.SQLITE import SqliteDefs
from utils.constants import *

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
            # [0] because retrieve_data_as_dict gives list of dicts
            return rnd.choices(exercises_matching_condition)[0]
        else:
            return exercises_matching_condition  # returns all matching



class ExerciseLog:
    '''
    used for Gui 
    - create a new db if it doesn't exist
    - create the table in the following format
    - methods manipulate the dictionary of this class
    
    '''
    def __init__(self):
        current_datetime = datetime.now()
        self.log_entry = {
            'name': None,
            'muscle': None,
            'difficulty': None,
            'equipment': None,
            'completed': None,
            'reason': None,
            'date': current_datetime.strftime('%d'),
            'month': current_datetime.strftime('%B'),
            'year': current_datetime.strftime('%Y'),
            'time': current_datetime.strftime('%H:%M:%S')
        }

    def set_completed(self, is_completed):
        self.log_entry['completed'] = is_completed

    def add_reason(self, text):
        self.log_entry['reason'] = text

    def copy_values_from_dict(self, source_dict):
        for key in source_dict:
            if key in self.log_entry:
                self.log_entry[key] = source_dict[key]

    def add_entry_to_database(self):
        DbManager.insert_data_into_table(EXERCISE_LOG_PATH, 'Track', self.log_entry)

    def get_log_entry(self):
        return self.log_entry


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

        if user_preference_dict['muscle'] == 'default': 
            # if default cycle through exercises

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
        returns list of conditions which will be used further to create queiry conditions
        '''
        condition_list = []

        # check if user selected stretches
        # print('stretches' in setting_dict.values())

        for key, value in setting_dict.items():

            condition_list.append(f"{key}='{value}'")

        return condition_list

    @staticmethod
    def insert_data_into_table(database_or_cursor, table_name: str, data_dict: dict) -> bool:
        """
        Insert data into a table in an SQLite database.

        Args:
            database_or_cursor (str or sqlite3.Cursor): Either a database path or a cursor object.
            table_name (str): The name of the table where data will be inserted.
            data_dict (dict): A dictionary where keys are column names, and values are the data to be inserted.

        Returns:
            bool: True if the insertion was successful, False if an error occurred.

        Raises:
            ValueError: If the database_or_cursor argument is invalid.

        Example:
            data = {
                "name": "John Doe",
                "age": 30,
                "city": "New York"
            }
            success = insert_data_into_table("mydb.db", "users", data)
            if success:
                print("Data inserted successfully.")
            else:
                print("Error inserting data.")
        """
        if isinstance(database_or_cursor, str):
            # If a database path is provided, create a new connection and cursor
            connection = sqlite3.connect(database_or_cursor)
            cursor = connection.cursor()
        elif isinstance(database_or_cursor, sqlite3.Cursor):
            # If a cursor is provided, use it directly
            cursor = database_or_cursor
        else:
            raise ValueError("Invalid database_or_cursor argument")

        try:
            # Create the table if it doesn't exist
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {", ".join(data_dict.keys())}
                )
            ''')

            # Insert data into the table
            placeholders = ", ".join(["?" for _ in data_dict])
            values = tuple(data_dict.values())

            cursor.execute(f'''
                INSERT INTO {table_name} ({", ".join(data_dict.keys())})
                VALUES ({placeholders})
            ''', values)

            connection.commit()
            return True  # Success

        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")
            return False  # Error occurred
        finally:
            if isinstance(database_or_cursor, str):
                # Close the database connection if it was created here
                connection.close()

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
