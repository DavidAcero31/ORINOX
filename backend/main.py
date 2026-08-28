import os

from dotenv import load_dotenv

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy import text
from sqlalchemy.orm import Session

from google import genai
from google.genai import types

from database import Base, engine, get_db
from models import (
    User,
    Product,
    Buyer,
    Conversation,
    Message,
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

if engine is not None:
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

        result.scalar()

        return {
            "status": "ok",
            "message": "Conexión con PostgreSQL funcionando",
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
        db.query(Product)
        .filter(
            Product.disponible == True
        )
        .all()
    )

    resultado = []

    for producto in productos:

        productor = (
            db.query(User)
            .filter(
                User.id == producto.productor_id
            )
            .first()
        )

        resultado.append(
            {
                "id": producto.id,
                "nombre": producto.nombre,
                "categoria": producto.categoria,
                "descripcion": producto.descripcion,
                "unidad": producto.unidad,
                "cantidad": producto.cantidad,
                "precio": producto.precio,
                "disponible": producto.disponible,
                "productor": (
                    productor.nombre
                    if productor
                    else None
                ),
                "municipio": (
                    productor.municipio
                    if productor
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
        db.query(Buyer)
        .join(
            User,
            Buyer.usuario_id == User.id
        )
        .filter(
            User.activo == True
        )
        .all()
    )

    resultado = []

    for comprador in compradores:

        usuario = (
            db.query(User)
            .filter(
                User.id == comprador.usuario_id
            )
            .first()
        )

        resultado.append(
            {
                "id": comprador.id,
                "empresa": comprador.empresa,
                "categoria_interes": (
                    comprador.categoria_interes
                ),
                "ubicacion": comprador.ubicacion,
                "nombre": (
                    usuario.nombre
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
# CREAR CONVERSACIÓN
# ==========================================

def obtener_conversacion(
    db: Session,
    usuario_id: int | None,
    modulo: str,
):

    conversacion = None

    if usuario_id:

        conversacion = (
            db.query(Conversation)
            .filter(
                Conversation.usuario_id
                == usuario_id,
                Conversation.modulo
                == modulo,
            )
            .order_by(
                Conversation.id.desc()
            )
            .first()
        )

    if conversacion is None:

        conversacion = Conversation(
            usuario_id=usuario_id,
            modulo=modulo,
        )

        db.add(conversacion)

        db.commit()

        db.refresh(conversacion)

    return conversacion


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

    mensaje_usuario = Message(
        conversacion_id=conversacion.id,
        rol="user",
        contenido=request.mensaje,
    )

    db.add(mensaje_usuario)

    db.commit()


    # ======================================
    # OBTENER PRODUCTOS
    # ======================================

    productos = (
        db.query(Product)
        .filter(
            Product.disponible == True
        )
        .limit(20)
        .all()
    )


    productos_contexto = ""

    for producto in productos:

        productor = (
            db.query(User)
            .filter(
                User.id
                == producto.productor_id
            )
            .first()
        )

        productos_contexto += (
            f"- Producto: {producto.nombre}\n"
            f"  Categoría: {producto.categoria}\n"
            f"  Cantidad: {producto.cantidad} "
            f"{producto.unidad}\n"
            f"  Precio: "
            f"${producto.precio:,.0f} COP\n"
            f"  Productor: "
            f"{productor.nombre if productor else 'No disponible'}\n"
            f"  Municipio: "
            f"{productor.municipio if productor else 'No disponible'}\n"
            f"\n"
        )


    if not productos_contexto:

        productos_contexto = (
            "No existen productos disponibles "
            "registrados actualmente."
        )


    # ======================================
    # OBTENER COMPRADORES
    # ======================================

    compradores = (
        db.query(Buyer)
        .join(
            User,
            Buyer.usuario_id == User.id
        )
        .filter(
            User.activo == True
        )
        .limit(20)
        .all()
    )


    compradores_contexto = ""

    for comprador in compradores:

        usuario = (
            db.query(User)
            .filter(
                User.id
                == comprador.usuario_id
            )
            .first()
        )

        compradores_contexto += (
            f"- Empresa: "
            f"{comprador.empresa or 'No especificada'}\n"
            f"  Categoría de interés: "
            f"{comprador.categoria_interes or 'No especificada'}\n"
            f"  Ubicación: "
            f"{comprador.ubicacion or 'No especificada'}\n"
            f"  Contacto: "
            f"{usuario.nombre if usuario else 'No disponible'}\n"
            f"\n"
        )


    if not compradores_contexto:

        compradores_contexto = (
            "No existen compradores activos "
            "registrados actualmente."
        )


    # ======================================
    # HISTORIAL DE CONVERSACIÓN
    # ======================================

    mensajes_previos = (
        db.query(Message)
        .filter(
            Message.conversacion_id
            == conversacion.id
        )
        .order_by(
            Message.id.desc()
        )
        .limit(10)
        .all()
    )

    mensajes_previos.reverse()


    historial = ""

    for mensaje in mensajes_previos:

        historial += (
            f"{mensaje.rol}: "
            f"{mensaje.contenido}\n"
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
   representan información de la plataforma.
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
"""


    # ==========================================
    # LLAMADA A GEMINI
    # ==========================================

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=instrucciones
        )
    )

    return {
        "respuesta": response.text,
        "modulo": request.modulo
    }