import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types


# ==========================================
# CONFIGURACIÓN DE VARIABLES DE ENTORNO
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

client = genai.Client(api_key=api_key)


# ==========================================
# APLICACIÓN FASTAPI
# ==========================================

app = FastAPI(
    title="LLANO IA API",
    version="1.0.0"
)


# ==========================================
# CORS
# Permite comunicación con React/Vite
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


# ==========================================
# RUTA PRINCIPAL
# ==========================================

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "LLANO IA API funcionando"
    }


# ==========================================
# CHAT CON LLANO IA
# ==========================================

@app.post("/api/chat")
def chat(request: ChatRequest):

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
       productores o datos que no hayan sido proporcionados.
    5. Si faltan datos importantes, pregunta al usuario.
    6. Ten en cuenta el contexto de Casanare y los Llanos.
    7. No digas que eres ChatGPT. Eres LLANO IA.
    """

    prompt = f"""
    Módulo actual: {request.modulo}

    Mensaje del usuario:
    {request.mensaje}
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