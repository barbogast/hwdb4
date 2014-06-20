#!/usr/bin/env python
"""
Author: Benjamin Arbogast
"""

import argparse
import os
import subprocess

import six
from flask import Flask, send_file
from sqlalchemy.orm import scoped_session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin, AdminIndexView
from flask.ext.admin.contrib.sqla import ModelView
from flask_debugtoolbar import DebugToolbarExtension
import sadisplay

import hwdb.model as M
from hwdb import ui
from hwdb import wikipedia
from hwdb import init_data


data_path = os.environ.get('DATA_PATH', '.')

filepath = os.path.join(data_path, 'hwdb4.sqlite')
dbpath = 'sqlite:///' + filepath

debug = False


def init_admin(app):
    admin = Admin(app, index_view=AdminIndexView(template='admin_index.html'))
    for name, klass in sorted(M.get_model_classes().items()):
        admin.add_view(ModelView(klass, M.db_session))


def run_ui(args):
    app = Flask(__name__, static_folder='hwdb/static', template_folder='hwdb/templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
    app.config['SQLALCHEMY_ECHO'] = False
    app.debug = True
    app.secret_key = 'Todo'
    app.register_blueprint(ui.bp)

    db = SQLAlchemy(app)
    M.db_session = db.session
    init_admin(app)
    if False:
        toolbar = DebugToolbarExtension(app)
    app.run()


def reset_db(args):
    if os.path.exists(filepath):
        if not args.force:
            answer = six.moves.input('Really delete file %r (y,N)? ' % filepath)
            if answer != 'y':
                print('Abort')
                return
        os.remove(filepath)

    engine = M.get_engine(dbpath, debug)
    print('Creating db...')
    M.enable_auto_add_objects_to_session()
    M.create_all(engine)
    M.init_scoped_session(engine)

    init_data.import_units()
    M.db_session.flush()
    init_data.import_attr_types()
    M.db_session.flush()
    init_data.import_parts()
    init_data.import_standards()
    M.db_session.flush()
    init_data.import_connectors()
    init_data.import_subparts()
    M.db_session.flush()
    init_data.import_systems()

    if args.wikipedia:
        wikitext = wikipedia.fetch_from_wikipedia()
        all_rows = wikipedia.get_all_rows(wikitext)
        for d in all_rows:
            wikipedia.insert_record(d)

    M.db_session.commit()
    M.db_session.close()
    print('Creation of db was successful')
    _make_ER()


def _make_ER():
    desc = sadisplay.describe(M.get_model_classes().values())
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
        print('Info: Conversion of dot file %r to png failed. Maybe the program "dot" (Graphviz) is missing?' % dot_filename)
    else:
        os.remove(dot_filename)
        print ('Written ER-diagram to file %r' % png_filename)


COMMANDS = {
    'run_ui': run_ui,
    'reset_db': reset_db,
}


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('command', choices=COMMANDS.keys(), help='Run one of the commands')
parser.add_argument('--force', action="store_true", help='Force yes on user input for the given command')
parser.add_argument('--wikipedia', action="store_true", help='Parse Pentium 4 tables from Wikipedia')

args = parser.parse_args()

COMMANDS[args.command](args)
