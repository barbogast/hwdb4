"""
Author: Benjamin Arbogast

Open questions:
 * at the moment it is not possible to define which attribute_types are allowed
   for which part. Should this be possible? This way, a admin could restrict the
   attributes which can be set for a given part. This could be implemented as
   a mapping table from Part to AttrType. Then each part could have the attributes which
   are associated with its parent part. This would replace the FK from AttrType to Part
 * saving single values and ranges in table Attr:
    - store single values in a "value"-column and min/max in extra columns
    - store single values in min. fill max only for ranges (problem: ranges with max=unlimited)
    - store single values in min and max (min=max)
    - store the values in a postgres array. array length 1 = single value, array length 2 = min/max, array length > 2 = multi value
    * should Attr.value be an (Postgres-) Array so the columns Attr.value_from,
      Attr.value_to and the table MultiAttr could be removed?
"""

import re
import os

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Boolean, Float, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base, declared_attr


db_session = None


class _DisplayNameMixin(object):
    def __unicode__(self):
        return self.name

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


Base = declarative_base(cls=_MyBase)


class StandardSet(_DisplayNameMixin, Base):
    name = Column(String, nullable=False, unique=True)
    note = Column(String, nullable=True, unique=False)

class Standard(_DisplayNameMixin, Base):
    name = Column(String, nullable=False, unique=True)
    note = Column(String, nullable=True, unique=False)
    standard_set_id = Column(Integer, ForeignKey(StandardSet.id))
    standard_set = relationship(StandardSet, backref='standards')

class Unit(_DisplayNameMixin, Base):
    name = Column(String, nullable=False, unique=True)
    note = Column(String, nullable=True, unique=False)

class Part(_DisplayNameMixin, Base):
    parent_part_id = Column(Integer, ForeignKey('part.id'))
    parent_part = relationship('Part', remote_side='Part.id', backref='children')
    #children = relationship('Part', backref('parent_part', remote_side=['Part.id']))
    #parent_part = relationship('Part', remote_side=[id])
    #parent_part = relationship('Part', backref=backref('children', remote_side=[id]))
    # TODO: http://docs.sqlalchemy.org/en/rel_0_7/orm/relationships.html#adjacency-list-relationships
    name = Column(String, nullable=False)
    note = Column(String, nullable=True, unique=False)

class AttrType(_DisplayNameMixin, Base):
    __table_args__ = (UniqueConstraint('name', 'part_id'),)
    name = Column(String, nullable=False, unique=False)
    note = Column(String, nullable=True, unique=False)
    from_to = Column(Boolean)
    multi_value = Column(Boolean)
    # Reference to a Part to declare that this AttrType should only be used for the given Part
    part_id = Column(Integer, ForeignKey(Part.id), nullable=True)
    part = relationship(Part, backref='attr_types')
    unit_id = Column(Integer, ForeignKey(Unit.id), nullable=False)
    unit = relationship(Unit, backref='attr_types')
    standard_set_id = Column(Integer, ForeignKey(StandardSet.id))
    standard_set = relationship(StandardSet, backref='attr_types')

class PartMapping(Base):
    __table_args__ = (UniqueConstraint('container_part_id', 'content_part_id'),)
    container_part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    container_part = relationship(Part, primaryjoin='Part.id==PartMapping.container_part_id', backref='container_map')
    content_part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    content_part = relationship(Part, primaryjoin='Part.id==PartMapping.content_part_id', backref='content_map')
    # Todo: http://docs.sqlalchemy.org/en/rel_0_7/orm/relationships.html#self-referential-many-to-many-relationship
    occurrence = Column(Integer, nullable=False, server_default='1')
    position = Column(Integer)

class Attr(Base):
    __table_args__ = (UniqueConstraint('attr_type_id', 'part_id'),)
    attr_type_id = Column(Integer, ForeignKey(AttrType.id), nullable=False)
    attr_type = relationship(AttrType, backref='attrs')
    part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    part = relationship(Part, backref='attrs')
    value = Column(String, nullable=True)
    value_from = Column(Float, nullable=True)
    value_to = Column(Float, nullable=True)
    standard_id = Column(Integer, ForeignKey(Standard.id))
    standard = relationship(Standard, backref='attrs')

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


_objects = locals()
def get_model_classes():
    models = []
    for k, obj in sorted(_objects.items()):
        if isinstance(obj, type) and issubclass(obj, Base) and not obj is Base:
            models.append(obj)
    return models
