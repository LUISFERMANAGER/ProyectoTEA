from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

# Diccionario de categorías con palabras clave y respuestas
categorias = {
    "saludo": {
        "palabras_claves": ["hola", "buenos dias", "buenas tardes", "buenas noches", "como esta?"],
        "respuestas": ["Hola, bienvenido a tu asistente virtual del TEA", "¡Hola! ¿En qué puedo ayudarte?", "¡Bienvenido! Espero que tengas un gran día."]
    },
    "despedida": {
        "palabras_claves": ["adios", "chao", "hasta luego", "nos vemos", "bye", "que tengas un lindo dia", "que tengas una buena tarde", "feliz noche"],
        "respuestas": ["Gracias por usar mi asistente virtual.", "Un gusto para mí ayudarte.", "Que tengas un buen día.", "Nos vemos pronto."]
    },
    "motivacion": {
        "palabras_claves": ["aconsejame", "necesito ayuda", "motivame", "me gustaria saber"],
        "respuestas": [
            "Ser diferente es ser único, y eso es algo hermoso.",
            "El mundo necesita tu forma especial de pensar y ser.",
            "Puedes lograr grandes cosas a tu propio ritmo.",
            "No te rindas, cada paso cuenta."
        ]
    }
}

# Modelo de entrada del usuario
class UserInput(BaseModel):
    mensaje: str
    cantidad_respuestas: int = 1  # Opcional: cuántas respuestas se generarán (valor predeterminado: 1)


@app.get("/")
def home():
    return {"mensaje": "Bienvenidos al Proyecto TEA for Luisfer-javi-nelson-anderson-jorge-neiver-valentina"}


@app.get("/favicon.ico")
def favicon():
    return {}


@app.post("/responder")
def responder(input: UserInput):
    # Convertimos el mensaje del usuario a minúsculas para evitar problemas de coincidencia
    mensaje = input.mensaje.lower()
    categorias_detectadas = []

    # Identificar categorías presentes en el mensaje
    for categoria, datos in categorias.items():
        for palabra_clave in datos["palabras_claves"]:
            if palabra_clave in mensaje:
                categorias_detectadas.append(categoria)
                break  # Salimos del bucle interno para evitar duplicados dentro de la misma categoría

    if categorias_detectadas:
        # Generar respuestas combinadas
        respuestas_generadas = []
        for _ in range(input.cantidad_respuestas):
            respuesta_combinada = []
            for categoria in categorias_detectadas:
                respuesta_combinada.append(random.choice(categorias[categoria]["respuestas"]))
            respuestas_generadas.append(" ".join(respuesta_combinada))
        return {"respuestas": respuestas_generadas}

    # Si no se encuentra ninguna categoría
    raise HTTPException(status_code=404, detail="No se encontró una respuesta adecuada para tu mensaje.")


# Buscar palabras clave y respuestas de una categoría específica
@app.get("/categoria/{nombre_categoria}")
def buscar_categoria(nombre_categoria: str):
    nombre_categoria = nombre_categoria.lower()
    # Verificamos si la categoría existe en el diccionario
    if nombre_categoria in categorias:
        return categorias[nombre_categoria]
    else:
        raise HTTPException(status_code=404, detail=f"La categoría '{nombre_categoria}' no fue encontrada.")
