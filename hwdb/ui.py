"""
Author: Benjamin Arbogast
"""

from collections import OrderedDict

import six
from flask import (Blueprint, render_template, render_template_string,
                    request, jsonify)
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


admin_menu = OrderedDict()
for name in sorted(M.get_model_classes()):
    admin_menu['/admin/%sview' % name.lower()] = name


def _render(template, **kwargs):
    """ Adds common template arguments """
    return render_template(template, menu_items=menu_items,
                           admin_menu=admin_menu, **kwargs)


def _render_string(tmpl_str, **kwargs):
    """ Adds common template arguments """
    return render_template_string(tmpl_str, menu_items=menu_items,
                                  admin_menu=admin_menu, **kwargs)


@bp.route("/")
def index():
    li_list = [H.li(H.a(href=href)(name)) for href, name in six.iteritems(menu_items)]
    doc = H.join(
        H.ul(li_list),
        H.a(href="/admin")('Admin')
    )
    return _render_string(base_template, heading='Welcome to HWDB', content=doc)


@bp.route("/parts")
def parts():
    if 'download' in request.args:
        def _get_children(parent_part):
            res = []
            query = M.db_session.query(M.Part).\
            filter(and_(M.Part.parent_part==parent_part,
                        M.Part.is_standard==False,
                        M.Part.is_connector==False)).\
            order_by(M.Part.name)
            for part in query:
                d = {'name': part.name}
                if part.note:
                    d['note'] = part.note

                children = _get_children(part)

                if children:
                    d['children'] = children

                attr_types = []
                for attr_type_map in part.attr_type_maps:
                    attr_types.append(attr_type_map.attr_type.name)
                if attr_types:
                    d['attr_types'] = attr_types

                res.append(d)
            return res

        return jsonify(parts=_get_children(None))


    elif 'id' in request.args:
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
                    container = pc.container_part
                    if container and container.is_standard:
                        if standards:
                            standards.append(', ')
                        a = H.a(href="/parts?id=%s" % container.id)(container.name)
                        standards.append(a)
                container_parts = [': '] + standards if standards else ''

                a = H.a(href="/parts?id=%s" % part.id)(part.name)
                li_elements.append(H.li(a,
                                        H.small(container_parts),
                                        _get_html(part)))
            return H.ul(li_elements)

        doc = H.div(
            _get_html(None),
            H.h3('Export'),
            H.a(href="/parts?download=json")('Download parts as JSON'),
        )
        return _render_string(base_template, heading='Parts', content=doc)


@bp.route('/attr_types')
def attr_types():
    attributes = M.db_session.query(M.AttrType).order_by('name')
    if 'download' in request.args:
        l = []
        for attr in attributes:
            d = {'name': attr.name, 'unit': attr.unit.name}
            if attr.note:
                d['note'] = attr.note
            l.append(d)
        return jsonify(attr_types=l)

    else:
        return _render('attr_types.html', attributes=attributes)


@bp.route('/units')
def units():
    units = M.db_session.query(M.Unit).order_by('name')
    if 'download' in request.args:
        return jsonify(units=[{'name': u.name,
                          'label': u.label,
                          'format': u.format,
                          'note': u.note} for u in units])
    else:
        return _render('units.html', units=units)


@bp.route("/combinations")
def combinations():
    def _render_li(part, sub_parts, level, border=False):
        ul_dict = dict(class_='icons collapsible')
        li_dict = {}
        if level == 1:
            icon = 'icon-minus'
        else:
            icon = 'icon-plus'
            ul_dict['style'] = 'display: none;'

        if level > 1 and border:
            li_dict['class_'] = 'system'

        li_elements = [H.i(class_=icon)()] if sub_parts else []
        li_elements.append(H.a(href="/parts?id=%s" % part.id)(part.name))
        if sub_parts:
            li_elements.append(H.ul(**ul_dict)(sub_parts))
            return H.li(**li_dict)(li_elements)
        else:
            return H.li(**li_dict)(class_='noicon')(li_elements)


    def _render_part(system_part, part, level):
        level += 1
        sub_parts = []
        query = M.db_session.query(M.PartConnection).\
            filter(and_(M.PartConnection.parent_part==system_part,
                        M.PartConnection.container_part==part))
        for part_connection in query:
            contained_part = part_connection.contained_part
            if contained_part.is_system:
                subpart_html = _render_system(contained_part, level)
            else:
                subpart_html = _render_part(system_part, contained_part, level)
            sub_parts.append(subpart_html)

        return _render_li(part, sub_parts, level)


    def _render_system(system_part, level):
        level += 1
        sub_parts = []

        # Get root parts of this system
        query = M.db_session.query(M.PartConnection).\
            filter(and_(M.PartConnection.parent_part==system_part,
                        M.PartConnection.container_part==system_part))
        for part_connection in query:
            contained_part = part_connection.contained_part

            contained_html = _render_part(system_part, contained_part, level)
            sub_parts.append(contained_html)

        return _render_li(system_part, sub_parts, level, border=True)


    query = M.db_session.query(M.Part).\
        filter(M.Part.is_system==True).order_by(M.Part.name)

    li_elements = []
    for part in query:
        li_elements.append(_render_system(part, 1))
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
