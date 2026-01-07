from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer, String, CheckConstraint, UniqueConstraint, Computed

from sqlalchemy.orm import mapped_column, Mapped, relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property

from app.core.db import Base
from app.models.components import Drennage, Alumoflex, Marker, Color, Plastic


class Cable(Base):
    """Модель готового кабеля."""

    article: Mapped[int] = mapped_column(Integer, unique=True)
    outer_diametr: Mapped[float] = mapped_column(Float)
    inner_diametr: Mapped[float] = mapped_column(Float)
    radial: Mapped[float] = mapped_column(Float)

    isolation_id: Mapped[int] = mapped_column(ForeignKey(
        "isolation.id",
        ondelete="CASCADE",
        name='fk_isolation'))
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

    isolation: Mapped["Isolation"] = relationship(back_populates="cable",
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
        CheckConstraint('radial > 0',
                        name='check_radial'),
        CheckConstraint('inner_diametr < outer_diametr',
                        name='inner_smaller_outer'),
        UniqueConstraint('article',
                         name='check_article'),
        UniqueConstraint('article', 'isolation_id', 'construction_id',
                         name='unique_art_and_isolate')
    )


class Isolation(Base):
    """Модель изолированной жилы."""

    # core: Mapped[str] = mapped_column(String(32))  # 3x0.25м (fk на Twisting)
    description: Mapped[str] = mapped_column(Computed("twist.count_wires || 'x' || twist.diametr_wires || twist.metall.name"))
    twist_id: Mapped[int] = mapped_column(ForeignKey("twisting.id",
                                                     name="fk_twisting"))
    outer_diametr: Mapped[float] = mapped_column(Float)
    inner_diametr: Mapped[float] = mapped_column(Float)
    radial: Mapped[float] = mapped_column(Float)

    cable: Mapped[list["Cable"]] = relationship(back_populates="isolation",
                                                cascade="all, delete-orphan",
                                                passive_deletes=True)
    twist: Mapped["Twisting"] = relationship("Twisting",
                                             back_populates="isolation")

    __table_args__ = (
        # CheckConstraint("core ~ '^\\d+x\\d+\\.?\\d*(м|ф|н|л|с|нс)$'",
        #                 name='check_format_core'),
        CheckConstraint('inner_diametr > 0',
                        name='check_inner_diametr'),
        CheckConstraint('radial > 0',
                        name='check_radial'),
        CheckConstraint('inner_diametr < outer_diametr',
                        name='inner_smaller_outer'),
    )


class Twisting(Base):
    """Модель скрученной проволоки."""

    count_wires: Mapped[int] = mapped_column(Integer)
    diametr_wires: Mapped[float] = mapped_column(Float)
    metall_id: Mapped[int] = mapped_column(ForeignKey("metall.id",
                                                      ondelete="CASCADE",
                                                      name="fk_metall"))
    resistance: Mapped[float] = mapped_column(Float)
    step: Mapped[float] = mapped_column(Float)

    metall = relationship('Metall', back_populates='core')
    core = relationship('Isolation', back_populates='twist')


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
