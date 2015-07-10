# Copyright 2015 Jason Heeris <jason.heeris@gmail.com>
# 
# This file is part of the 'flaskery' application, and is licensed under the MIT
# license.
from flask import Blueprint, render_template, request, session, make_response, redirect, url_for, flash
from flask.ext.wtf import Form
from wtforms import SubmitField

import sqlalchemy.orm.exc as sql_exc

from flaskery.switches.state import SwitchesState

switches_app = Blueprint('switches', __name__, url_prefix='', template_folder='templates')

class StateForm(Form):
    """ Creates a WTForm interface for changing states. """
    set_one = SubmitField()
    set_two = SubmitField()

def format_bytes(data):
    """
    Converts a sequence of bytes to a formatted string, where each byte is
    represented as hexadecimal.
    """
    return ' '.join('{:02X}'.format(byte) for byte in data)

def label_for(name, value):
    """
    English label for changing the state of a button named `name` when the state
    is `value`.
    """
    words = {
        True:  "Falsify",
        False: "Truthify"
    }

    return "{:s} thing {:s}…".format(words[value], name)

def make_the_thing_exist(session):
    """
    If the session contains a valid ID for a state, return the state. Otherwise
    create a new state, update the session with the ID, and return the new
    state. 
    """
    # If the browser doesn't remember a session, make a new one
    create_state = False

    if 'state' not in session:
        create_state = True
    else:
        state_key = session['state']

        state_query = SwitchesState.query.filter_by(key = state_key)
        
        try:
            state = state_query.one()
        except sql_exc.NoResultFound:
            create_state = True

        # sql_exc.MultipleResultsFound is actually an error.

    if create_state:
        state = SwitchesState()
        session['state'] = state.key
        state.save()
        state.session().commit()

    assert(state != None)
    assert(session['state'] == state.key)

    return state

@switches_app.route("/")
def root():
    """ Web interface landing page. """
    state = make_the_thing_exist(session)
    form = StateForm(request.form)

    template = render_template(
        'index.html',
        state=state,
        form=StateForm(),
        label_for=label_for,
        format_bytes=format_bytes)

    return template

@switches_app.route("/change", methods=('POST',))
def change():
    """ Interface for changing switch state. """
    state = make_the_thing_exist(session)

    form = StateForm(request.form)

    if form.validate_on_submit():
        change_state_one = form.set_one.data
        change_state_two = form.set_two.data

        state.one = bool(state.one) ^ bool(change_state_one)
        state.two = bool(state.two) ^ bool(change_state_two)

        state.save()
        state.session().commit()

    return redirect(url_for('.root'))
