import requests
import config

session = requests.Session()
session.headers.update(
        {
            'Teamup-Token': config.TEAMUP_API_KEY,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    )

payload = {
        'subcalendar_ids':[0],
        'start_dt':'2024-10-26T14:35:24Z', 
        'end_dt':'2024-10-26T15:35:24Z',
        'title': 'test',
           }
r = session.post('https://api.teamup.com/ksvvx3e1n68gmkz7x8/events', json=payload)

print(r.status_code)
print(r.text)
