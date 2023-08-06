import hmac
import hashlib
import requests
import json


def generate_signature(data, key):
    mac = hmac.new(key.encode("utf-8"), msg=data, digestmod=hashlib.sha1)
    return mac.hexdigest()

url = 'http://127.0.0.1:8000/th/api/taiga/webhook/5/1235'
# url = 'http://127.0.0.1:5000/taiga/123'

key = '1235'
"""
data = {
    "type": "test",
    "by": {
        "id": 6,
        "permalink": "http://localhost:9001/profile/user1",
        "username": "user1",
        "full_name": "Purificacion Montero",
        "photo": "//media.taiga.io/avatar.80x80_q85_crop.png",
        "gravatar_id": "464bb6d514c3ecece1b87136ceeda1da"
    },
    "date": "2016-04-12T12:00:56.335Z",
    "action": "test",
    "data": {
        "test": "test",
        "permalink": "https://tree.taiga.io/project/foxmask-trigger-happy/us/3"
    }
}
"""
data = {
    "type": "userstory",
    "date": "2016-04-12T12:17:20.486Z",
    "action": "create",
    "data": {
        "custom_attributes_values": {},
        "watchers": [],
        "permalink": "http://localhost:9001/project/project-0/us/72",
        "tags": [
            "dolorum",
            "adipisci",
            "ipsa"
        ],
        "external_reference": '',
        "project": {
            "id": 1,
            "permalink": "http://localhost:9001/project/project-0",
            "name": "Project Example 0",
            "logo_big_url": ""
        },
        "owner": {
            "id": 6,
            "permalink": "http://localhost:9001/profile/user1",
            "username": "user1",
            "full_name": "Purificacion Montero",
            "photo": "//media.taiga.io/avatar.80x80_q85_crop.png",
            "gravatar_id": "464bb6d514c3ecece1b87136ceeda1da"
        },
        "assigned_to": "",
        "points": [
            {
                "role": "UX",
                "name": "5",
                "value": 5.0
            },
            {
                "role": "Design",
                "name": "1",
                "value": 1.0
            },
            {
                "role": "Front",
                "name": "3",
                "value": 3.0
            },
            {
                "role": "Back",
                "name": "40",
                "value": 40.0
            }
        ],
        "status": {
            "id": 1,
            "name": "New",
            "slug": "new",
            "color": "#999999",
            "is_closed": False,
            "is_archived": False
        },
        "milestone": "",
        "id": 139,
        "is_blocked": True,
        "blocked_note": "Blocked test message",
        "ref": 72,
        "is_closed": False,
        "created_date": "2016-04-12T12:17:19+0000",
        "modified_date": "2016-04-12T12:17:19+0000",
        "finish_date": "",
        "subject": "test user story 5",
        "description": "this is a test description",
        "client_requirement": False,
        "team_requirement": True,
        "generated_from_issue": "",
        "tribe_gig": ""
    },
    "by": {
        "id": 6,
        "permalink": "http://localhost:9001/profile/user1",
        "username": "user1",
        "full_name": "Purificacion Montero",
        "photo": "//media.taiga.io/avatar.80x80_q85_crop.png",
        "gravatar_id": "464bb6d514c3ecece1b87136ceeda1da"
    }
}


signature = generate_signature(json.dumps(data).encode("utf-8"), key)

headers = {
    "X-TAIGA-WEBHOOK-SIGNATURE": signature,
    "X-Hub-Signature": "sha1={}".format(signature),
    "Content-Type": "application/json"
}

request = requests.post(url, data=json.dumps(data).encode("utf-8"),
                        headers=headers)
print(request)

