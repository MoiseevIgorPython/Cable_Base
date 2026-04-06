from typing import Optional

from core.db import Base
from sqlalchemy import (BigInteger, CheckConstraint, Computed, Float,
                        ForeignKey, Integer, String, UniqueConstraint, cast,
                        event, func, select)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from .components import Alumoflex, Color, Drennage, Marker, Plastic


class Cable(Base):
    """Модель готового кабеля."""

    title: Mapped[str] = mapped_column(String,
                                       nullable=False,
                                       server_default="untitled")
    article: Mapped[int] = mapped_column(BigInteger, unique=True)
    outer_diametr: Mapped[float] = mapped_column(Float,
                                                 nullable=True)
    inner_diametr: Mapped[float] = mapped_column(Float,
                                                 nullable=True)

    twist_id: Mapped[int] = mapped_column(ForeignKey(
        "twisting.id",
        ondelete="CASCADE",
        name='fk_twisting'))
    construction_id: Mapped[int] = mapped_column(ForeignKey(
        "construction.id",
        ondelete="CASCADE",
        name='fk_construction'))
    drennage_id: Mapped[int] = mapped_column(ForeignKey(
        "drennage.id",
        name='fk_drennage'))
    alumoflex_id: Mapped[int] = mapped_column(ForeignKey(
        "alumoflex.id",
        name='fk_alumoflex'))
    marker_id: Mapped[Optional[int]] = mapped_column(ForeignKey(
        "marker.id",
        name='fk_marker'),
        nullable=True)

    twisting: Mapped["Twisting"] = relationship(back_populates="cable",
                                                lazy='joined')
    construction: Mapped["Construction"] = relationship(back_populates="cable",
                                                        lazy='joined')
    drennage: Mapped["Drennage"] = relationship(back_populates="cable",
                                                lazy='joined')
    alumoflex: Mapped["Alumoflex"] = relationship(back_populates="cable",
                                                  lazy='joined')
    marker: Mapped[Optional["Marker"]] = relationship(back_populates="cable",
                                                      lazy='joined')

    __table_args__ = (
        CheckConstraint('outer_diametr > 0',
                        name='check_outer_diametr'),
        CheckConstraint('inner_diametr > 0',
                        name='check_inner_diametr'),
        CheckConstraint('inner_diametr < outer_diametr',
                        name='inner_smaller_outer'),
        UniqueConstraint('article',
                         name='check_article'),
        CheckConstraint('article BETWEEN 100000000 AND 999999999',
                        name="check_article_9_digits"),
    )

    def __repr__(self):
        return self.title


class Twisting(Base):
    """Модель скрученной проволоки."""

    count_wires: Mapped[int] = mapped_column(Integer)
    diametr_wires: Mapped[float] = mapped_column(Float)
    diametr_twist: Mapped[float] = mapped_column(
        Float,
        Computed('CEIL((diametr_wires * sqrt(count_wires)) * 100) / 100'))
    metall_id: Mapped[int] = mapped_column(ForeignKey("metall.id",
                                                      ondelete="CASCADE",
                                                      name="fk_metall"))
    resistance: Mapped[float] = mapped_column(Float)
    step: Mapped[float] = mapped_column(Float)

    metall = relationship('Metall',
                          lazy='joined',
                          back_populates='core')
    cable: Mapped["Cable"] = relationship('Cable',
                                          cascade="all, delete-orphan",
                                          back_populates="twisting")

    def __str__(self):
        return f"{self.count_wires}x{self.diametr_wires} {self.metall.name}"


class Construction(Base):
    """Модель конструкций кабелей."""

    name: Mapped[str] = mapped_column(String(64), unique=True)
    color_id: Mapped[int] = mapped_column(ForeignKey(
        'color.id',
        name='fk_color'))
    isolate_plastic_id: Mapped[int] = mapped_column(ForeignKey(
        'plastic.id',
        name='fk_isolate_plastic'))
    shell_plastic_id: Mapped[int] = mapped_column(ForeignKey(
        'plastic.id',
        name='fk_shell_plastic'))
    radial_isolate: Mapped[float] = mapped_column(Float, nullable=False)
    radial_shell: Mapped[float] = mapped_column(Float, nullable=False)

    cable: Mapped[list[Cable]] = relationship(
        'Cable',
        back_populates='construction',
        lazy='selectin')
    color: Mapped["Color"] = relationship(
        'Color',
        back_populates='constructions',
        lazy='joined')
    isolate_plastic: Mapped["Plastic"] = relationship(
        'Plastic',
        foreign_keys=[isolate_plastic_id],
        back_populates='isolate',
        lazy='joined')
    shell_plastic: Mapped["Plastic"] = relationship(
        'Plastic',
        foreign_keys=[shell_plastic_id],
        back_populates='shell',
        lazy='joined')

    __table_args__ = (
        UniqueConstraint('name', name='check_name_consrtruction'),
        )

    def __str__(self):
        return self.name

    @hybrid_property
    def sort_number(self):
        try:
            return int(self.name.split('-')[1]) if '-' in self.name and self.name.split('-')[1].isdigit() else 0
        except (IndexError, ValueError):
            return 0

    @sort_number.expression
    def sort_number(cls):
        return cast(
            func.substring(cls.name, func.strpos(cls.name, '-') + 1),
            Integer)


@event.listens_for(Cable, 'before_insert')
@event.listens_for(Cable, 'before_update')
def create_fields_cable(mapper, connection, target):
    session = Session(bind=connection)
    twist = session.execute(select(Twisting)
                            .where(Twisting.id == target.twist_id))
    construction = session.execute(
        select(Construction)
        .where(Construction.id == target.construction_id))

    twist = twist.scalar_one_or_none()
    construction = construction.scalar_one_or_none()
    inner_diametr = (twist.diametr_twist + construction.radial_isolate * 2) * 2
    outer_diametr = inner_diametr + construction.radial_shell * 2
    title = f"{construction.name} {twist.count_wires}x"
    f"{twist.diametr_wires} {twist.metall.name}"
    target.inner_diametr = round(inner_diametr, 2)
    target.outer_diametr = round(outer_diametr, 2)
    target.title = title


@event.listens_for(Construction, 'after_update')
def receive_after_update(mapper, connection, target):
    session = Session(bind=connection)
    cables = session.execute(
        select(Cable)
        .where(Cable.construction_id == target.id))
    cables = cables.scalars().all()
    for cable in cables:
        twist = session.execute(
            select(Twisting)
            .where(Twisting.id == cable.twist_id))
        twist = twist.scalar_one_or_none()
        inner_diametr = (twist.diametr_twist + float(target.radial_isolate) * 2) * 2
        outer_diametr = inner_diametr + float(target.radial_shell) * 2

        cable.title = f"{target.name} {twist.count_wires}x"
        f"{twist.diametr_wires} {twist.metall.name}"
        cable.inner_diametr = round(inner_diametr, 2)
        cable.outer_diametr = round(outer_diametr, 2)
        session.commit()
