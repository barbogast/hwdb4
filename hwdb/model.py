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
 * Vendors: A vendor of a Part could be represented as attribute or as parent_part.
   Which one is better? Vendors as attribute is bad because there is no single entry which
   represents the vendor but multiple attributes containing the name of the vendor.
   Vendors as parents are bad because the parent-child-relationship of Parts represents
   the category by hardware type, not by vendor. Maybe an extra table? Or with the N:M-Mapping of Parts?
 * Enums: Should AttrTypes be able to store allowed values?
   For example: casing_size=>(mini_tower, Midi_tower, big_tower)
 * Does Parts inherit the connections to Attributes and Attribute Types from its
   parents?
 * How should be stored, that Motherboard xyz has one cpu socket 1155 (which
   support Standard Socket 1155), 5 PCIe x16-Slots (which support PCIe x16), 5x Audio, ...?
 * new column: Part.anonymous (type=boolean) to store if the name of a specific
   Part is unknown
"""

import re
import os

from sqlalchemy import (Column, Integer, String, ForeignKey, UniqueConstraint,
                        Boolean, Float, Table, create_engine, and_)
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base, declared_attr


db_session = None


class _DisplayNameMixin(object):
    """ Adds a default representation for SQLAlchemy objects """
    def __unicode__(self):
        return self.name

    @classmethod
    def search(cls, name):
        """
        Searches a record by the given name. If multiple records with the
        given name are found, an Exception is raised
        """
        # TOOD
        raise NotImplemented()


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


class Unit(_DisplayNameMixin, Base):
    """
    The unit which describes the values of Attributes. Examples: meter, volt
    """
    name = Column(String, nullable=False, unique=True)
    note = Column(String, nullable=True, unique=False)


class Part(_DisplayNameMixin, Base):
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
    contains the 'CPU-Socket QQ'.
    As a standard it represents a standard like 'ATX' or 'PCI Express 3.0'. The
    parent relation is used to group standards. For example the standard 'ATX'
    could have the parent 'Casing standard'. To indicate that a Part supports a
    standard the Part should `contain` the standard like it contains other Parts.
    attr_type_maps are a n:m relation to AttrTypes using PartAttrTypeMap to
    mark which Attr Types are allowed for this Part
    """
    parent_part_id = Column(Integer, ForeignKey('part.id'))
    parent_part = relationship('Part', remote_side='Part.id', backref='children')
    name = Column(String, nullable=False)
    note = Column(String, nullable=True, unique=False)
    is_standard = Column(Boolean)

    @classmethod
    def init(cls, attributes={}, **kwargs):
        """
        Create a Part and return it. Attributes is expected to be a
        dict (key=AttrType-object, value=value). For each key/value pair
        an Attr object will be created with the given AttrType object
        and value and associated with the new Part.
        """
        part = cls(**kwargs)
        for attr_type, value in attributes.iteritems():
            attr = Attr.init(part=part, value=value, attr_type=attr_type)
        return part

    def add_content_part(self, contained_part):
        """
        Adds the given Part to the list of Parts contained by this Part.
        """
        # TODO
        raise NotImplemented()


class AttrType(_DisplayNameMixin, Base):
    """
    An AttrType describes an type of attribute. It will be associated with an
    Attr which is in turn associated with a part and has the actual value.
    Examples are 'Bus speed', 'Frequency', 'Release date'.
    TODO: describe the connection with part and from_to/multi_value
    """
    name = Column(String, nullable=False, unique=False)
    note = Column(String, nullable=True, unique=False)
    from_to = Column(Boolean)
    multi_value = Column(Boolean)
    unit_id = Column(Integer, ForeignKey(Unit.id), nullable=False)
    unit = relationship(Unit, backref='attr_types')

    @classmethod
    def init(cls, parts, **kwargs):
        """
        Creates + returns an AttrType object with a PartAttrTypeMap for every
        given Part.
        """
        attr_type = cls(**kwargs)
        maps = [PartAttrTypeMap(part=part, attr_type=attr_type) for part in parts]

        attr_type.part_maps = maps
        return attr_type


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


class PartMap(Base):
    """
    A m:n connection from Part to itself. Used to describe that a Part contains
    other Parts. For examples see docstring of Part.
    TODO: Position and occurrence rule each other out.
    """
    __table_args__ = (UniqueConstraint('container_part_id', 'content_part_id'),)
    container_part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    container_part = relationship(Part, primaryjoin='Part.id==PartMap.container_part_id', backref='content_maps')
    content_part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    content_part = relationship(Part, primaryjoin='Part.id==PartMap.content_part_id', backref='container_maps')
    occurrence = Column(Integer, nullable=False, server_default='1')
    position = Column(Integer)


class Attr(Base):
    """
    A attr represents an actual attribute of a Part. It is associated with an
    AttrType and a Part and contains the actual value of the attribute.
    TODO: describe value_to, value_from
    """
    __table_args__ = (UniqueConstraint('part_attr_type_mapping_id', 'part_id'),)
    part_attr_type_mapping_id = Column(Integer, ForeignKey(PartAttrTypeMap.id), nullable=False)
    part_attr_type_mapping = relationship(PartAttrTypeMap, backref='attrs')
    part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    part = relationship(Part, backref='attrs')
    value = Column(String, nullable=True)
    value_from = Column(Float, nullable=True)
    value_to = Column(Float, nullable=True)

    @classmethod
    def init(cls, attr_type, part, **kwargs):
        """
        Creates + returns an Attr object. The PartAttrTypeMap is looked up with
        the given AttrType and Part in the parents of the Part.
        """
        mapping = search_PartAttrTypeMap(attr_type, part.parent_part)
        if not mapping:
            raise Exception(('No PartAttrTypeMap is found for attr_type '
                             '"%s" and part "%s"' % (attr_type.__unicode__(),
                                                     part.__unicode__())))

        attr = cls(part_attr_type_mapping=mapping, part=part, **kwargs)
        return attr


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


def search_PartAttrTypeMap(attr_type, part):
    """
    Searches a part and its parent recursivly for an PartAttrTypeMap
    with the given attr_type.

    :return: PartAttrTypeMap object or None"""
    mapping = db_session.query(PartAttrTypeMap).\
        filter(and_(PartAttrTypeMap.attr_type==attr_type, PartAttrTypeMap.part==part)).first()

    if mapping:
        return mapping
    elif part.parent_part:
        return search_PartAttrTypeMap(attr_type, part.parent_part)
    else:
        return None


def get_attr_types_without_part():
    """
    Returns a list AttrTypes which are not associated with a Part and therefore not
    usable
    """
    # TODO
    pass
