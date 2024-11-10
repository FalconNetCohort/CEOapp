import pickle
import xml.etree.ElementTree as ET
from collections import defaultdict

import requests

url = "https://usafa0.sharepoint.com/CW/CWT/_api/web/lists/GetByTitle('CMTS_and_CW_Calendar')/items"


def get_data(source: str) -> str:
    return requests.get(
        source,
        headers={
            "Cookie": "MSFPC=GUID=bb36b5023e524d1db946bdc16bc4eb31&HASH=bb36&LV=202305&V=4&LU=1683775865952; "
                      "WordWacDataCenter=PUS1; PowerPointWacDataCenter=PUS5; WacDataCenter=PUS5; rtFa=/ulRwnoWSBgGaXvxtub5"
                      "QYGpSMX3IiaQEqgAWwnVoM4mN0FCODBBMDYtRjAyOS00NUMwLTg0RDEtN0RBRDE5Q0UzQzYxIzEzMzM5NzE1MDMwNzI0OTEyMyM"
                      "wMzY3RENBMC05MERGLTQwMDAtMkRCNC03OEEwMTYyNURCNjQjQzI2RVRIQU4uQ0hBUE1BTiU0MEFGQUNBREVNWS5BRi5FRFUjMT"
                      "kyMDU0I1ZUR0NCRVRHUERJU1FLRUhWRVNQRi0xQU1KSUMNuQ/gdemKYdFwTsJZR0Vg+quNNtoApw3tXxDK/ooCwPLZQQp/YaPIr"
                      "d58dxHm7a+oyDTHHLIyqSrPwVkgwAjvHjhD72FxSgrqzdn5B6VFj5rSvIgR4Ssmeh8VQnS7Q1bxR1kNfB91JjU9Gp61sD94+58z"
                      "cPhqMMg6aZZuJf4nvRuIlsqgfFIWzdw6oZOZGTTt7AYQEqPiueSR4Gu/frB2L6QG/EMS59K+G02Vn6Y7J+o7kGe4z6/5oi+3TLQ"
                      "0Drazl4A7o1KM+TTZvn3DAZrytikrNVu47kl16qegcOcGyx6H/eLKa+A433CH3K8BUIjI4YMixGSFCyr5oyG+7O7EAAAA; SIMI"
                      "=eyJzdCI6MH0=; FedAuth=77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjEzLDBoLmZ8bWVt"
                      "YmVyc2hpcHwxMDAzMjAwMjA2MTU1NjU3QGxpdmUuY29tLDAjLmZ8bWVtYmVyc2hpcHxjMjZldGhhbi5jaGFwbWFuQGFmYWNhZGV"
                      "teS5hZi5lZHUsMTMzMzk3MTUwMjkwMDAwMDAwLDEzMzAwNjY2NTc4MDAwMDAwMCwxMzMzOTgwMTQzMDcyNDkxMjMsMTI5LjE5Lj"
                      "E2My4yNTQsNjU2MDIsN2FiODBhMDYtZjAyOS00NWMwLTg0ZDEtN2RhZDE5Y2UzYzYxLCxmYmEyNjA3OC0zZDRmLTQ0MTEtOTUxM"
                      "i02YmE2MDRhMWJiMzMsMDM2N2RjYTAtOTBkZi00MDAwLTJkYjQtNzhhMDE2MjVkYjY0LDAzNjdkY2EwLTkwZGYtNDAwMC0yZGI0"
                      "LTc4YTAxNjI1ZGI2NCwsMCwxMzMzOTcxODYzMDU4NDI3NzYsMTMzMzk5NzQyMzA1ODQyNzc2LCwsZXlKallYQnZiR2xrYzE5c1l"
                      "YUmxZbWx1WkNJNklsdGNJalF6T1RoaVpXWXdMVGczTmpBdE5EWmlZeTA1WldVeUxXRXdPRGhqTmpsbFptTXdObHdpWFNJc0luaH"
                      "RjMTlqWXlJNklsdGNJa05RTVZ3aVhTSXNJbmh0YzE5emMyMGlPaUl4SWl3aWNISmxabVZ5Y21Wa1gzVnpaWEp1WVcxbElqb2lRe"
                      "kkyUlhSb1lXNHVRMmhoY0cxaGJrQmhabUZqWVdSbGJYa3VZV1l1WldSMUlpd2lkWFJwSWpvaWIyUk9PR2hKWlVJME1FOVNVSGx6"
                      "T1RjMmNVbEJRU0o5LDI2NTA0Njc3NDM5OTk5OTk5OTksMTMzMzk3MTUwMjkwMDAwMDAwLGJiNTNhNTc4LTAwNGEtNDEwYy05MGY"
                      "zLWFiZGMwN2RkZTk0NSwsLCwsLDAsLDE5MjA1NCxHQWR4V1gzcWctcGxQNGU5WEJQMXkxNmlmalUsTHo2bWQyWmdCZG9DWUlITW"
                      "hycXVhbXExQzRCc3IxVHdKbkpVRU95dHBjbndKaWRtZjVhTDJDVzNpcUZRd0hyanZ2UlBlOHVQejdEa1BRRVJpY1VIWkdXdGVKR"
                      "m0xTVl2NHhBY1JaL3NyWUg2cU0vMlF3dUdxMDhZRjZncnJLelluTlo5QVZPR1RoVFE0OWVuWWMxVVFTR0lITkxVaElnZEwwTmFw"
                      "UlNPakpJOTB6UC9XTkVhVktzY2ticVFsaVpQU3pTWVpkUjd3MzA0UngzT2h2emtIM2JUNUlaRWpCZnRCUUJwZHk5bXo2emtkd2J"
                      "GdC9IT3lMcUpSVlh1MEREVVhHelZ1RXpnN29pV3VrV3hUcWZwaHNKK01uUUlUenA2cld1S3NyaHUxMVRla3gxYkxxS0RvVk4wam"
                      "ZIRHVLa1craHVObzVUeGF4YmFWZjJ5QlNGWit3PT08L1NQPg==; spo_abt=Mjg4MDAsWyJpbmtub3dubnR3ayJdLCxmYmEyNjA"
                      "3OC0zZDRmLTQ0MTEtOTUxMi02YmE2MDRhMWJiMzM=; WSS_FullScreenMode=false; odbn=1"
        }
    ).text


plist = defaultdict(lambda: [])

events = []


def get_event_list(source: str = None):
    next_link = None

    if source is None:
        # root = ET.fromstring(get_data(url))
        root = ET.parse("thing.xml").getroot()
    else:
        root = ET.fromstring(get_data(source))

    for child in root:
        if 'entry' in child.tag:
            print("\n\n")
            content = child.find('{http://www.w3.org/2005/Atom}content')
            if content is None:
                continue
            properties = content.find('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties')
            if properties is None:
                continue
            events.append(properties)
            for prop in properties:
                prop_tag = prop.tag.split('}')[1]
                prop_value = prop.text
                plist[prop_tag].append(prop_value)
        if 'link' in child.tag:
            if child.attrib['rel'] == 'next':
                next_link: str = child.attrib['href']

    if next_link is not None:
        get_event_list(next_link)

text = get_data(url)
print(text)
#get_event_list(url)

#with open('plist.pickle', 'wb') as file:
#    pickle.dump(dict(plist), file)
#with open('events.pickle', 'wb') as file:
#    pickle.dump(events, file)
