#!/usr/bin/env python
"""
Author: Benjamin Arbogast
"""

import argparse
import os
import subprocess

from flask import Flask, send_file
from sqlalchemy.orm import scoped_session
from flask.ext.admin import Admin, expose, AdminIndexView
from flask.ext.admin.contrib.sqlamodel import ModelView
import sadisplay

import hwdb.model as M
from hwdb import ui
from hwdb import wikipedia
from hwdb import init_data


filepath = 'test.db'
dbpath = 'sqlite:///' + filepath
debug = False


def init_admin(app):
    # Custom AdminIndexView to change the rendered template
    class MyIndexView(AdminIndexView):
        @expose()
        def index(self):
            return self.render('admin_index.html')

    admin = Admin(app, index_view=MyIndexView())
    for name, klass in sorted(M.get_model_classes().items()):
        admin.add_view(ModelView(klass, M.db_session))


def run_ui(args):
    engine = M.get_engine(dbpath, debug)
    M.init_scoped_session(engine)
    app = Flask(__name__, static_folder='hwdb/static', template_folder='hwdb/templates')
    app.debug = True
    app.secret_key = 'Todo'
    app.register_blueprint(ui.bp)
    init_admin(app)
    app.run()


def reset_db(args):
    if os.path.exists(filepath):
        if not args.force:
            answer = raw_input('Really delete file %r (y,N)? ' % filepath)
            if answer != 'y':
                print 'Abort'
                return
        os.remove(filepath)

    engine = M.get_engine(dbpath, debug)
    print 'Creating db...'
    M.create_all(engine)
    M.init_scoped_session(engine)

    M.db_session.add_all(init_data.get_units())
    M.db_session.add_all(init_data.get_parts())
    M.db_session.add_all(init_data.get_standards())
    M.db_session.flush()
    M.db_session.add_all(init_data.get_attr_types())
    M.db_session.flush()
    M.db_session.add_all(init_data.get_common_attributes())
    M.db_session.flush()

    M.db_session.add_all(init_data.get_objects_computer_BA())
    M.db_session.add_all(init_data.get_objects_computer_alt())
    M.db_session.flush()

    if args.wikipedia:
        wikitext = wikipedia.fetch_from_wikipedia()
        all_rows = wikipedia.get_all_rows(wikitext)
        for d in all_rows:
            wikipedia.insert_record(d)

    M.db_session.commit()
    M.db_session.close()
    print 'Creation of db was successful'
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
        print 'Info: Conversion of dot file %r to png failed. Maybe the program "dot" (Graphviz) is missing?' % dot_filename
    else:
        os.remove(dot_filename)
        print 'Written ER-diagram to file %r' % png_filename


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
