"""
Author: Benjamin Arbogast

Open questions:
 * saving single values and ranges in table Attr:
    - store single values in a "value"-column and min/max in extra columns
    - store single values in min. fill max only for ranges (problem: ranges with max=unlimited)
    - store single values in min and max (min=max)
    - store the values in a postgres array. array length 1 = single value, array length 2 = min/max, array length > 2 = multi value
    * should Attr.value be an (Postgres-) Array so the columns Attr.value_from,
      Attr.value_to and the table MultiAttr could be removed?
 * Does Parts inherit the connections to Attributes and Attribute Types from its
   parents?
 * Change the table Unit to a Postgres Enum
"""

import re
import os

from sqlalchemy import (Column, Integer, String, ForeignKey, UniqueConstraint,
                        Boolean, Float, Table, create_engine, and_)
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.declarative import declarative_base, declared_attr


db_session = None
SERVER_DEFAULT_FALSE = '0'

class _TableWithNameColMixin(object):
    """ Adds a default representation for SQLAlchemy objects """
    def __unicode__(self):
        return self.name

    @classmethod
    def search(cls, name):
        """
        Searches a record by the given name. If multiple records with the
        given name are found, an Exception is raised
        """
        try:
            return db_session.query(cls).filter_by(name=name).one()
        except NoResultFound:
            raise Exception('No %s found with name %r' % (cls.__name__, name))
        except MultipleResultsFound:
            raise Exception('Multiple %ss found with name %r' % (cls.__name__, name))


def _convert_camel_to_underscore(s):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class _MyBase(object):
    """
    Base class for SQLAlchemy model classes:
    Generate the "__tablename__" attribute from the name of the class
    and add an id attribute
    """
    @declared_attr
    def __tablename__(cls):
        return _convert_camel_to_underscore(cls.__name__)

    id =  Column(Integer, primary_key=True)

_model_classes = {}
Base = declarative_base(cls=_MyBase, class_registry=_model_classes)


class Unit(_TableWithNameColMixin, Base):
    """
    The unit which describes the values of Attributes. Examples: meter, volt
    Format should be a Python format string which will be used to display values
    with this unit.
    """
    name = Column(String, nullable=False, unique=True)
    label = Column(String, nullable=False, unique=True)
    format = Column(String, nullable=False, server_default='%(unit)s')
    note = Column(String, nullable=True, unique=False)


# Note: this is used to store attributes which were inserted into the
# database. It is used to access Attr objects before they are commited
# to the database. This way newly created Attr objects can be shared
# between different parts before they are inserted. The key for this
# dict is '%s.%s' % (attr_type.id, value)
_attr_cache = {}

class Part(_TableWithNameColMixin, Base):
    """
    A Part represents a hardware part or an IT standard.
    As a hardware part it can be an abstract part like 'cpu' or a specific part
    like 'Pentium 4 Willamette 1.3'.
    A hardware part can have a parent to categorize similar parts (See the class
    PartMapping). For example a 'Pentium 4 Willamette 1.3' has the parent
    'Pentium 4 Willamette' which has in turn the parent 'Pentium 4' which has
    the parent 'CPU'.
    A part can contain multiple other parts. For example a 'Laptop Sony XX'
    contains the 'Mainboard YY' and the 'Display ZZ'. The 'Mainboard YY'
    contains the 'CPU-Socket QQ'. The relation is done using the class PartMap.
    As a standard it represents a standard like 'ATX' or 'PCI Express 3.0'. The
    parent relation is used to group standards. For example the standard 'ATX'
    could have the parent 'Casing standard'. To indicate that a Part supports a
    standard the Part should `contain` the standard like it contains other Parts.
    attr_type_maps are a n:m relation to AttrTypes using PartAttrTypeMap to
    mark which Attr Types are allowed for this Part
    """
    __table_args__ = (UniqueConstraint('id', 'parent_part_id'),)
    parent_part_id = Column(Integer, ForeignKey('part.id'))
    parent_part = relationship('Part', remote_side='Part.id', backref='children')
    name = Column(String, nullable=False)
    note = Column(String, nullable=True, unique=False)
    is_standard = Column(Boolean, nullable=False, server_default=SERVER_DEFAULT_FALSE)
    is_connector = Column(Boolean, nullable=False, server_default=SERVER_DEFAULT_FALSE)

    @classmethod
    def init(cls, name, parent_part_name, attributes={}, is_standard=False, is_connector=False):
        """
        Create a Part and return it.
        :param attributes: dict (key=AttrType-name, value=value). For each
          key/value pair:
            - an AttrType object will be looked up by the given name
            - an Attr will be looked up with the AttrType and the given value
            - if no Attr was found, it will be created
            - a PartAttrMap will be created with the new Part and Attr
            - the PartAttrMap will be created to the new Part
        :param parent_part: A Part with this name will be searched and set as
          parent_part
        """
        parent_part = Part.search(parent_part_name)
        part = cls(name=name, parent_part=parent_part, is_standard=is_standard,
                   is_connector=is_connector)
        for attr_type_name, value in attributes.iteritems():
            attr_type = AttrType.search(attr_type_name)
            if not search_PartAttrTypeMap(part, attr_type):
                raise Exception('AttrType %s is not registered for %s' % (attr_type.name, part.name))

            key = '%s.%s' % (attr_type.id, value)
            attr = _attr_cache.get(key)
            if not attr:
                attr = db_session.query(Attr).\
                    filter(and_(Attr.attr_type==attr_type, Attr.value==value)).\
                    first()
            if not attr:
                attr = Attr(value=value, attr_type=attr_type)
                _attr_cache[key] = attr
            attr_map = PartAttrMap(part=part, attr=attr)
            part.attr_maps.append(attr_map)
        return part

    def add_part_connection(self, container_part, contained_part, quantity=1):
        """ Add a PartConnection as child of this Part """
        part_conn = PartConnection(container_part=container_part,
                                   contained_part=contained_part,
                                   quantity=quantity)
        self.part_connection_children.append(part_conn)


def add_standards_to_part(part, *standard_names):
    """
    Add the Standards (=Parts) looked up by the given standard names to the
    given Part
    """
    for standard_name in standard_names:
        standard = Part.search(standard_name)
        mapping = PartConnection(container_part=standard, contained_part=part)
        part.container_maps.append(mapping)


class AttrType(_TableWithNameColMixin, Base):
    """
    An AttrType describes an type of attribute. It will be associated with an
    Attr which is in turn associated with a part and has the actual value.
    Examples are 'Bus speed', 'Frequency', 'Release date'.
    TODO: describe the connection with part and from_to/multi_value
    """
    name = Column(String, nullable=False, unique=False)
    note = Column(String, nullable=True, unique=False)
    from_to = Column(Boolean, nullable=False, server_default=SERVER_DEFAULT_FALSE)
    multi_value = Column(Boolean, nullable=False, server_default=SERVER_DEFAULT_FALSE)
    unit_id = Column(Integer, ForeignKey(Unit.id), nullable=False)
    unit = relationship(Unit, backref='attr_types')

    @classmethod
    def init(cls, name, unit_name, from_to=False, note=None, multi_value=False):
        """
        Creates + returns an AttrType object with a PartAttrTypeMap for every
        given part name. The corresponding Part object and the Unit object will
        be looked up by the given names.
        """
        unit = Unit.search(unit_name)
        attr_type = db_session.query(cls).filter(and_(cls.name==name,cls.unit==unit)).first()
        if not attr_type:

            attr_type = cls(name=name,
                            unit=unit,
                            from_to=from_to,
                            note=note,
                            multi_value=multi_value)
        return attr_type

    def add_to_parts(self, *part_names):
        for part_name in part_names:
            part = Part.search(part_name)
            part_map = PartAttrTypeMap(part=part, attr_type=self)
            self.part_maps.append(part_map)
        return self


class PartAttrTypeMap(Base):
    """
    Relates AttrTypes with Parts to show which attribute types are allowed for a
    Part
    """
    __table_args__ = (UniqueConstraint('part_id', 'attr_type_id'),)
    part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    part = relationship(Part, backref='attr_type_maps')
    attr_type_id = Column(Integer, ForeignKey(AttrType.id), nullable=False)
    attr_type = relationship(AttrType, backref='part_maps')

    def __unicode__(self):
        return '%s - %s' % (self.part.name, self.attr_type.name)


class PartConnection(Base):
    """
    This table is used to describe that one or multiple Parts are contained in /
    connected to another Part.
    Examples: CPU contained in Socket, Socket contained to Motherboard.
    The connetions can be in turn assigned to a Part using the column parent_part.
    Example: 'Socket X' connected with 'CPU Y' belongs to 'PC Z'.
    The column quantity can be used if the same Part is contained multiple times.
    """
    __table_args__ = (UniqueConstraint('container_part_id', 'contained_part_id', 'parent_part_id'),)
    container_part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    container_part = relationship(Part, backref='contained_maps', primaryjoin='Part.id==PartConnection.container_part_id')
    contained_part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    contained_part = relationship(Part, backref='container_maps', primaryjoin='Part.id==PartConnection.contained_part_id')
    parent_part_id = Column(Integer, ForeignKey(Part.id))
    parent_part = relationship(Part, backref='part_connection_children', primaryjoin='Part.id==PartConnection.parent_part_id')
    quantity = Column(Integer, nullable=False, server_default='1')


class Attr(Base):
    """
    A attr represents an actual attribute of a Part. It is associated with an
    AttrType and a Part and contains the actual value of the attribute.
    TODO: describe value_to, value_from
    """
    __table_args__ = (UniqueConstraint('attr_type_id', 'value'),)
    attr_type_id = Column(Integer, ForeignKey(AttrType.id), nullable=False)
    attr_type = relationship(AttrType, backref='attrs')
    value = Column(String, nullable=True) # TODO: nullable should be False
    value_from = Column(Float, nullable=True)
    value_to = Column(Float, nullable=True)

    def __unicode__(self):
        return '%s: %s' % (self.attr_type.name, self.value)


class PartAttrMap(Base):
    __table_args__ = (UniqueConstraint('part_id', 'attr_id'),)
    part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    part = relationship(Part, backref='attr_maps')
    attr_id = Column(Integer, ForeignKey(Attr.id), nullable=False)
    attr = relationship(Attr, backref='part_maps')


class MultiAttr(Base):
    attr_id = Column(Integer, ForeignKey(Attr.id), nullable=False)
    attr = relationship(Attr, backref='multi_attrs')
    value = Column(String, nullable=False)


def get_engine(dbpath, debug):
    #return create_engine('sqlite:///:memory:', echo=debug)
    return create_engine(dbpath, echo=debug)


def create_all(engine):
    Base.metadata.create_all(engine)


def init_scoped_session(engine):
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    global db_session
    db_session = scoped_session(Session)


def init_session(engine):
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    global db_session
    db_session = Session()


def get_model_classes():
    return _model_classes


def search_PartAttrTypeMap(part, attr_type):
    """
    Searches a part and its parent recursivly for an PartAttrTypeMap
    with the given attr_type.

    :return: PartAttrTypeMap object or None"""
    mapping = db_session.query(PartAttrTypeMap).\
        filter(and_(PartAttrTypeMap.attr_type==attr_type, PartAttrTypeMap.part==part)).first()

    if mapping:
        return mapping
    elif part.parent_part:
        return search_PartAttrTypeMap(part.parent_part, attr_type)
    else:
        return None


def get_attr_types_without_part():
    """
    Returns a list AttrTypes which are not associated with a Part and therefore not
    usable
    """
    # TODO
    pass
