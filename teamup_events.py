import requests
apikey = "021d5ce3f150bda7e1727d637ed9ccdc1a40d4c03a5f693721ee5badc39c18a7"

session = requests.Session()
#session.auth = ('Teamup-Token ', apikey);
session.headers.update({'Teamup-Token': apikey})

r = session.get('https://api.teamup.com/ks9q9tx6hkpjiictdg/events')
print(r.status_code)
print(r.text)
