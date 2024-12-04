from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import random
from collections import Counter
import schedule
import time

# Inicializar la aplicación FastAPI
app = FastAPI()

# **1. Configuración inicial de categorías y dataset**
# Diccionario de categorías: define palabras clave y respuestas automáticas para cada categoría.
categorias = {
    "saludo": {
        "palabras_claves": ["hola", "Hola!", "Hey!", "Qué tal?", "Cómo va?", "Quiubo?", "Hola de nuevo", "Me alegra verte de nuevo", "", "buenos dias", "buenas tardes", "buenas noches", "como estas?"],
        "respuestas": ["Hola, bienvenido a tu asistente virtual del TEA.", "¡Bienvenido! Espero que tengas un gran día.", "¡Hola! ¿En qué puedo ayudarte hoy?", "¡Hey! ¿Cómo te va?", "¡Hola! Estoy listo para responder a tus preguntas."]
    },
    "despedida": {
        "palabras_claves": ["adios", "chao", "hasta luego", "nos vemos", "bye"],
        "respuestas": ["Gracias por usar mi asistente virtual.", "Un gusto para mí ayudarte.", "Que tengas un buen día."]
    },
    "motivacion": {
        "palabras_claves": ["aconsejame", "necesito ayuda", "motivame", "me gustaria saber", "qué puedo hacer bien", "mis habilidades", "me siento diferente", "soy diferente", "en qué soy bueno"],
        "respuestas": [
            "Ser diferente es ser único, y eso es algo hermoso.",
            "El mundo necesita tu forma especial de pensar y ser.",
            "Cada persona con TEA es única y tiene sus propias fortalezas. Descubre las tuyas y úsalas a tu favor.",
            "El TEA no te define. Enfócate en tus habilidades e intereses, y busca oportunidades para desarrollarlas.",
            "Ser diferente no es algo malo. La diversidad es lo que hace al mundo interesante.",
            "Recuerda que tienes mucho que ofrecer. No te compares con los demás, concéntrate en tu propio camino.",
            "Tus habilidades y talentos son valiosos. Busca un entorno donde puedas usarlos y brillar.",

        ]
    },
    "estrategias": {
        "palabras_claves": ["estrategias", "como puedo ayudarme", "metodos para mejorar", "me cuesta socializar", "me siento incomprendido", "tengo ansiedad", "me siento abrumado", "no sé cómo manejar mis emociones", "socializar", "conversar", "interacción social", "hacer amigos", "entender a los demás", "frustración", "ira", "tristeza", "autocontro", "aprendizaje", "estudiar", "concentrarse", "atención", "memoria", "comprensión"],
        "respuestas": [
            "Crear rutinas es clave para avanzar.",
            "Busca apoyo en un terapeuta especializado.",
            "Es normal que las personas con TEA enfrenten desafíos en la interacción social. Busca estrategias que te ayuden a comunicarte y relacionarte con los demás.",
            "No estás solo. Hay muchas personas con TEA que se sienten incomprendidas. Busca grupos de apoyo donde puedas compartir tus experiencias y conectar con otros.",
            "La ansiedad es común en personas con TEA. Aprende técnicas de relajación y manejo del estrés para afrontar situaciones que te generen ansiedad.",
            "Si te sientes abrumado, busca un espacio tranquilo donde puedas relajarte y recuperar la calma. También puedes pedir ayuda a un familiar o profesional.",
            "Es importante aprender a identificar y manejar tus emociones. Busca recursos y herramientas que te ayuden a comprender y regular tus emociones.",
            "Practicar la comunicación en entornos seguros y controlados, como juegos de roles o con familiares y amigos.",
            "Utilizar apoyos visuales, como imágenes o pictogramas, para facilitar la comprensión y la expresión.",
            "Aprender estrategias para iniciar y mantener conversaciones, como hacer preguntas, escuchar activamente y mostrar interés",
            "Trabajar en la interpretación del lenguaje no verbal, como las expresiones faciales y el lenguaje corporal.",
            "Unirse a grupos de apoyo o actividades sociales para personas con TEA para practicar habilidades sociales y conocer gente nueva.",
            "Aprender a identificar y nombrar las emociones para comprender mejor lo que sientes.",
            "Desarrollar estrategias para regular las emociones, como técnicas de respiración, relajación o mindfulness.",
            "Identificar las situaciones que te generan estrés o ansiedad y desarrollar planes para afrontarlas.",
            "Utilizar herramientas como diarios emocionales o aplicaciones de mindfulness para registrar y gestionar las emociones.",
            "Buscar apoyo en un terapeuta o consejero para aprender estrategias de manejo emocional más específicas.",
            "Utilizar métodos de aprendizaje visual, como mapas mentales o diagramas, para facilitar la comprensión y la memorización.",
            "Crear un ambiente de estudio tranquilo y libre de distracciones.",
            "Dividir el tiempo de estudio en bloques más cortos con descansos regulares para mantener la concentración.",
            "Utilizar técnicas de memorización, como la repetición espaciada o la asociación de ideas.",
            "Buscar apoyos educativos, como tutores o adaptaciones curriculares, para facilitar el aprendizaje."



        ]
    },
    "emociones": {
        "palabras_claves": ["emociones", "como manejo mis sentimientos", "tristeza", "ansiedad", "no me acepto", "me siento mal conmigo mismo", "no me gusto", "tengo baja autoestima", "mis sueños", "mis metas", "qué quiero lograr", "cómo alcanzar mis metas", "mi futuro",],
        "respuestas": [
            "Hablar sobre tus emociones puede ayudarte a procesarlas.",
            "Intenta ejercicios de respiración para relajarte.",
            "No renuncies a tus sueños. Con esfuerzo y perseverancia, puedes lograr lo que te propongas.",
            "Define tus metas y crea un plan para alcanzarlas. Divide tus objetivos en pasos más pequeños y celebra cada logro.",
            "Busca inspiración en historias de personas con TEA que han alcanzado el éxito. Recuerda que tú también puedes.",
            "No tengas miedo de pedir ayuda. Hay personas y recursos que pueden apoyarte en tu camino hacia tus metas.",
            "Tu futuro está lleno de posibilidades. Enfócate en lo que quieres lograr y trabaja para conseguirlo."
        ]
    },
    "familiares": {
        "palabras_claves": ["familia", "como puedo ayudar a mi hijo", "mi familiar tiene TEA"],
        "respuestas": [
            "La paciencia y el amor son fundamentales en el apoyo familiar.",
            "Busca grupos de apoyo para compartir experiencias."
        ]
    },
    "habilidades_sociales": {
        "palabras_claves": ["habilidades sociales", "como interactuar", "socializar"],
        "respuestas": [
            "Practica escenarios sociales con juegos de roles.",
            "La repetición es clave para desarrollar confianza social."
        ]
    },
    "orientacion_vocacional": {
        "palabras_claves": ["orientacion vocacional", "que carrera estudiar", "encontrar mi vocación"],
        "respuestas": [
            "Considera tus intereses, habilidades y valores al elegir una carrera.",
            "Existen tests y profesionales que pueden ayudarte a descubrir tu vocación."
        ]
    },
    "insercion_laboral": {
        "palabras_claves": ["insercion laboral", "encontrar trabajo", "recursos de apoyo"],
        "respuestas": [
            "Existen programas y recursos de apoyo para la inserción laboral de personas con TEA.",
            "Investiga las opciones disponibles en tu área."
        ]
    },
    "plataformas": {
        "palabras_claves": ["plataformas", "recomendaciones de plataformas", "recursos online"],
        "respuestas": [
            "Hay plataformas online con información y recursos para personas con TEA.",
            "Puedo recomendarte algunas si me dices qué tipo de información buscas."
        ]
    },
    "barreras_laborales": {
        "palabras_claves": ["barreras a la inclusión", "dificultades laborales", "discriminación"],
        "respuestas": [
            "Las barreras a la inclusión laboral pueden ser sociales, comunicativas, sensoriales u organizacionales.",
            "Es importante conocer tus derechos y buscar apoyo si enfrentas discriminación."
        ]
    },
    "barreras_sociales": {
        "palabras_claves": ["barreras sociales", "dificultades sociales", "interacción social"],
        "respuestas": [
            "Las barreras sociales pueden dificultar la interacción y la participación en la comunidad.",
            "Existen estrategias para mejorar las habilidades sociales y la comunicación."
        ]
    },
    "barreras_comunicativas": {
        "palabras_claves": ["barreras comunicativas", "dificultades de comunicación", "comunicación"],
        "respuestas": [
            "Las barreras comunicativas pueden afectar la comprensión y la expresión.",
            "Existen herramientas y técnicas para mejorar la comunicación."
        ]
    },
    "barreras_sensoriales": {
        "palabras_claves": ["barreras sensoriales", "sensibilidad sensorial", "sobrecarga sensorial", "ruido", "luces", "texturas", "olores", "ansiedad sensorial"],
        "respuestas": [
            "Las barreras sensoriales pueden causar malestar o sobrecarga sensorial.",
            "Es importante identificar tus necesidades sensoriales y buscar adaptaciones.",
            "Identificar los estímulos sensoriales que te causan malestar y desarrollar estrategias para regularlos.",
            "Crear un kit sensorial con objetos que te ayuden a calmarte o a estimular tus sentidos de forma positiva.",
            "Utilizar herramientas como auriculares con cancelación de ruido o gafas de sol para reducir la sobrecarga sensorial en entornos ruidosos o con mucha luz.",
            "Practicar técnicas de relajación, como la respiración profunda o la meditación, para reducir la ansiedad sensorial",
            "Adaptar el entorno para que sea más amigable con tus necesidades sensoriales, como ajustar la iluminación o la temperatura.",


        ]
    },
    "barreras_organizacionales": {
        "palabras_claves": ["barreras organizacionales", "entorno laboral", "adaptaciones laborales"],
        "respuestas": [
            "Las barreras organizacionales pueden dificultar la adaptación al entorno laboral.",
            "Es importante buscar empresas que ofrezcan adaptaciones y flexibilidad."
        ]
    },
    "preparacion_entrevistas": {
        "palabras_claves": ["preparacion para entrevistas", "entrevista de trabajo", "consejos para entrevistas"],
        "respuestas": [
            "La preparación para entrevistas es clave para tener éxito en la búsqueda de empleo.",
            "Puedo darte algunos consejos y recursos para que te prepares."
        ]
    },
    "busqueda_empleo": {
        "palabras_claves": ["busqueda de empleo", "encontrar trabajo", "como buscar trabajo"],
        "respuestas": [
            "Existen diferentes estrategias y recursos para la búsqueda de empleo.",
            "Puedo ayudarte a identificar tus habilidades y a crear un buen currículum."
        ]
    },
    "adaptacion_laboral": {
        "palabras_claves": ["adaptacion laboral", "nuevo trabajo", "integrarse al trabajo"],
        "respuestas": [
            "La adaptación al entorno laboral puede ser un desafío.",
            "Es importante tener paciencia, comunicarte con tus compañeros y buscar apoyo."
        ]
    },
    "ansiedad_laboral": {
        "palabras_claves": ["ansiedad laboral", "estrés en el trabajo", "manejar la ansiedad"],
        "respuestas": [
            "Existen estrategias para manejar la ansiedad y el estrés en el trabajo.",
            "Puedo recomendarte algunas técnicas de relajación y mindfulness."
        ]
    },
    "comunicacion_laboral": {
        "palabras_claves": ["comunicacion laboral", "comunicarse en el trabajo", "habilidades de comunicación"],
        "respuestas": [
            "La comunicación efectiva es esencial en el trabajo.",
            "Puedo darte consejos para mejorar tus habilidades de comunicación en el entorno laboral."
        ]
    },
    "adaptaciones_lugar_trabajo": {
        "palabras_claves": ["adaptaciones en el lugar de trabajo", "adaptaciones laborales", "entorno laboral"],
        "respuestas": [
            "Existen diferentes adaptaciones que pueden facilitar tu trabajo.",
            "Puedes hablar con tu empleador sobre tus necesidades y solicitar adaptaciones."
        ]
    }
}

# **2. Preparación del modelo de aprendizaje automático**
# Inicializar el modelo Naive Bayes y el vectorizador para transformar texto en datos numéricos.
vectorizer = CountVectorizer()
model = MultinomialNB()

# Dataset inicial que contiene ejemplos representativos de cada categoría.
dataset = {
    "saludo": [
        "hola", "buenos dias", "como estas",  # Frases básicas
        "hola!", "hey!", "qué tal?",  # Frases informales
        "buenas tardes", "buenas noches",  # Saludos con hora
        "hola de nuevo", "me alegra verte",  # Repetición
        "¿qué me cuentas?", "¿cómo te encuentras hoy?"  # Variaciones
    ],
    "despedida": [
        "adios", "chao", "hasta luego",  # Despedidas comunes
        "nos vemos", "bye", "hasta pronto"  # Variaciones
    ],
    "motivacion": [
        "necesito motivación", "aconsejame", "quiero ánimos",  # Solicitud de motivación
        "soy diferente", "mis habilidades",  # Autoconocimiento
        "qué puedo hacer bien", "en qué soy bueno",  # Fortalezas
        "me siento diferente", "soy diferente"  # Dudas sobre la diferencia
    ],
    "estrategias": [
        "estrategias para la vida diaria", "como puedo ayudarme",  # Solicitud de estrategias
        "metodos para mejorar", "me cuesta socializar",  # Dificultades sociales
        "me siento incomprendido", "tengo ansiedad", "me siento abrumado",  # Ansiedad y emociones
        "no sé cómo manejar mis emociones", "socializar", "conversar",  # Habilidades sociales
        "interacción social", "hacer amigos", "entender a los demás",  # Relaciones
        "frustración", "ira", "tristeza", "autocontrol",  # Manejo emocional
        "aprendizaje", "estudiar", "concentrarse", "atención", "memoria", "comprensión"  # Aprendizaje
    ],
    "emociones": [
        "emociones", "como manejo mis sentimientos",  # Manejo emocional
        "tristeza", "ansiedad", "no me acepto",  # Emociones negativas
        "me siento mal conmigo mismo", "no me gusto",  # Autoestima
        "tengo baja autoestima", "mis sueños", "mis metas",  # Metas y aspiraciones
        "qué quiero lograr", "cómo alcanzar mis metas", "mi futuro"  # Planificación
    ],
    "familiares": [
        "mi hijo tiene TEA", "ayuda para familiares",  # Apoyo familiar
        "como ayudar a un familiar", "como puedo ayudar a mi hijo",  # Información para familiares
        "familia", "padres", "hermanos"  # Roles familiares
    ],
    "habilidades_sociales": [
        "habilidades sociales", "como interactuar", "socializar",  # Interacción social
        "comunicación", "conversación", "relaciones", "amistad"  # Aspectos de la interacción
    ],
    "orientacion_vocacional": [
        "orientacion vocacional", "que carrera estudiar",  # Orientación
        "encontrar mi vocación", "qué quiero ser de mayor",  # Futuro profesional
        "mis intereses", "mis habilidades", "tests vocacionales"  # Autoconocimiento
    ],
    "insercion_laboral": [
        "insercion laboral", "encontrar trabajo", "recursos de apoyo",  # Búsqueda de empleo
        "trabajo", "empleo", "oportunidades laborales"  # Conceptos relacionados
    ],
    "plataformas": [
        "plataformas", "recomendaciones de plataformas", "recursos online",  # Recursos online
        "páginas web", "aplicaciones", "información útil"  # Tipos de recursos
    ],
    "barreras_laborales": [
        "barreras a la inclusión", "dificultades laborales", "discriminación",  # Inclusión laboral
        "desigualdad", "prejuicios", "estereotipos"  # Obstáculos
    ],
    "barreras_sociales": [
        "barreras sociales", "dificultades sociales", "interacción social",  # Dificultades sociales
        "aceptación", "inclusión", "comprensión"  # Aspectos sociales
    ],
    "barreras_comunicativas": [
        "barreras comunicativas", "dificultades de comunicación",  # Comunicación
        "comunicación", "lenguaje", "expresión", "comprensión"  # Aspectos de la comunicación
    ],
    "barreras_sensoriales": [
        "barreras sensoriales", "sensibilidad sensorial", "sobrecarga sensorial",  # Sensibilidad sensorial
        "ruido", "luces", "texturas", "olores", "ansiedad sensorial"  # Estímulos sensoriales
    ],
    "barreras_organizacionales": [
        "barreras organizacionales", "entorno laboral", "adaptaciones laborales",  # Adaptaciones laborales
        "flexibilidad", "accesibilidad", "apoyos"  # Necesidades en el trabajo
    ],
    "preparacion_entrevistas": [
        "preparacion para entrevistas", "entrevista de trabajo",  # Entrevistas de trabajo
        "consejos para entrevistas", "cómo prepararme", "qué decir"  # Dudas sobre entrevistas
    ],
    "busqueda_empleo": [
        "busqueda de empleo", "encontrar trabajo", "como buscar trabajo",  # Búsqueda de empleo
        "currículum", "carta de presentación", "portales de empleo"  # Herramientas
    ],
    "adaptacion_laboral": [
        "adaptacion laboral", "nuevo trabajo", "integrarse al trabajo",  # Adaptación al trabajo
        "compañeros", "jefe", "entorno", "tareas"  # Aspectos del trabajo
    ],
    "ansiedad_laboral": [
        "ansiedad laboral", "estrés en el trabajo", "manejar la ansiedad",  # Ansiedad laboral
        "presión", "nervios", "estrés"  # Síntomas
    ],
    "comunicacion_laboral": [
        "comunicacion laboral", "comunicarse en el trabajo",  # Comunicación laboral
        "habilidades de comunicación", "asertividad", "claridad"  # Habilidades
    ],
    "adaptaciones_lugar_trabajo": [
        "adaptaciones en el lugar de trabajo", "adaptaciones laborales",  # Adaptaciones en el trabajo
        "entorno laboral", "herramientas", "tecnología", "espacio"  # Aspectos del entorno
    ]
}    

# **3. Estructura del modelo de entrada para recibir mensajes del usuario**
class UserInput(BaseModel):
    mensaje: str  # Mensaje enviado por el usuario
    cantidad_respuestas: int = 1  # Número de respuestas solicitadas por el usuario (por defecto 1)

# **4. Expansión del dataset inicial**
# Función que extiende el dataset con las palabras clave definidas en las categorías.
def expand_dataset(original_dataset):
    for categoria, datos in categorias.items():
        if categoria in original_dataset:
            original_dataset[categoria].extend(datos["palabras_claves"])
        else:
            original_dataset[categoria] = datos["palabras_claves"]
    return original_dataset

# Ampliar el dataset con datos adicionales.
dataset = expand_dataset(dataset)

# **5. Entrenamiento del modelo Naive Bayes**
@app.post("/train")
def train_model():
    # Recopilar frases y etiquetas de todas las categorías para entrenar el modelo.
    all_phrases = []
    all_labels = []
    for categoria, frases in dataset.items():
        all_phrases.extend(frases)
        all_labels.extend([categoria] * len(frases))  # Asignar categoría a cada frase.

    # Vectorizar las frases y entrenar el modelo Naive Bayes.
    X = vectorizer.fit_transform(all_phrases)
    model.fit(X, all_labels)

    # Verificar si el vocabulario se ha creado correctamente (opcional)
    if not vectorizer.vocabulary:  # Corrección aquí también
        print("Error: El vocabulario no se ha creado correctamente.")

    return {"message": "Modelo entrenado exitosamente."}

# Entrenar el modelo al iniciar la aplicación
train_model()

# **6. Predicción de la categoría de un mensaje**
@app.post("/predict")
def predict(input: UserInput):
    # Verificar si el modelo está entrenado.
    if not vectorizer.vocabulary_:
        raise HTTPException(status_code=400, detail="El modelo no ha sido entrenado.")
    
    # Vectorizar el mensaje del usuario y predecir la categoría más probable.
    mensaje = input.mensaje.lower()
    X = vectorizer.transform([mensaje])
    prediction = model.predict(X)[0]

    # Generar respuestas predefinidas según la categoría.
    if prediction in categorias:
        respuestas = []
        for _ in range(input.cantidad_respuestas):
            respuestas.append(random.choice(categorias[prediction]["respuestas"]))
        return {"categoria": prediction, "respuestas": respuestas}
    
    # Caso en que no se encuentre una categoría adecuada.
    raise HTTPException(status_code=404, detail="No se encontró una respuesta adecuada.")

# **7. Funcionalidades adicionales del modelo**
# Listar todas las categorías disponibles.
@app.get("/categorias")
def listar_categorias():
    return {"categorias": list(categorias.keys())}

# Obtener detalles de una categoría específica (palabras clave y respuestas).
@app.get("/categoria/{nombre_categoria}")
def detalles_categoria(nombre_categoria: str):
    if nombre_categoria in categorias:
        return categorias[nombre_categoria]
    else:
        raise HTTPException(status_code=404, detail=f"La categoría '{nombre_categoria}' no fue encontrada.")

# Añadir nuevas frases a una categoría existente o crear una nueva categoría.
@app.post("/add-phrase")
def add_phrase(categoria: str, frase: str):
    if categoria not in dataset:
        dataset[categoria] = []  # Crear nueva categoría si no existe.
    dataset[categoria].append(frase)  # Añadir frase al dataset.
    if categoria in categorias:
        categorias[categoria]["palabras_claves"].append(frase)
    else:
        categorias[categoria] = {"palabras_claves": [frase], "respuestas": []}
    return {"message": f"Frase añadida a la categoría '{categoria}'."}

# **8. Cálculo de frecuencia de palabras en un texto**
# Función para calcular las frecuencias de palabras en un texto proporcionado.
def calcular_frecuencia_palabras(texto: str):
    palabras = texto.lower().split()
    frecuencia = Counter(palabras)
    return dict(frecuencia)

# Ruta para calcular y devolver las frecuencias de palabras en un texto.
@app.post("/frecuencia-palabras")
def prueba_frecuencia_palabras(texto: str):
    if not texto.strip():
        raise HTTPException(status_code=400, detail="El texto proporcionado está vacío.")
    frecuencia = calcular_frecuencia_palabras(texto)
    return {"frecuencia": frecuencia}

# **9. Verificación del funcionamiento del servicio**
@app.get("/")
def home():
    return {"mensaje": "Bienvenido al asistente virtual TEA mejorado."}
