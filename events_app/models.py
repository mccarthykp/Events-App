from datetime import datetime
from events_app import db
from sqlalchemy.orm import backref
import enum

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    events_attending = db.relationship('Event', secondary='event_guest', back_populates='guests')

class Event_type(enum.Enum):
    Party = 1
    Study = 2
    Networking = 3
    ALL = 4
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date_and_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_type = db.Column(db.Enum(Event_type), default=Event_type.ALL)
    guests = db.relationship('Guest', secondary='event_guest', back_populates='events_attending')

    def __init__(self, title, description, date_and_time):
        self.title = title
        self.description = description
        self.date_and_time = date_and_time

guest_event_table = db.Table('event_guest',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('guest_id', db.Integer, db.ForeignKey('guest.id'))
)
