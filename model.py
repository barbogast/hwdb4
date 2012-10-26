import re
import os

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Boolean, Float, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView


class _DisplayName(object):
    def __unicode__(self):
        return self.name

def _convert_camel_to_undersocre(s):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class _MyBase(object):
    @declared_attr
    def __tablename__(cls):
        return _convert_camel_to_undersocre(cls.__name__)

    id =  Column(Integer, primary_key=True)


Base = declarative_base(cls=_MyBase)


class Unit(_DisplayName, Base):
    name = Column(String, nullable=False, unique=True)
    note = Column(String, nullable=True, unique=False)

class Part(_DisplayName, Base):
    parent_part_id = Column(Integer, ForeignKey('part.id'))
    parent_part = relationship('Part', remote_side='Part.id')
    #children = relationship('Part', backref('parent_part', remote_side=['Part.id']))
    #parent_part = relationship('Part', remote_side=[id])
    #parent_part = relationship('Part', backref=backref('children', remote_side=[id]))
    # TODO: http://docs.sqlalchemy.org/en/rel_0_7/orm/relationships.html#adjacency-list-relationships
    name = Column(String, nullable=False)

class AttrType(_DisplayName, Base):
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

class PartMapping(Base):
    __table_args__ = (UniqueConstraint('container_part_id', 'content_part_id'),)
    container_part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    container_part = relationship(Part, primaryjoin='Part.id==PartMapping.container_part_id', backref='container_map')
    content_part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    content_part = relationship(Part, primaryjoin='Part.id==PartMapping.content_part_id', backref='content_map')
    # Todo: http://docs.sqlalchemy.org/en/rel_0_7/orm/relationships.html#self-referential-many-to-many-relationship
    occurrence = Column(Integer, nullable=False, server_default='1')

class Attr(Base):
    __table_args__ = (UniqueConstraint('attr_type_id', 'part_id'),)
    attr_type_id = Column(Integer, ForeignKey(AttrType.id), nullable=False)
    attr_type = relationship(AttrType, backref='attrs')
    part_id = Column(Integer, ForeignKey(Part.id), nullable=False)
    part = relationship(Part, backref='attrs')
    value = Column(String, nullable=True)
    value_from = Column(Float, nullable=True)
    value_to = Column(Float, nullable=True)

class MultiAttr(Base):
    attr_id = Column(Integer, ForeignKey(Attr.id), nullable=False)
    attr = relationship(Attr, backref='multi_attrs')
    value = Column(String, nullable=False)


def get_initial_objects():
    u_mm = Unit(name='Milimeter')
    u_hz = Unit(name='Herz')
    u_date = Unit(name='Date')
    u_year = Unit(name='Year')
    u_count = Unit(name='Count')
    u_byte = Unit(name='Byte')
    u_transfer = Unit(name='Transfer/Second', note='MT/s (Megatranfer) used with Front side bus')
    u_factor = Unit(name='Factor', note='ie cpu clock multiplier')
    u_volt = Unit(name='Volt')
    u_watt = Unit(name='Watt')
    u_dollar = Unit(name='Dollar')
    u_url = Unit(name='Url')
    u_text = Unit(name='Text')

    p_socket = Part(name='CPU-Socket')
    p_cpu = Part(name='CPU')

    at_name = AttrType(name='Name', unit=u_text)

    # Socket
    #TODO: at_socket_package = AttrType(name='Package', unit=part=p_socket)
    at_year_introduction = AttrType(name='Year of introduction', unit=u_year, part=p_socket)
    at_pin_count = AttrType(name='Pin count', unit=u_count, part=p_socket)
    at_pin_count = AttrType(name='Pin pitch', unit=u_mm, part=p_socket)
    at_bus_speed = AttrType(name='Bus speed', unit=u_hz, from_to=True, part=p_socket)

    # CPU
    at_frequency = AttrType(name='Frequency', unit=u_hz, part=p_cpu)
    at_l2cache = AttrType(name='L2 cache', unit=u_byte, part=p_cpu)
    at_front_side_bus = AttrType(name='Front side bus', unit=u_transfer, part=p_cpu)
    at_clock_multiplier = AttrType(name='Clock multiplier', unit=u_factor, part=p_cpu)
    at_voltage_range = AttrType(name='Voltage range', unit=u_volt, from_to=True, part=p_cpu)
    at_tdp = AttrType(name='Thermal design power', unit=u_watt, part=p_cpu)
    at_release_date = AttrType(name='Release date', unit=u_date, part=p_cpu)
    at_release_price = AttrType(name='Release price', unit=u_dollar, part=p_cpu)
    at_part_number = AttrType(name='Part number', unit=u_text, multi_value=True, part=p_cpu)
    at_url = AttrType(name='URL', unit=u_url, part=p_cpu)

    return locals().values()


def get_engine(filepath):
    #return create_engine('sqlite:///:memory:', echo=debug)
    return create_engine('sqlite:///test.db', echo=debug)


def create_all(engine):
    Base.metadata.create_all(engine)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def init_admin(session, app):
    admin = Admin(app)
    admin.add_view(ModelView(Part, session))
    admin.add_view(ModelView(Attr, session))
    admin.add_view(ModelView(AttrType, session))
    admin.add_view(ModelView(MultiAttr, session))
    admin.add_view(ModelView(PartMapping, session))
    admin.add_view(ModelView(Unit, session))
    return admin


def create_db(engine):
    print 'Create db...',
    create_all(engine)
    session = get_session(engine)

    obj_list = get_initial_objects()

    session.add_all(obj_list)

    from wikipedia import get_all_rows, insert_record
    all_rows = get_all_rows()
    for d in all_rows:
        insert_record(session, d)

    session.commit()
    session.close()
    print ' done'


debug = False
if __name__ == '__main__':
    filepath = 'test.db'
    engine = get_engine(filepath)
    if not os.path.exists(filepath):
        create_db(engine)

    session = get_session(engine)
    app = Flask(__name__)
    init_admin(session, app)
    app.run(port=50001)