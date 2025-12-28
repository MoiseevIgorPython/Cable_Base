from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core.db import Base, ComponentName


class Drennage(Base, ComponentName):
    cable = relationship('Cable', back_populates='drennage')

    __table_args__ = (
        CheckConstraint("name ~ '^\d+x\d+\.?\d*м$'", name='check_format_drennage_name'),
    )


class Alumoflex(Base, ComponentName):
    cable = relationship('Cable', back_populates='alumoflex')


class Marker(Base):
    text = mapped_column(String(64))
    cable: Mapped['Cable'] = relationship('Cable', back_populates='marker')


class Color(Base, ComponentName):
    constructions = relationship('Construction', back_populates='color')


class Plastic(Base, ComponentName):
    isolate = relationship('Construction',
                           foreign_keys='[Construction.isolate_plastic_id]',
                           back_populates='isolate_plastic')
    shell = relationship('Construction',
                         foreign_keys='[Construction.shell_plastic_id]',
                         back_populates='shell_plastic')
