import requests
import json

token = "secret_pQDRHWjHeuQKobzHR13o427U1fmr5YCmlg5wl5tcO7j"

databaseId = "adbee758-e99a-43e6-8c11-eed12771f4d5"
headers = {
    "Authorization": token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
# response = requests.post(url=f'{url}/sdapi/v1/interrogate', json=caption_payload)


def readDb(databaseId, headers):
    readurl = f"https://api.notion.com/v1/databases/{databaseId}"
    # res = requests.request("get", readurl, headers=headers)
    res = requests.get(readurl, headers=headers)
    data = res.json()
    print(res.status_code)
    with open("./db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


def createPage(databaseId, headers):
    pageurl = "https://api.notion.com/v1/pages"

    newPagedata = {
        "parent": {"type": "database_id", "database_id": databaseId},
        "properties": {
            "Name": {
                "type": "title",
                "title": [{"type": "text", "text": {"content": "soromatoes"}}]
            },
            
            

    }
    }
    data = json.dumps(newPagedata)
    res = requests.request("post", pageurl, headers=headers, data=data)
    if res.status_code == 200:
        print(f"Status Code 200: {res.reason}")
    else:
        print(f"Status Code {res.status_code}: {res.reason}")


# readDb(databaseId, headers)
createPage(databaseId, headers)





   