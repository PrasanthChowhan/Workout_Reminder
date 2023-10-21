import requests
from src.utils.SQLITE import SqliteDefs
from src.utils.constants import DatabaseConstants


def create_option_from_db(table_name: str, column_name: str):

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


NOTION_API_KEY = "secret_pQDRHWjHeuQKobzHR13o427U1fmr5YCmlg5wl5tcO7j"
PAGE_ID = "a88edc8d512c451798c284b88f70b9f1"
## FROM https://www.notion.so/prasanthchowhan/API-a88edc8d512c451798c284b88f70b9f1?pvs=4 ##

url = "https://api.notion.com/v1/databases/"
headers = {
    "Authorization": NOTION_API_KEY,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
## STRUCTURE OF DATABSE ##
data = {
    "parent": {
        "type": "page_id",
        "page_id": PAGE_ID
    },
    "icon": {
        "type": "emoji",
        "emoji": "😊"
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
                "options": create_option_from_db(table_name=DatabaseConstants.EXERCISE_DB_TABLE_NAME,
                                                 column_name='muscle')
            }
        },
        "Difficulty": {
            "select": {
                "options": [
                    {
                        "name": "Beginner",
                        "color": "green"
                    },
                    {
                        "name": "Intermediate",
                        "color": "orange"
                    },
                    {
                        "name": "Advanced 🔥",
                        "color": "red"
                    }
                ]
            }
        },
        "Done on": {
            "created_time": {}
        } 


    }
}

response = requests.post(url, headers=headers, json=data)

# Check if the request was successful (HTTP status code 200)
if response.status_code == 200:
    # Request was successful, parse the JSON content if needed
    response_data = response.json()
    print("Request was successful.")
    print(response_data['id'])
else:
    # Request failed, print the error message
    error_message = response.text  # or response.content if you need the raw content
    print(f"Request failed with status code {response.status_code}")
    print(f"Error message: {error_message}")

