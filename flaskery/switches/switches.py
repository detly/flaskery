# Copyright 2015 Jason Heeris <jason.heeris@gmail.com>
# 
# This file is part of the 'flaskery' application, and is licensed under the MIT
# license.
from flask import Blueprint, render_template, request, session, make_response, redirect, url_for, flash
from flask.ext.wtf import Form
from wtforms import SubmitField

from flaskery.switches.state import SwitchesState

switches_app = Blueprint('switches', __name__, url_prefix='', template_folder='templates')

class StateForm(Form):
    """ Creates a WTForm interface for changing states. """
    set_one = SubmitField()
    set_two = SubmitField()

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

def make_the_thing_exist(session, db):
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
        state_id = session['state']
        state = SwitchesState.query.get(state_id)

        if state == None:
            # Maybe this is an error instead?
            create_state = True

    if create_state:
        state = SwitchesState()
        db.session.add(state)
        db.session.commit()
        session['state'] = state.id

    assert(state != None)
    assert(state.id != None)
    assert(session['state'] == state.id)

    return state

# Not a fan of this.
from flaskery.app import db

@switches_app.route("/")
def root():
    """ Web interface landing page. """
    state = make_the_thing_exist(session, db)
    form = StateForm(request.form)

    template = render_template(
        'index.html',
        state=state,
        form=StateForm(),
        label_for=label_for)

    return template

@switches_app.route("/change", methods=('POST',))
def change():
    """ Interface for changing switch state. """
    state = make_the_thing_exist(session, db)

    form = StateForm(request.form)

    if form.validate_on_submit():
        change_state_one = form.set_one.data
        change_state_two = form.set_two.data

        state.one = bool(state.one) ^ bool(change_state_one)
        state.two = bool(state.two) ^ bool(change_state_two)

        db.session.commit()

    return redirect(url_for('.root'))
