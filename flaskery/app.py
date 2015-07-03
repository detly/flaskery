# Copyright 2015 Jason Heeris <jason.heeris@gmail.com>
# 
# This file is part of the 'flaskery' application, and is licensed under the MIT
# license.
import argparse

from flask import Flask, session
from flask_alchy import Alchy
from flaskery.switches.state import SwitchesState

HELP_TEXT = """\
Silly demo app for stomping around Flask."""

# The WSGI thingo.
app = Flask(__name__)

# The configuration.
app.config.from_object('config')

# The database.
db = Alchy(app, Model=SwitchesState)

# OMG flask.
from flaskery.switches.switches import switches_app

# The switches module.
app.register_blueprint(switches_app)

# Let there be data.
db.create_all()

# Make sessions have a timeout.
@app.before_request
def make_session_permanent():
    session.permanent = True

def main():
    """ Parse arguments and get things going for the web interface """
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    
    parser.add_argument(
        '-p', '--port',
        help="Port to serve the interface on.",
        type=int,
        default=5050
    )

    parser.add_argument(
        '-a', '--host',
        help="Host to server the interface on.",
    )

    args = parser.parse_args()

    app.run(port=args.port, host=args.host, debug=True)
