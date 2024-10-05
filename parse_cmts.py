from __future__ import annotations

import dataclasses
import json
import pickle
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from xml.etree.ElementTree import Element
from io import StringIO
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    if html is None:
        return None
    s = MLStripper()
    s.feed(html)
    return s.get_data()


plist: dict = pickle.load(open('plist.pickle', 'rb'))
events: list[Element] = pickle.load(open('events.pickle', 'rb'))

for k, v in plist.items():
    print(f"{k}: {len(set(v))}")
    if len(set(v)) > 1:
        print(f"    {list(set(v))[:min(len(set(v)), 5)]}")

for k in set(plist['TypeforCommMaster']):
    print(k.split('|||')[1])


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

    @classmethod
    def from_element(cls, e: Element) -> CMTSEvent | None:
        e_dict = {}
        for prop in e:
            prop_tag = prop.tag.split('}')[1]
            prop_value = prop.text
            e_dict[prop_tag] = prop_value

        raw_type = e_dict['TypeforCommMaster'].split('|||')[1]

        event_type: str | None = None
        class_years = [True, True, True, True]

        if raw_type == "NMF":
            event_type = "nmf"
            e_dict['Title'] = "NMF"

        if "Class Cadets" in raw_type:
            class_years = [False, False, False, False]
            class_years[4 - int(raw_type[0])] = True
            # assume it's an M5
            event_type = "m5"

        if raw_type == "Mandatory Special Event":
            event_type = "other"

        if event_type is None:
            return None

        return cls(
            type=event_type,
            name=e_dict['Title'],
            description=strip_tags(e_dict['Description']),
            time=datetime.fromisoformat(e_dict['EventDate']),
            submission_start=datetime.fromisoformat(e_dict['EventDate']) - timedelta(minutes=15),
            submission_deadline=datetime.fromisoformat(e_dict['EndDate']) + timedelta(hours=1),
            attending_units=["AFCW"],
            attending_class_years=class_years,
            attending_users=[],
            accountability_method="squadron_based"
        )


cmts_ev = []


for e in events:
    ev = CMTSEvent.from_element(e)
    if ev is not None:
        if ev.time < datetime.utcnow().astimezone(UTC):
            continue
        if ev.time > datetime.utcnow().astimezone(UTC) + timedelta(days=28):
            continue
        print(ev)
        cmts_ev.append(ev)


@dataclass
class CMTSEventList:
    events: list[CMTSEvent]


l = CMTSEventList(cmts_ev)

open("cmts.json", "w").write(json.dumps(dataclasses.asdict(l), default=datetime.isoformat))
