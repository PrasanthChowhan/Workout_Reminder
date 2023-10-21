import requests
import json
from src.utils.SQLITE import SqliteDefs
from src.utils.constants import DatabaseConstants


class NotionIntergrate:
    def __init__(self):
        self.URL = "https://api.notion.com/v1/databases/"
        self.NOTION_API_KEY = "secret_pQDRHWjHeuQKobzHR13o427U1fmr5YCmlg5wl5tcO7j"
        self.PAGE_ID = "a88edc8d512c451798c284b88f70b9f1"
        self.headers = {
            "Authorization": self.NOTION_API_KEY,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    
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
                "Equipment":{
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
                    "created_time": {}
                } 


            }
        }
        response_data = self.send_request(self.URL,data)
        database_id = response_data['id']
        return database_id
    def add_row_to_database(self):
        databaseId = "b7fcbd11-a397-47ab-aa99-d3caf02a3dca"
        pageurl = "https://api.notion.com/v1/pages"

        newPagedata = {
            "parent": {"type": "database_id", "database_id": databaseId},
            "properties": {
                "Exercise Name": {
                    "type": "title",
                    "title": [{"type": "text", 
                               "text": {"content": "🎈🎈🎈"}
                               }]
                }, 
                "Completed":{
                    # "type": "checkbox",
                    "checkbox" : True
                },
                "Difficulty":{
                    "select":{
                    "name": "Intermediate"
                    }
                },
                "Muscle targetted":{
                    "select":{
                        "name":"chest",
                        
                    }
                },
                "Equipment":{
                    "select":{
                        "name":"bodyweight"
                    }
                }
                          
        }
        }
        self.send_request(pageurl,newPagedata)
    
    def send_request(self,url, data:json):
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
    def _create_option_from_db(self,table_name: str, column_name: str):   

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
    notion.add_row_to_database()
    

