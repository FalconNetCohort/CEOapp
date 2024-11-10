import requests
import config
#import parse_cmts
from dataclasses import dataclass
from datetime import datetime, timedelta, UTC, timezone



#this should be imported from parse_cmts.py but that file doesnt work atm, so this is
#temporary workaround
@dataclass
class CMTSEvent:
    type: str  # 'TypeforCommMaster'
    name: str  # 'Title'
    description: str  # 'Description'
    time: datetime  # 'EventDate'
    submission_start: datetime  # 'EventDate'
    submission_deadline: datetime  # 'EndDate'
    attending_units: list[str]
    attending_class_years: list[bool]
    attending_users: list[str]
    accountability_method: str


#set headers
session = requests.Session()
session.headers.update(
        {
            'Teamup-Token': config.TEAMUP_API_KEY,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    )

#only way to get these AFAIK is through get requests
def get_subcalendar_ids() -> list[str]:
    request = session.get('https://api.teamup.com/ksvvx3e1n68gmkz7x8/configuration') 
    calendar_info_json = request.json()
    sub_calendars = calendar_info_json['configuration']['subcalendars']
    calendar_ids = [calendar['id'] for calendar in sub_calendars] 
    return calendar_ids

#IMPORTANT FUNCTON: post event to calendar
def post_event(
        event: CMTSEvent, 
    ):


    subcalendar_id = (get_subcalendar_ids())[0];    
    note = event.accountability_method # this should be built out to include all extra info
    params = {
        'inputFormat':'html'
    }    
    
    payload = {
        'subcalendar_ids':[subcalendar_id],
        'start_dt': event.submission_start, 
        'end_dt': event.submission_deadline,
        'title': event.name,
        'notes': note
    }
    
    r = session.post('https://api.teamup.com/ksvvx3e1n68gmkz7x8/events', json=payload, params=params)
    return r.status_code,r.text

now = timezone.utc
time = datetime.now(now).isoformat(timespec='seconds')
print(time)
event = CMTSEvent(
    "other",  
    "Event",  
    "Test", 
    time,
    time, 
    time, 
    ["Hello"],
    [True,True,True,True],
    ["1","2","3"],
    "Accountability",
)

print(post_event(event))