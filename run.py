#!/usr/bin/env python
"""
Author: Benjamin Arbogast
"""

import argparse
import os
import subprocess

from flask import Flask
from sqlalchemy.orm import scoped_session
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView
import sadisplay

import hwdb.model as M
from hwdb import ui
from hwdb import wikipedia
from hwdb.init_data import get_initial_objects


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

    model_classes = M.get_model_classes()
    admin = Admin(app)
    for klass in model_classes:
        admin.add_view(ModelView(klass, M.db_session))

    # Add redirect from / to /admin
    app.add_url_rule('/', 'index', app.view_functions['admin.index'])
    app.run(port=50000)


def run_ui():
    engine = M.get_engine(dbpath, debug)
    M.init_scoped_session(engine)
    app = Flask(__name__, static_folder='hwdb/static')
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
    print 'Creating db...'
    M.create_all(engine)
    M.init_scoped_session(engine)
    obj_list = get_initial_objects()

    M.db_session.add_all(obj_list)
    M.db_session.flush()

    wikitext = wikipedia.fetch_from_wikipedia()
    all_rows = wikipedia.get_all_rows(wikitext)
    for d in all_rows:
        wikipedia.insert_record(d)

    M.db_session.commit()
    M.db_session.close()
    print 'done'
    _make_ER()



def _make_ER():
    desc = sadisplay.describe(M.get_model_classes())
    path = 'hwdb/static'
    if not os.path.exists(path):
        os.mkdir(path)

    dot_filename = os.path.join(path, 'schema.dot')
    png_filename = os.path.join(path, 'schema.png')
    if os.path.exists(dot_filename): os.remove(dot_filename)
    if os.path.exists(png_filename): os.remove(png_filename)
    open(dot_filename, 'w').write(sadisplay.dot(desc))
    try:
        subprocess.check_call("dot -Tpng %s > %s" % (dot_filename, png_filename), shell=True)
    except subprocess.CalledProcessError:
        print 'Error: Conversion of dot file %r to png failed. Maybe the program "dot" is missing?' % dot_filename
    else:
        os.remove(dot_filename)
        print 'Written ER-diagram to file %r' % png_filename


COMMANDS = {
    'run_admin': run_admin,
    'run_ui': run_ui,
    'reset_db': reset_db,
}


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('command', choices=COMMANDS.keys())

args = parser.parse_args()

COMMANDS[args.command]()
