import os

from dotenv import load_dotenv

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy import text
from sqlalchemy.orm import Session

from google import genai
from google.genai import types

from database import engine, get_db
from models import (
    Base,
    Usuario,
    Productor,
    Producto,
    Comprador,
    PreferenciaComprador,
    Match,
    Conversacion,
    Mensaje,
    Categoria,
    MovimientoInventario,
    ExperienciaTuristica,
    Reserva,
    OfertaCultural,
)


# ==========================================
# CONFIGURACIÓN
# ==========================================

load_dotenv("clave-agent.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "No se encontró GEMINI_API_KEY en clave-agent.env"
    )


# ==========================================
# CLIENTE GEMINI
# ==========================================

client = genai.Client(
    api_key=api_key
)


# ==========================================
# CREAR TABLAS
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# APLICACIÓN FASTAPI
# ==========================================

app = FastAPI(
    title="LLANO IA API",
    version="1.0.0",
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# MODELO DE PETICIÓN
# ==========================================

class ChatRequest(BaseModel):

    mensaje: str

    modulo: str = "productivo"

    usuario_id: int | None = None


# ==========================================
# RUTA PRINCIPAL
# ==========================================

@app.get("/")
def root():

    return {
        "status": "ok",
        "message": "LLANO IA API funcionando",
    }


# ==========================================
# PRUEBA DE BASE DE DATOS
# ==========================================

@app.get("/api/db-test")
def database_test(
    db: Session = Depends(get_db)
):

    try:

        result = db.execute(
            text("SELECT 1")
        )

        resultado = result.scalar()

        return {
            "status": "ok",
            "message": "Conexión con PostgreSQL funcionando",
            "resultado": resultado,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error conectando con PostgreSQL: {str(e)}",
        )


# ==========================================
# PRODUCTOS
# ==========================================

@app.get("/api/productos")
def obtener_productos(
    db: Session = Depends(get_db)
):

    productos = (
        db.query(Producto)
        .filter(
            Producto.activo == True
        )
        .all()
    )

    resultado = []

    for producto in productos:

        productor = (
            db.query(Productor)
            .filter(
                Productor.id == producto.productor_id
            )
            .first()
        )

        usuario = None

        if productor:

            usuario = (
                db.query(Usuario)
                .filter(
                    Usuario.id == productor.usuario_id
                )
                .first()
            )

        categoria = (
            db.query(Categoria)
            .filter(
                Categoria.id == producto.categoria_id
            )
            .first()
        )

        resultado.append(
            {
                "id": producto.id,

                "nombre": producto.nombre,

                "categoria": (
                    categoria.nombre
                    if categoria
                    else None
                ),

                "descripcion": producto.descripcion,

                "unidad": producto.unidad_medida,

                "cantidad": float(
                    producto.cantidad_disponible
                ),

                "precio": (
                    float(producto.precio_unitario)
                    if producto.precio_unitario is not None
                    else None
                ),

                "disponible": producto.activo,

                "imagen_url": producto.imagen_url,

                "productor": (
                    f"{usuario.nombre} {usuario.apellido}"
                    if usuario
                    else None
                ),

                "municipio": (
                    usuario.municipio
                    if usuario
                    else None
                ),

                "departamento": (
                    usuario.departamento
                    if usuario
                    else None
                ),
            }
        )

    return resultado


# ==========================================
# COMPRADORES
# ==========================================

@app.get("/api/compradores")
def obtener_compradores(
    db: Session = Depends(get_db)
):

    compradores = (
        db.query(Comprador)
        .join(
            Usuario,
            Comprador.usuario_id == Usuario.id
        )
        .filter(
            Usuario.activo == True
        )
        .all()
    )

    resultado = []

    for comprador in compradores:

        usuario = (
            db.query(Usuario)
            .filter(
                Usuario.id == comprador.usuario_id
            )
            .first()
        )

        preferencias = (
            db.query(PreferenciaComprador)
            .filter(
                PreferenciaComprador.comprador_id
                == comprador.id,
                PreferenciaComprador.activa == True
            )
            .all()
        )

        intereses = []

        for preferencia in preferencias:

            intereses.append(
                preferencia.producto_interes
            )

        resultado.append(
            {
                "id": comprador.id,

                "empresa": comprador.nombre_negocio,

                "tipo_negocio": comprador.tipo_negocio,

                "descripcion": comprador.descripcion,

                "categoria_interes": intereses,

                "ubicacion": (
                    usuario.direccion
                    if usuario
                    else None
                ),

                "nombre": (
                    f"{usuario.nombre} {usuario.apellido}"
                    if usuario
                    else None
                ),

                "municipio": (
                    usuario.municipio
                    if usuario
                    else None
                ),

                "departamento": (
                    usuario.departamento
                    if usuario
                    else None
                ),
            }
        )

    return resultado


# ==========================================
# CREAR / OBTENER CONVERSACIÓN
# ==========================================

def obtener_conversacion(
    db: Session,
    usuario_id: int | None,
    modulo: str,
):

    conversacion = None

    if usuario_id:

        conversacion = (
            db.query(Conversacion)
            .filter(
                Conversacion.usuario_id
                == usuario_id
            )
            .order_by(
                Conversacion.id.desc()
            )
            .first()
        )

    if conversacion is None:

        # La tabla conversaciones actual
        # no tiene columna modulo.
        conversacion = Conversacion(
            usuario_id=usuario_id,
            titulo=f"Conversación - {modulo}",
        )

        db.add(conversacion)

        db.commit()

        db.refresh(conversacion)

    return conversacion


# ==========================================
# CONSTRUIR CONTEXTO DE PRODUCTOS
# ==========================================

def obtener_contexto_productos(
    db: Session
):

    productos = (
        db.query(Producto)
        .filter(
            Producto.activo == True
        )
        .limit(20)
        .all()
    )

    contexto = ""

    for producto in productos:

        productor = (
            db.query(Productor)
            .filter(
                Productor.id
                == producto.productor_id
            )
            .first()
        )

        usuario = None

        if productor:

            usuario = (
                db.query(Usuario)
                .filter(
                    Usuario.id
                    == productor.usuario_id
                )
                .first()
            )

        categoria = (
            db.query(Categoria)
            .filter(
                Categoria.id
                == producto.categoria_id
            )
            .first()
        )

        cantidad = producto.cantidad_disponible

        precio = producto.precio_unitario

        contexto += (
            f"- Producto: {producto.nombre}\n"
            f"  Categoría: "
            f"{categoria.nombre if categoria else 'No especificada'}\n"
            f"  Cantidad: "
            f"{cantidad} "
            f"{producto.unidad_medida}\n"
            f"  Precio: "
            f"${float(precio):,.0f} COP\n"
            f"  Productor: "
            f"{usuario.nombre if usuario else 'No disponible'}\n"
            f"  Municipio: "
            f"{usuario.municipio if usuario else 'No disponible'}\n"
            f"\n"
        )

    if not contexto:

        contexto = (
            "No existen productos disponibles "
            "registrados actualmente."
        )

    return contexto


# ==========================================
# CONSTRUIR CONTEXTO DE COMPRADORES
# ==========================================

def obtener_contexto_compradores(
    db: Session
):

    compradores = (
        db.query(Comprador)
        .join(
            Usuario,
            Comprador.usuario_id == Usuario.id
        )
        .filter(
            Usuario.activo == True
        )
        .limit(20)
        .all()
    )

    contexto = ""

    for comprador in compradores:

        usuario = (
            db.query(Usuario)
            .filter(
                Usuario.id
                == comprador.usuario_id
            )
            .first()
        )

        preferencias = (
            db.query(PreferenciaComprador)
            .filter(
                PreferenciaComprador.comprador_id
                == comprador.id,
                PreferenciaComprador.activa == True
            )
            .all()
        )

        intereses = []

        for preferencia in preferencias:

            if preferencia.producto_interes:

                intereses.append(
                    preferencia.producto_interes
                )

        contexto += (
            f"- Empresa: "
            f"{comprador.nombre_negocio or 'No especificada'}\n"
            f"  Tipo de negocio: "
            f"{comprador.tipo_negocio or 'No especificado'}\n"
            f"  Productos de interés: "
            f"{', '.join(intereses) if intereses else 'No especificados'}\n"
            f"  Contacto: "
            f"{usuario.nombre if usuario else 'No disponible'}\n"
            f"  Municipio: "
            f"{usuario.municipio if usuario else 'No disponible'}\n"
            f"  Departamento: "
            f"{usuario.departamento if usuario else 'No disponible'}\n"
            f"\n"
        )

    if not contexto:

        contexto = (
            "No existen compradores activos "
            "registrados actualmente."
        )

    return contexto


# ==========================================
# HISTORIAL DE CONVERSACIÓN
# ==========================================

def obtener_historial(
    db: Session,
    conversacion_id: int
):

    mensajes = (
        db.query(Mensaje)
        .filter(
            Mensaje.conversacion_id
            == conversacion_id
        )
        .order_by(
            Mensaje.id.desc()
        )
        .limit(10)
        .all()
    )

    mensajes.reverse()

    historial = ""

    for mensaje in mensajes:

        historial += (
            f"{mensaje.rol}: "
            f"{mensaje.contenido}\n"
        )

    return historial


# ==========================================
# CHAT CON LLANO IA
# ==========================================

@app.post("/api/chat")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    # ======================================
    # CONVERSACIÓN
    # ======================================

    conversacion = obtener_conversacion(
        db=db,
        usuario_id=request.usuario_id,
        modulo=request.modulo,
    )


    # ======================================
    # GUARDAR MENSAJE DEL USUARIO
    # ======================================

    mensaje_usuario = Mensaje(
        conversacion_id=conversacion.id,
        rol="user",
        contenido=request.mensaje,
    )

    db.add(mensaje_usuario)

    db.commit()


    # ======================================
    # DATOS DE POSTGRESQL
    # ======================================

    productos_contexto = obtener_contexto_productos(
        db
    )

    compradores_contexto = obtener_contexto_compradores(
        db
    )

    historial = obtener_historial(
        db,
        conversacion.id
    )


    # ======================================
    # INSTRUCCIONES DE LLANO IA
    # ======================================

    instrucciones = """
Eres LLANO IA, el asistente inteligente de una
plataforma para fortalecer la economía productiva,
cultural y turística de los Llanos de Colombia,
especialmente Casanare y Meta.

Tienes tres módulos:

PRODUCTIVO:
- agricultura
- ganadería
- piscicultura
- productos
- inventario
- compradores
- comercialización

CULTURAL:
- cultura llanera
- artesanías
- gastronomía
- música
- tradiciones
- oficios
- experiencias culturales

TURÍSTICO:
- destinos
- experiencias
- actividades
- turismo rural
- gastronomía
- reservas
- paquetes turísticos

REGLAS:

1. Responde siempre en español.
2. Sé claro, amable y práctico.
3. Ayuda al usuario a avanzar hacia una acción concreta.
4. No inventes compradores, precios, reservas,
   productores o datos.
5. Los datos proporcionados desde PostgreSQL
   representan información real de la plataforma.
6. Utiliza los datos de PostgreSQL cuando
   respondas preguntas relacionadas con ellos.
7. Si un dato no existe en PostgreSQL,
   dilo claramente.
8. Nunca inventes información para completar
   datos faltantes.
9. Ten en cuenta el contexto de Casanare
   y los Llanos.
10. No digas que eres ChatGPT.
11. Eres LLANO IA.
"""


    # ======================================
    # PROMPT
    # ======================================

    prompt = f"""
MÓDULO ACTUAL:
{request.modulo}


========================================
PRODUCTOS DISPONIBLES
========================================

{productos_contexto}


========================================
COMPRADORES REGISTRADOS
========================================

{compradores_contexto}


========================================
HISTORIAL DE CONVERSACIÓN
========================================

{historial}


========================================
NUEVO MENSAJE DEL USUARIO
========================================

{request.mensaje}


========================================
INSTRUCCIÓN
========================================

Responde al usuario utilizando la información
disponible en la base de datos.

Si pregunta por productos, cantidades,
precios, productores o compradores,
utiliza los datos reales proporcionados.

Si la información solicitada no está disponible,
indícalo claramente.

No inventes datos.
"""


    # ======================================
    # GEMINI
    # ======================================

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=instrucciones,
            ),
        )

        respuesta = response.text


    except Exception as e:

        db.rollback()

        return {
            "respuesta": (
                "Lo siento, ocurrió un problema "
                "al consultar LLANO IA."
            ),
            "error": str(e),
            "modulo": request.modulo,
        }


    # ======================================
    # GUARDAR RESPUESTA DE IA
    # ======================================

    mensaje_ia = Mensaje(
        conversacion_id=conversacion.id,
        rol="assistant",
        contenido=respuesta,
        modelo_ia="gemini-3.6-flash",
    )

    db.add(mensaje_ia)

    db.commit()


    # ======================================
    # RESPUESTA
    # ======================================

    return {
        "respuesta": respuesta,
        "modulo": request.modulo,
        "conversacion_id": conversacion.id,
    }