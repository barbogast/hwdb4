"""
Author: Benjamin Arbogast
"""

from flask import Blueprint, render_template, request
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import and_
from sqlalchemy import func
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
            li = [H.a(href='/parts?id=%s' % parent_part.id)(parent_part.name)]
            # Omit the divider for the first elemement
            if li_elements:
                li.append(divider)
            li_elements.append(H.li(li))
            parent_part = parent_part.parent_part

        chain = H.ul(class_='breadcrumb')(reversed(li_elements))

        return render_template('parts_detail.html', part=part, parent_part_chain=chain)
    else:
        root_parts = M.db_session.query(M.Part).filter_by(parent_part=None)
        return render_template('parts.html', root_parts=root_parts)

@bp.route('/attr_types')
def attr_types():
    attributes = M.db_session.query(M.AttrType).order_by('name')
    return render_template('attr_types.html', attributes=attributes)

@bp.route('/units')
def units():
    units = M.db_session.query(M.Unit).order_by('name')
    return render_template('units.html', units=units)

@bp.route("/combinations")
def combinations():
    root_parts = M.db_session.query(M.Part).filter(and_(M.Part.content_maps!=None, M.Part.container_maps==None))
    return render_template('combinations.html', root_parts=root_parts)

@bp.route("/attributes")
def attributes():
    stmt = M.db_session.query(M.Attr.id.label('attr_id'),
                              func.count('*').label('cnt')).\
                    join(M.PartAttrMap).\
                    join(M.Part).\
                    group_by(M.Attr.value, M.Attr.attr_type_id).\
                    subquery()

    attributes = M.db_session.query(M.Attr).\
                    join(stmt, M.Attr.id == stmt.c.attr_id).\
                    filter(stmt.c.cnt > 1).\
                    all()
    return render_template('attributes.html', attributes=attributes)
