import requests
import json
from src.utils.SQLITE import SqliteDefs
from src.utils.constants import DatabaseConstants
from src.DbManager import ConfigReader


class NotionIntergrate:
    def __init__(self):
        self.DBURL = "https://api.notion.com/v1/databases/"
        self.pageurl = "https://api.notion.com/v1/pages"
        # self.NOTION_API_KEY = ""
        # self.PAGE_ID = ""
        self.headers = {
            "Authorization": self.NOTION_API_KEY,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        settings = ConfigReader(DatabaseConstants.SETTINGS_YAML_PATH).read_config_file()
        self.notion_settings = settings.get('Integration setting', {}).get('Notion')

        self.NOTION_API_KEY = self.notion_settings['api']
        self.PAGE_ID = self.notion_settings['page_id']

        # self.notion_settings= get_nested_dict_value(settings,'Notion')
        if self.notion_settings:
            ## get save value, any error during retriving default False ##
            if self.notion_settings.get('save', False):

                # CHECK IF DBID EXISTS IF NOT CREATE DATABASE
                self.database_id = self.notion_settings.get('database_id', None)
                if self.database_id == None or self.database_id == '':
                    self.database_id = self.create_db()
                    settings['Integration setting']['Notion']['database_id'] = self.database_id
                    ## Add to file ##
                    ConfigReader().update_or_create_yaml_file(DatabaseConstants.SETTINGS_YAML_PATH, settings)

        # print(self.notion_setting)

    def create_db(self):
        ## STRUCTURE OF DATABSE ##
        data = {
            "parent": {
                "type": "page_id",
                "page_id": self.PAGE_ID
            },
            "icon": {
                "type": "emoji",
                "emoji": "🔥"
            },
            "cover": {
                "type": "external",
                "external": {
                    "url": "https://unsplash.com/photos/qZ-U9z4TQ6A"
                }
            },
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": "My Workouts",
                        "link": None
                    }
                }
            ],
            "properties": {
                "Exercise Name": {
                    "title": {}
                },
                "Reason": {
                    "rich_text": {}
                },
                "Completed": {
                    "checkbox": {}
                },
                "Muscle targetted": {
                    "select": {
                        "options": self._create_option_from_db(table_name=DatabaseConstants.EXERCISE_DB_TABLE_NAME,
                                                               column_name='muscle')
                    }
                },
                "Equipment": {
                    "select": {
                        "options": self._create_option_from_db(table_name=DatabaseConstants.EXERCISE_DB_TABLE_NAME,
                                                               column_name='equipment')
                    }

                },
                "Difficulty": {
                    "select": {
                        "options": self._create_option_from_db(table_name=DatabaseConstants.EXERCISE_DB_TABLE_NAME,
                                                               column_name='difficulty')
                    }
                },
                "Done on": {
                    'date': {}
                }


            }
        }
        response_data = self.send_request(self.DBURL, data)
        database_id = response_data['id']
        return database_id

    def add_row_to_database(self, user_log: dict = {}):

        ## USE KEYS FROM EXERCISELOG ##

        newPagedata = {
            "parent": {"type": "database_id", "database_id": self.database_id},
            "properties": {
                "Exercise Name": {
                    "type": "title",
                    "title": [{"type": "text",
                               "text": {
                                   "content": user_log.get('name', 'Test'),
                                   "link": {'url': user_log.get('url', 'https://www.youtube.com/@prasanthchowhan')}
                               }
                               }]
                },
                "Completed": {
                    # "type": "checkbox",
                    "checkbox": user_log.get('completed', False)
                },
                "Difficulty": {
                    "select": {
                        "name": user_log.get('difficulty', 'beginner')
                    }
                },
                "Muscle targetted": {
                    "select": {
                        "name": user_log.get('muscle', 'chest')

                    }
                },
                "Equipment": {
                    "select": {
                        "name": user_log.get('equipment', 'bodyweight')
                    }
                },
                "Reason": {
                    "rich_text": [{
                        "type": "text",
                                "text": {
                                    "content": user_log.get('reason', 'test_reason'),
                                    "link": None
                                },
                        ## if you ever wanted to retrive unfromatted text use create a plain text ##

                    }],

                },
                "Done on": {

                    "type": "date",
                    "date": {
                        "start": user_log.get('date_time', "1999-09-09T09:09:09"),
                        "end": None,
                        "time_zone": 'Asia/Kolkata'
                    }
                }
            }
        }
        self.send_request(self.pageurl, newPagedata)

    def send_request(self, url, data: json):
        response = requests.post(url, headers=self.headers, json=data)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Request was successful, parse the JSON content if needed
            response_data = response.json()
            # print("Request was successful.")
            return response_data
        else:
            # Request failed, print the error message
            error_message = response.text  # or response.content if you need the raw content
            print(f"Request failed with status code {response.status_code}")
            print(f"Error message: {error_message}")

# b7fcbd11-a397-47ab-aa99-d3caf02a3dca
    ## SUPPORTING FUNCTIONS ##
    def _create_option_from_db(self, table_name: str, column_name: str):

        values = SqliteDefs.get_distinct_column_values(
            table_name=table_name,
            column_name=column_name,
            database_or_cursor=DatabaseConstants.EXERCISE_DB_PATH)

        options = []
        for value in values:
            option = {
                "name": value,
                # "color": "green"  ## Set a default color here
            }
            options.append(option)

        return options


if __name__ == "__main__":
    url = "https://api.notion.com/v1/databases/"
    notion = NotionIntergrate()
    # notion.create_db()
    notion.add_row_to_database()
