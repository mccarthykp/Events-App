import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest, guest_event_table

from events_app import app, db

main = Blueprint('main', __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""
    events = Event.query.all()
    return render_template('index.html', events=events)

@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')

        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            return render_template('create.html', 
                error='Incorrect datetime format! Please try again.')

        event = Event(title=new_event_title, description=new_event_description, date_and_time=date_and_time)
        db.session.add(event)
        db.session.commit()

        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')

@main.route('/event/<int:event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""

    event = Event.query.get_or_404(event_id)
    guests = db.session.query(guest_event_table).filter_by(event_id=event.id)
    return render_template('event_detail.html', title=event.title, event=event, guests=guests)

@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')
    event = Event.query.get_or_404(event_id)

    if is_returning_guest:
        exists = db.session.query(Guest.id).filter_by(name=guest_name).first() is not None

        if exists:
            update_guest = Guest.query.filter_by(name=guest_name).one()
            update_guest.events_attending.append(event)
            db.session.add(update_guest)
            db.session.commit()
        else:
            return render_template('event_detail.html', error='error', title=event.title, event=event)
    else:
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')

        new_guest = Guest(name=guest_name, email=guest_email, phone=guest_phone)
        new_guest.events_attending.append(event)

        db.session.add(new_guest)
        db.session.commit()
    
    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id))

@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    guest = Guest.query.get_or_404(guest_id)
    return render_template('guest_detail.html', guest=guest)
