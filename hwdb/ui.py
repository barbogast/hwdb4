"""
Author: Benjamin Arbogast
"""

from flask import Blueprint, render_template, request
from sqlalchemy.orm import scoped_session, sessionmaker
from flaskext.htmlbuilder import html as H

import hwdb.model as M


bp = Blueprint('ui', __name__, template_folder='templates')

@bp.route("/")
def index():
    return render_template('index.html')

@bp.route("/parts")
def parts():
    if 'id' in request.args:
        part = M.db_session.query(M.Part).filter_by(id=request.args['id']).one()
        has_parent = bool(part.parent_part)

        # Generate breadcrumb for part
        li_elements = []
        divider = H.span(class_='divider')(H.i(class_='icon-chevron-right')(), ' ')

        parent_part = part
        while parent_part:
            li = [H.a(href='/part?id=%s' % parent_part.id)(parent_part.name)]
            # Omit the divider for the first elemement
            if parent_parts_html:
                li.append(divider)
            li_elements.append(H.li(li))
            parent_part = parent_part.parent_part

        chain = H.ul(class_='breadcrumb')(reversed(li_elements))

        return render_template('parts_detail.html', part=part, parent_part_chain=chain)
    else:
        root_parts = M.db_session.query(M.Part).filter_by(parent_part=None)
        return render_template('parts.html', root_parts=root_parts)

@bp.route('/attributes')
def attributes():
    attributes = M.db_session.query(M.AttrType).order_by('name')
    return render_template('attributes.html', attributes=attributes)

@bp.route('/units')
def units():
    units = M.db_session.query(M.Unit).order_by('name')
    return render_template('units.html', units=units)
