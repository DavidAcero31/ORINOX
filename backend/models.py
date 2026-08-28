from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
    )

    tipo: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="productor",
    )

    municipio: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    departamento: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    productos: Mapped[list["Product"]] = relationship(
        back_populates="productor",
        cascade="all, delete-orphan",
    )

    comprador: Mapped["Buyer | None"] = relationship(
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Product(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    productor_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    categoria: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    unidad: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="kg",
    )

    cantidad: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    precio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    disponible: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    productor: Mapped["User"] = relationship(
        back_populates="productos",
    )


class Buyer(Base):
    __tablename__ = "compradores"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        unique=True,
        nullable=False,
    )

    empresa: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    categoria_interes: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    ubicacion: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    usuario: Mapped["User"] = relationship(
        back_populates="comprador",
    )


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id"),
        nullable=False,
    )

    comprador_id: Mapped[int] = mapped_column(
        ForeignKey("compradores.id"),
        nullable=False,
    )

    puntuacion: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        default="pendiente",
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


class Conversation(Base):
    __tablename__ = "conversaciones"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=True,
    )

    modulo: Mapped[str] = mapped_column(
        String(30),
        default="productivo",
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    mensajes: Mapped[list["Message"]] = relationship(
        back_populates="conversacion",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "mensajes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversacion_id: Mapped[int] = mapped_column(
        ForeignKey("conversaciones.id"),
        nullable=False,
        index=True,
    )

    rol: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    contenido: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    conversacion: Mapped["Conversation"] = relationship(
        back_populates="mensajes",
    )