#!/usr/bin/env python
"""
Author: Benjamin Arbogast
"""

import argparse
import os

from flask import Flask
from sqlalchemy.orm import scoped_session

import hwdb.model as M
from hwdb import ui
from hwdb import wikipedia


filepath = 'test.db'
dbpath = 'sqlite:///' + filepath
debug = False


def run_admin():
    engine = M.get_engine(dbpath, debug)
    if not os.path.exists(filepath):
        M.create_all(engine)

    M.init_scoped_session(engine)
    app = Flask(__name__)
    app.debug = debug
    app.secret_key = 'Todo'
    M.init_admin(app)
    # Add redirect from / to /admin
    app.add_url_rule('/', 'index', app.view_functions['admin.index'])
    app.run(port=50000)


def run_ui():
    engine = M.get_engine(dbpath, debug)
    M.init_scoped_session(engine)
    app = Flask(__name__)
    app.debug = True
    app.register_blueprint(ui.bp)

    @app.teardown_request
    def shutdown_session(exception=None):
        M.db_session.remove()

    app.run()


def reset_db():
    if os.path.exists(filepath):
        answer = raw_input('Really delete file %r (y,N)? ' % filepath)
        if answer != 'y':
            print 'Abort'
            return
        os.remove(filepath)

    engine = M.get_engine(dbpath, debug)
    print 'Creating db...',
    M.create_all(engine)
    M.init_scoped_session(engine)
    obj_list = M.get_initial_objects()

    M.db_session.add_all(obj_list)
    M.db_session.flush()

    wikitext = wikipedia.fetch_from_wikipedia()
    all_rows = wikipedia.get_all_rows(wikitext)
    for d in all_rows:
        wikipedia.insert_record(d)

    M.db_session.commit()
    M.db_session.close()
    print ' done'



COMMANDS = {
    'run_admin': run_admin,
    'run_ui': run_ui,
    'reset_db': reset_db
}


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('command', choices=COMMANDS.keys())

args = parser.parse_args()

COMMANDS[args.command]()
