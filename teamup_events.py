import requests
apikey = "REDACTED"

session = requests.Session()
#session.auth = ('Teamup-Token ', apikey);
session.headers.update({'Teamup-Token': apikey})

r = session.get('https://api.teamup.com/ks9q9tx6hkpjiictdg/events')
print(r.status_code)
print(r.text)
