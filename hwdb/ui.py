"""
Author: Benjamin Arbogast
"""

from flask import Blueprint, render_template, render_template_string, request
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import and_
from sqlalchemy import func
from flaskext.htmlbuilder import html as H

import hwdb.model as M


bp = Blueprint('ui', __name__, template_folder='templates')

base_template = '''
{% extends "base.html" %}
{% block body %}
  <div class="container">
    <h1>{{heading}}</h1>
    {{content}}
  </div>
{% endblock %}'''


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
            a = H.a(href='/parts?id=%s' % parent_part.id)(parent_part.name)
            li_elements.append(H.li(divider, a))
            parent_part = parent_part.parent_part
        chain = H.join(reversed(li_elements))
        return render_template('parts_detail.html', part=part, parent_part_chain=chain)
    else:
        def _get_html(parent_part):
            query = M.db_session.query(M.Part).\
                filter(and_(M.Part.parent_part==parent_part,
                            M.Part.is_standard==False)).\
                order_by(M.Part.name)
            li_elements = []
            for part in query:
                standards = []
                for pc in part.container_maps:
                    standard = pc.container_part
                    if not standard.is_standard:
                        continue
                    if standards:
                        standards.append(', ')
                    a = H.a(href="/parts?id=%s" % standard.id)(standard.name)
                    standards.append(a)
                container_parts = [': '] + standards if standards else ''

                a = H.a(href="/parts?id=%s" % part.id)(part.name)
                li_elements.append(H.li(a,
                                        H.small(container_parts),
                                        _get_html(part)))
            return H.ul(li_elements)
        doc = _get_html(None)
        return render_template_string(base_template, heading='Parts', content=doc)

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
    def _get_html(part):
        li_elements = []
        for mapping in part.contained_maps:
            if not mapping.contained_part.is_standard:
                li_elements.append(_get_html(mapping.contained_part))
        return H.li(
                H.a(href="/parts?id=%s" % part.id)(part.name),
                H.ul(li_elements)
            )

    query = M.db_session.query(M.Part).\
        filter(and_(M.Part.contained_maps!=None,
                    M.Part.container_maps==None,
                    M.Part.is_standard==False))

    li_elements = []
    for part in query:
        li_elements.append(_get_html(part))
    doc = H.ul(li_elements)
    return render_template_string(base_template, heading='Combinations', content=doc)

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

@bp.route("/standards")
def standards():
    def _get_html(parent_part):
        lis = []
        query = M.db_session.query(M.Part).\
            filter(and_(M.Part.parent_part==parent_part,
                        M.Part.is_standard==True)).\
            order_by(M.Part.name)

        for standard in query:
            # remove " (Standard)" from the end of the name
            name = standard.name[:-1*len(' (Standard)')]
            parts = []
            for pc in standard.contained_maps:
                if parts:
                    parts.append(', ')
                a = H.a(href="/parts?id=%s" % pc.contained_part.id)(pc.contained_part.name)
                parts.append(a)
            contained_parts = [': '] + parts if parts else ''

            lis.append(H.li(
                H.a(href="/parts?id=%s" % standard.id)(name),
                contained_parts,
                _get_html(standard)))
        return H.ul(lis)

    doc = _get_html(None)
    return render_template_string(base_template, heading='Standards', content=doc)
