from datetime import datetime
from src.utils.SQLITE import SqliteDefs
from src.utils.constants import *
from src.NotionIntegrate import NotionIntergrate
from src.utils.Create_csv import CreateCSV

import time,threading


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute.")
        return result
    return wrapper


class ExerciseLog:
    '''
    used for Gui 
    - format for tracking user data
    - create table of following structure if doesnt exist.and add dict as row to db
    - save to cloud (Notion)
    - methods to manipulate the dictionary of this class

    '''

    def __init__(self):
        current_datetime = datetime.now()
        self.log_entry = {
            'name': None,
            'muscle': None,
            'difficulty': None,
            'equipment': None,
            'completed': False,
            'reason': '',
            'url': '',
            'date_time': current_datetime.isoformat()
        }

    def set_completed(self, is_completed):
        self.log_entry['completed'] = bool(is_completed)

    def add_reason(self, text):
        self.log_entry['reason'] = text

    def copy_values_from_dict(self, source_dict):
        for key in source_dict:
            if key in self.log_entry:
                self.log_entry[key] = source_dict[key]
    # @timing_decorator

    def add_entry_to_database(self):

        threading.Thread(target=SqliteDefs.insert_data_into_table, 
                         args=(DatabaseConstants.EXERCISE_LOG_PATH, 'Track', self.log_entry)).start()
        threading.Thread(target=NotionIntergrate().add_row_to_database,
                         args=(self.log_entry)).start()
        threading.Thread(target=CreateCSV, 
                         args=(DatabaseConstants.CSV_PATH, self.log_entry)).start()

    def get_log_entry(self):
        return self.log_entry
