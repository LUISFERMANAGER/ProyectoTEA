fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

# Diccionario de categorías con palabras clave y respuestas
categorias = {
    "saludo": {
        "palabras_claves": ["hola", "buenos dias", "buenas tardes", "buenas noches", "como esta?"],
        "respuestas": ["Hola, bienvenido a tu asistente virtual del TEA.", "¡Bienvenido! Espero que tengas un gran día."]
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
    },
    "aspectos_generales": {
        "palabras_claves": ["aspectos generales", "qué son los TEA", "introducción"],
        "respuestas": [
            "Los Trastornos del Espectro Autista (TEA) son un conjunto de condiciones del neurodesarrollo que afectan la comunicación, la interacción social y el comportamiento.",
            "Los TEA pueden manifestarse de diferentes formas en cada persona, con variaciones en las habilidades, intereses y necesidades de apoyo."
        ]
    },
    "causas_tea": {
        "palabras_claves": ["causas", "base neurológica", "factores genéticos", "contexto ambiental"],
        "respuestas": [
            "Las causas del TEA son complejas e incluyen factores genéticos, anomalías en la arquitectura cerebral y factores ambientales.",
            "La base neurológica del TEA está relacionada con diferencias en el desarrollo cerebral que afectan cómo se procesan las señales sociales y de comunicación.",
            "Los factores genéticos pueden desempeñar un papel importante, pero el TEA también puede influenciarse por interacciones con el entorno durante el desarrollo."
        ]
    },
    "diagnostico": {
        "palabras_claves": ["diagnóstico", "cómo se diagnostica"],
        "respuestas": [
            "El diagnóstico del TEA se basa en la observación del comportamiento y en el historial del desarrollo del individuo.",
            "Especialistas como pediatras, psicólogos y neurólogos utilizan herramientas estandarizadas para identificar síntomas y características del TEA.",
            "Es importante realizar un diagnóstico temprano para facilitar el acceso a tratamientos y apoyos adecuados."
        ]
    },
    "areas_afectadas": {
        "palabras_claves": ["áreas afectadas", "alteraciones", "dificultades"],
        "respuestas": [
            "Las áreas afectadas por el TEA incluyen la interacción social, la comunicación y el lenguaje, así como comportamientos e intereses restringidos.",
            "Las personas con TEA pueden tener dificultades para interpretar señales sociales, expresar emociones o comprender conversaciones.",
            "En el comportamiento, es común que presenten intereses muy específicos, rutinas repetitivas o respuestas inusuales a estímulos sensoriales."
        ]
    },
    "interaccion_social": {
        "palabras_claves": ["interacción social", "relaciones sociales"],
        "respuestas": [
            "Las personas con TEA pueden tener dificultades para iniciar o mantener conversaciones, interpretar gestos o establecer contacto visual.",
            "Es posible que prefieran actividades individuales y encuentren desafiantes las situaciones sociales complejas."
        ]
    },
    "comunicacion_lenguaje": {
        "palabras_claves": ["comunicación", "lenguaje"],
        "respuestas": [
            "La comunicación en el TEA puede incluir un retraso en el lenguaje, dificultades para comprender metáforas o un estilo de habla muy literal.",
            "Algunas personas pueden desarrollar habilidades avanzadas en áreas específicas del lenguaje mientras enfrentan desafíos en otras."
        ]
    },
    "comportamiento_intereses": {
        "palabras_claves": ["comportamiento", "intereses restringidos"],
        "respuestas": [
            "El comportamiento en el TEA a menudo incluye intereses muy específicos o repetitivos, como un fuerte enfoque en un tema particular.",
            "Las rutinas son importantes para muchas personas con TEA, y los cambios pueden generar ansiedad o estrés."
        ]
    },
    "tratamiento_tea": {
    "palabras_claves": ["tratamiento", "intervención", "apoyo"],
    "respuestas": [
        "El tratamiento para el TEA no tiene cura universal y debe ser personalizado en función de la persona y sus necesidades específicas.",
        "Los enfoques de intervención comúnmente incluyen estrategias para mejorar la comunicación y la interacción social.",
        "No hay una cura mágica para el TEA, pero un enfoque personalizado puede ser muy efectivo para personas específicas."
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


@app.get("/categoria/{nombre_categoria}")
def buscar_categoria(nombre_categoria: str):
    nombre_categoria = nombre_categoria.lower()
    # Verificamos si la categoría existe en el diccionario
    if nombre_categoria in categorias:
        return categorias[nombre_categoria]
    else:
        raise HTTPException(status_code=404, detail=f"La categoría '{nombre_categoria}' no fue encontrada.")

