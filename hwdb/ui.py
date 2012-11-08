"""
Author: Benjamin Arbogast
"""

from collections import OrderedDict

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

menu_items = OrderedDict([
    ('/parts', 'Parts'),
    ('/attr_types', 'Attribute Types'),
    ('/attributes', 'Attributes'),
    ('/units', 'Units'),
    ('/combinations', 'Combinations'),
    ('/standards', 'Standards'),
])

def _render(template, **kwargs):
    """ Adds common template arguments """
    return render_template(template, menu_items=menu_items, **kwargs)

def _render_string(tmpl_str, **kwargs):
    """ Adds common template arguments """
    return render_template_string(tmpl_str, menu_items=menu_items, **kwargs)

@bp.route("/")
def index():
    li_list = [H.li(H.a(href=href)(name)) for href, name in menu_items.iteritems()]
    doc = H.join(
        H.ul(li_list),
        H.a(href="/admin")('Admin')
    )
    return _render_string(base_template, heading='Welcome to HWDB', content=doc)

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
        return _render('parts_detail.html', part=part, parent_part_chain=chain)
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
        return _render_string(base_template, heading='Parts', content=doc)

@bp.route('/attr_types')
def attr_types():
    attributes = M.db_session.query(M.AttrType).order_by('name')
    return _render('attr_types.html', attributes=attributes)

@bp.route('/units')
def units():
    units = M.db_session.query(M.Unit).order_by('name')
    return _render('units.html', units=units)

@bp.route("/combinations")
def combinations():
    def _get_html(part, level):
        li_elements = []
        for mapping in part.contained_maps:
            if not mapping.contained_part.is_standard:
                li_elements.append(_get_html(mapping.contained_part, level+1))

        if level == 1:
            style, icon = '', 'icon-minus'
        else:
            style, icon = 'display: none;', 'icon-plus'
        li = [H.i(class_=icon)()] if li_elements else []
        li.append(H.a(href="/parts?id=%s" % part.id)(part.name))
        li.append(H.ul(class_='icons collapsible', style=style)(li_elements))
        return H.li(li)

    query = M.db_session.query(M.Part).\
        filter(and_(M.Part.contained_maps!=None,
                    M.Part.container_maps==None,
                    M.Part.is_standard==False)).\
        order_by(M.Part.name)

    li_elements = []
    for part in query:
        li_elements.append(_get_html(part, 1))
    doc = H.ul(class_='icons collapsible')(li_elements)
    return _render_string(base_template, heading='Combinations', content=doc)

@bp.route("/attributes")
def attributes():
    stmt = M.db_session.query(M.Attr.id.label('attr_id'),
                              func.count('*').label('cnt')).\
                    join(M.PartAttrMap).\
                    join(M.Part).\
                    group_by(M.Attr.value, M.Attr.attr_type_id).\
                    subquery()

    attributes = M.db_session.query(M.Attr).\
                    join(M.AttrType).\
                    join(stmt, M.Attr.id == stmt.c.attr_id).\
                    filter(stmt.c.cnt > 1).\
                    order_by(M.AttrType.name).\
                    all()
    return _render('attributes.html', attributes=attributes)

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
    return _render_string(base_template, heading='Standards', content=doc)
