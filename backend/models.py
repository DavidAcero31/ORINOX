from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# ============================================================
# 1. USUARIOS
# ============================================================

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True
    )

    telefono: Mapped[str | None] = mapped_column(String(30))
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    tipo_usuario: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    municipio: Mapped[str | None] = mapped_column(String(100))
    departamento: Mapped[str | None] = mapped_column(String(100))
    direccion: Mapped[str | None] = mapped_column(String(255))

    latitud: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7)
    )

    longitud: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 7)
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    productor: Mapped["Productor | None"] = relationship(
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    comprador: Mapped["Comprador | None"] = relationship(
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    conversaciones: Mapped[list["Conversacion"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    experiencias: Mapped[list["ExperienciaTuristica"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    ofertas_culturales: Mapped[list["OfertaCultural"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan"
    )


# ============================================================
# 2. PRODUCTORES
# ============================================================

class Productor(Base):
    __tablename__ = "productores"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    usuario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    nombre_finca: Mapped[str | None] = mapped_column(String(150))
    tipo_produccion: Mapped[str | None] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(Text())

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="productor"
    )

    productos: Mapped[list["Producto"]] = relationship(
        back_populates="productor",
        cascade="all, delete-orphan"
    )


# ============================================================
# 3. CATEGORIAS
# ============================================================

class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    modulo: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(Text())

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    __table_args__ = (
        UniqueConstraint(
            "nombre",
            "modulo",
            name="uq_categoria_nombre_modulo"
        ),
    )

    productos: Mapped[list["Producto"]] = relationship(
        back_populates="categoria"
    )

    experiencias: Mapped[list["ExperienciaTuristica"]] = relationship(
        back_populates="categoria"
    )

    ofertas_culturales: Mapped[list["OfertaCultural"]] = relationship(
        back_populates="categoria"
    )


# ============================================================
# 4. PRODUCTOS
# ============================================================

class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    productor_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("productores.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    categoria_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("categorias.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(Text())

    unidad_medida: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    precio_unitario: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2)
    )

    cantidad_disponible: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    imagen_url: Mapped[str | None] = mapped_column(
        String(500)
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    productor: Mapped["Productor"] = relationship(
        back_populates="productos"
    )

    categoria: Mapped["Categoria"] = relationship(
        back_populates="productos"
    )

    movimientos: Mapped[list["MovimientoInventario"]] = relationship(
        back_populates="producto",
        cascade="all, delete-orphan"
    )

    matches: Mapped[list["Match"]] = relationship(
        back_populates="producto"
    )


# ============================================================
# 5. MOVIMIENTOS DE INVENTARIO
# ============================================================

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    producto_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("productos.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    tipo_movimiento: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    cantidad: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    motivo: Mapped[str | None] = mapped_column(
        String(255)
    )

    fecha_movimiento: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    producto: Mapped["Producto"] = relationship(
        back_populates="movimientos"
    )

    __table_args__ = (
        Index(
            "ix_movimientos_producto_fecha",
            "producto_id",
            "fecha_movimiento"
        ),
    )


# ============================================================
# 6. COMPRADORES
# ============================================================

class Comprador(Base):
    __tablename__ = "compradores"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    usuario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    nombre_negocio: Mapped[str | None] = mapped_column(
        String(150)
    )

    tipo_negocio: Mapped[str | None] = mapped_column(
        String(100)
    )

    descripcion: Mapped[str | None] = mapped_column(Text())

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="comprador"
    )

    preferencias: Mapped[list["PreferenciaComprador"]] = relationship(
        back_populates="comprador",
        cascade="all, delete-orphan"
    )

    matches: Mapped[list["Match"]] = relationship(
        back_populates="comprador"
    )

    reservas: Mapped[list["Reserva"]] = relationship(
        back_populates="comprador"
    )


# ============================================================
# 7. PREFERENCIAS DEL COMPRADOR
# ============================================================

class PreferenciaComprador(Base):
    __tablename__ = "preferencias_comprador"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    comprador_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("compradores.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    categoria_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("categorias.id", ondelete="SET NULL")
    )

    producto_interes: Mapped[str | None] = mapped_column(
        String(150)
    )

    cantidad_minima: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2)
    )

    cantidad_maxima: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2)
    )

    precio_maximo: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2)
    )

    frecuencia: Mapped[str | None] = mapped_column(
        String(50)
    )

    municipio_preferido: Mapped[str | None] = mapped_column(
        String(100)
    )

    activa: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    comprador: Mapped["Comprador"] = relationship(
        back_populates="preferencias"
    )


# ============================================================
# 8. MATCHES
# ============================================================

class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    producto_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("productos.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    comprador_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("compradores.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    coincidencia_producto: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    coincidencia_cantidad: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    coincidencia_precio: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    coincidencia_ubicacion: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    porcentaje_match: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pendiente"
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    producto: Mapped["Producto"] = relationship(
        back_populates="matches"
    )

    comprador: Mapped["Comprador"] = relationship(
        back_populates="matches"
    )

    __table_args__ = (
        UniqueConstraint(
            "producto_id",
            "comprador_id",
            name="uq_match_producto_comprador"
        ),
    )


# ============================================================
# 9. CONVERSACIONES
# ============================================================

class Conversacion(Base):
    __tablename__ = "conversaciones"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    usuario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    titulo: Mapped[str | None] = mapped_column(
        String(200)
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="conversaciones"
    )

    mensajes: Mapped[list["Mensaje"]] = relationship(
        back_populates="conversacion",
        cascade="all, delete-orphan"
    )


# ============================================================
# 10. MENSAJES
# ============================================================

class Mensaje(Base):
    __tablename__ = "mensajes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    conversacion_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("conversaciones.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    rol: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    contenido: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    modelo_ia: Mapped[str | None] = mapped_column(
        String(100)
    )

    tokens: Mapped[int | None] = mapped_column(
        Integer
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    conversacion: Mapped["Conversacion"] = relationship(
        back_populates="mensajes"
    )

    __table_args__ = (
        Index(
            "ix_mensajes_conversacion_fecha",
            "conversacion_id",
            "creado_en"
        ),
    )


# ============================================================
# 11. EXPERIENCIAS TURISTICAS
# ============================================================

class ExperienciaTuristica(Base):
    __tablename__ = "experiencias_turisticas"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    usuario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    categoria_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("categorias.id", ondelete="SET NULL"),
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text()
    )

    ubicacion: Mapped[str | None] = mapped_column(
        String(255)
    )

    duracion_horas: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2)
    )

    capacidad: Mapped[int | None] = mapped_column(
        Integer
    )

    precio: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2)
    )

    imagen_url: Mapped[str | None] = mapped_column(
        String(500)
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="experiencias"
    )

    categoria: Mapped["Categoria | None"] = relationship(
        back_populates="experiencias"
    )

    reservas: Mapped[list["Reserva"]] = relationship(
        back_populates="experiencia",
        cascade="all, delete-orphan"
    )


# ============================================================
# 12. RESERVAS
# ============================================================

class Reserva(Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    experiencia_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("experiencias_turisticas.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    comprador_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("compradores.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    fecha_reserva: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    cantidad_personas: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pendiente"
    )

    observaciones: Mapped[str | None] = mapped_column(
        Text()
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    experiencia: Mapped["ExperienciaTuristica"] = relationship(
        back_populates="reservas"
    )

    comprador: Mapped["Comprador"] = relationship(
        back_populates="reservas"
    )


# ============================================================
# 13. OFERTAS CULTURALES
# ============================================================

class OfertaCultural(Base):
    __tablename__ = "ofertas_culturales"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    usuario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    categoria_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("categorias.id", ondelete="SET NULL"),
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text()
    )

    municipio: Mapped[str | None] = mapped_column(
        String(100)
    )

    precio: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2)
    )

    imagen_url: Mapped[str | None] = mapped_column(
        String(500)
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="ofertas_culturales"
    )

    categoria: Mapped["Categoria | None"] = relationship(
        back_populates="ofertas_culturales"
    )