import requests
import config
#import parse_cmts
from dataclasses import dataclass
from datetime import datetime, timedelta, UTC



#this should be imported from parse_cmts.py but that file doesnt work atm, so this is
#temporary workaround
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
        start_dt: str, 
        end_dt: str, 
        title: str, 
        attending_units: list[str],     
        attending_class_years: list[bool],
        attending_users: list[str],
        accountability_method: str, 
    ):

    subcalendar_id = (get_subcalendar_ids())[0];    
    note = accountability_method

    params = {
        'inputFormat':'html'
    }    
    
    payload = {
        'subcalendar_ids':[subcalendar_id],
        'start_dt':start_dt, 
        'end_dt':end_dt,
        'title': title,
        'notes': note
    }
    
    r = session.post('https://api.teamup.com/ksvvx3e1n68gmkz7x8/events', json=payload, params=params)
    return r.status_code,r.text

#fake event test for reference
start = "2024-11-09T13:41:00Z"
end = "2024-11-09T13:41:00Z"
title = "hello"
attending_unit = {"one","two"}
class_years = [False, False, False, False]
accountability = "bing"
print(post_event(start,end,title,attending_unit,class_years,attending_unit,accountability))