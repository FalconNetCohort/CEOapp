import os
import requests
from dotenv import load_dotenv

envFile = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(envFile)

apikey = os.getenv('TEAMUP_API_KEY')
email = os.getenv('TEAMUP_EMAIL')
password = os.getenv('TEAMUP_PASSWORD')

session = requests.Session()
#session.auth = ('Teamup-Token ', apikey);
session.headers.update({'Teamup-Token': apikey})

# Bearer Token - failsafe to misconfigured perms
url = "https://api.teamup.com/auth/tokens"

payload = {
    "app_name": "testAPI",
    "device_id": "My device",
    "email": email,
    "password": password
}
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Teamup-Token": apikey
}

response = requests.post(url, json=payload, headers=headers)

bearer_token = response.json()['auth_token']
print(bearer_token)


# Get events
r = session.get('https://api.teamup.com/ks9q9tx6hkpjiictdg/events')
print(r.status_code)
print(r.json()['events'])

calId = 'ks9q9tx6hkpjiictdg'

url = "https://api.teamup.com/"+calId+"/events"

headers = {
    "Accept": "application/json",
    "Teamup-Token": apikey
}

response = requests.get(url, headers=headers)

print(response.json())