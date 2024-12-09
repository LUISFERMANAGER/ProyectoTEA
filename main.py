import tkinter 
tkinter.Tk().withdraw()  

import threading 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer  # Importar TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import random
from collections import Counter
import spacy
from textblob import TextBlob

nlp = spacy.load("es_core_news_md")


# Inicializar la aplicación FastAPI
app = FastAPI()
app.title = "Bienvenido al asistente virtual TEABot → for Luisfer-Javi-Nelson-Anderson-Jorge-Neiver-valentina"
app.version = "[ Ver → 1.0 ]"
# **1. Configuración inicial de categorías y dataset**
# Diccionario de categorías: define palabras clave y respuestas automáticas para cada categoría.
categorias = {
    "saludo": {
        "palabras_claves": ["hola", "Hola!", "Hey!", "Qué tal?", "Cómo va?", "Quiubo?", "Hola de nuevo", "Me alegra verte de nuevo", "", "buenos dias", "buenas tardes", "buenas noches", "como estas?"],
        "respuestas": ["Hola, bienvenido a tu asistente virtual del TEA."]
    },
    "despedida": {
        "palabras_claves": ["adios", "chao", "hasta luego", "nos vemos", "bye"],
        "respuestas": ["Gracias por usar tu asistente virtual TEA."]
    },
    "bienestar_emocional": {  # Nueva categoría general
        "motivacion": {
            "palabras_claves": ["aconsejame", "motivame", "diferente", "triste","tengo baja autoestima"],
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
        "emociones": {
            "palabras_claves": ["emociones", "sentimientos", "no me acepto"],
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
        "ansiedad_laboral": {
            "palabras_claves": ["ansiedad laboral", "estrés en el trabajo"],
            "respuestas": [
            "Puedo recomendarte una pagina web de estrategias de relajación y mindfulness, que te ayudaran con tu ansiedad laboral da click en el siguiente enlace https://www.calm.com/es"
            ]
        }
    },
    "habilidades_sociales": {  # Nueva categoría general
        "socializacion": {  # Nueva subcategoría
            "palabras_claves": ["estrategias", "como puedo ayudarme", "metodos para mejorar", "incomprendido", "socializar", "conversar", "interacción social", "hacer amigos", "entender a los demás"],
            "respuestas": [
                "Crear rutinas es clave para avanzar.",
                "Busca apoyo en un terapeuta especializado.",
                "Es normal que las personas con TEA enfrenten desafíos en la interacción social. Busca estrategias que te ayuden a comunicarte y relacionarte con los demás.",
                "No estás solo. Hay muchas personas con TEA que se sienten incomprendidas. Busca grupos de apoyo donde puedas compartir tus experiencias y conectar con otros.",
                "Practicar la comunicación en entornos seguros y controlados, como juegos de roles o con familiares y amigos.",
                "Utilizar apoyos visuales, como imágenes o pictogramas, para facilitar la comprensión y la expresión.",
                "Aprender estrategias para iniciar y mantener conversaciones, como hacer preguntas, escuchar activamente y mostrar interés",
                "Trabajar en la interpretación del lenguaje no verbal, como las expresiones faciales y el lenguaje corporal.",
                "Unirse a grupos de apoyo o actividades sociales para personas con TEA para practicar habilidades sociales y conocer gente nueva."
            ]
        },
        "habilidades_sociales": {
            "palabras_claves": ["habilidades sociales", "como interactuar", "socializar"],
            "respuestas": [
                "Practica escenarios sociales con juegos de roles.",
                "Mejorar las habilidades sociales en personas con TEA es un proceso que requiere paciencia, comprensión y estrategias adaptadas a sus necesidades individuales. Aquí te dejo algunas recomendaciones que pueden ser útiles; Identificar las áreas de dificultad:Observación: Presta atención a las situaciones sociales donde la persona con TEA muestra más dificultades, iniciar conversaciones, mantener el contacto visual, interpretar expresiones faciales, etc...Comunicación: Habla con la persona sobre sus propias experiencias y desafíos en situaciones sociales. Evaluación profesional: Considera la posibilidad de una evaluación por parte de un profesional especializado en TEA para identificar las áreas específicas que necesitan atención."
            ]
        },
        "comunicacion_laboral": {
            "palabras_claves": ["comunicacion laboral", "comunicarse en el trabajo"],
            "respuestas": [
                "La comunicación efectiva es esencial en el trabajo.",
                "Identifica tus fortalezas y desafíos: Reconoce tus habilidades comunicativas y las áreas donde necesitas apoyo.Practica la comunicación asertiva: Aprende a expresar tus necesidades y opiniones de forma clara y respetuosa.Utiliza apoyos visuales: Si te resulta útil, usa imágenes, diagramas o escritura para complementar la comunicación verbal.Prepara lo que quieres comunicar: Si tienes que dar una presentación o participar en una reunión, planifica con antelación lo que quieres decir.Pide aclaraciones: Si no entiendes algo, no dudes en pedir que te lo expliquen de otra manera.Busca un mentor o compañero de apoyo: Tener a alguien en el trabajo que te comprenda y te apoye puede marcar una gran diferencia."
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
        }
    },
    "aprendizaje": {  # Nueva categoría general
        "estrategias_aprendizaje": {  # Nueva subcategoría
            "palabras_claves": ["aprendizaje", "estudiar", "concentrarse", "atención", "memoria",],
            "respuestas": [
                "Utilizar herramientas como diarios emocionales o aplicaciones de mindfulness para registrar y gestionar las emociones.",
                "Buscar apoyo en un terapeuta o consejero para aprender estrategias de manejo emocional más específicas.",
                "Utilizar métodos de aprendizaje visual, como mapas mentales o diagramas, para facilitar la comprensión y la memorización.",
                "Crear un ambiente de estudio tranquilo y libre de distracciones.",
                "Dividir el tiempo de estudio en bloques más cortos con descansos regulares para mantener la concentración.",
                "Utilizar técnicas de memorización, como la repetición espaciada o la asociación de ideas.",
                "Podria recomendarte una aplicacion para mejorar tu aprendizaje;Google Calendar:  Fundamental para programar tareas, recordatorios y citas.  Ayuda a visualizar el tiempo y a estructurar el día a día.Mindomo:  Herramienta para crear mapas mentales y  organizar ideas visualmente.Forest:  App que te ayuda a concentrarte bloqueando las distracciones del móvil.  Mientras te concentras,  crece un árbol virtual."
            ]
        }
    },
    "vida_laboral": {  # Nueva categoría general
        "orientacion_vocacional": {
            "palabras_claves": ["orientacion vocacional", "que carrera estudiar", "encontrar mi vocación"],
            "respuestas": [
                "Considera tus intereses, habilidades y valores al elegir una carrera.",
                "Existen tests y profesionales que pueden ayudarte a descubrir tu vocación. https://psicologiaymente.com/psicologia/test-aptitudes-diferenciales"
            ]
        },
        "insercion_laboral": {
            "palabras_claves": ["insercion laboral", "encontrar trabajo", "recursos de apoyo"],
            "respuestas": [
                "Fundación ConecTEA: Ofrece programas de inclusión sociolaboral que brindan apoyo a personas con TEA en la adquisición de competencias y habilidades profesionales. https://www.fundacionconectea.org/2023/10/20/los-programas-de-insercion-laboral-para-las-personas-con-autismo/",
                
            ]
        },
        "barreras_laborales": {
            "palabras_claves": ["barreras a la inclusión", "dificultades laborales", "discriminación"],
            "respuestas": [
                "Las barreras a la inclusión laboral pueden ser sociales, comunicativas, sensoriales u organizacionales.",
                "Es importante conocer tus derechos y buscar apoyo si enfrentas discriminación."
                "La legislación colombiana no define claramente el TEA como una discapacidad, lo que puede generar ambigüedad al momento de acceder a beneficios y protecciones legales.Esto puede dificultar la aplicación de la Ley 1618 de 2013, que promueve la inclusión laboral de personas con discapacidad, a las personas con TEA.A pesar de los desafíos,  es importante destacar que se están realizando esfuerzos para mejorar la inclusión laboral de las personas con TEA en Colombia.  Organizaciones como la Fundación ConecTEA y  ATADES  trabajan para  promover la  formación,  capacitación y  empleo de personas con TEA."
            ]
        },
        "barreras_organizacionales": {
            "palabras_claves": ["organizacionales", "entorno laboral", "adaptaciones laborales"],
            "respuestas": [
                "Las barreras organizacionales pueden dificultar la adaptación al entorno laboral.",
                "Es importante buscar empresas que ofrezcan adaptaciones y flexibilidad."
            ]
        },
        "preparacion_entrevistas": {
            "palabras_claves": ["preparacion para entrevistas", "entrevista de trabajo", "consejos para entrevistas"],
            "respuestas": [
                "Háblame de ti: Desarrolla una breve presentación que resuma tu experiencia, habilidades y aspiraciones, enfatizando lo relevante para el puesto. Preguntas comunes: Practica respuestas a preguntas típicas como: ¿Por qué quieres este trabajo?, ¿Cuáles son tus fortalezas y debilidades?", "¿Dónde te ves en 5 años?. Preguntas STAR: Utiliza el método STAR Situación, Tarea, Acción, Resultado para responder preguntas sobre experiencias pasadas, dando ejemplos concretos. Preguntas para el entrevistador: Prepara algunas preguntas inteligentes que demuestren tu interés y proactividad ej. ¿Cuáles son los mayores desafíos de este puesto?, ¿Cómo es el ambiente de trabajo en la empresa?."
                
            ]
        },
        "busqueda_empleo": {
            "palabras_claves": ["busqueda de empleo", "encontrar trabajo", "como buscar trabajo"],
            "respuestas": [
                "Existen diferentes estrategias y recursos para la búsqueda de empleo.",
                "Fundación ConecTEA: Ofrece programas de inclusión sociolaboral que brindan apoyo a personas con TEA en la adquisición de competencias y habilidades profesionales. https://www.fundacionconectea.org/2023/10/20/los-programas-de-insercion-laboral-para-las-personas-con-autismo/"
            ]
        },
        "adaptacion_laboral": {
            "palabras_claves": ["adaptacion laboral", "nuevo trabajo", "integrarse al trabajo"],
            "respuestas": [
                "La adaptación al entorno laboral puede ser un desafío.",
                "Es importante tener paciencia, comunicarte con tus compañeros y buscar apoyo."
            ]
        },
        "adaptaciones_lugar_trabajo": {
            "palabras_claves": ["adaptaciones en el lugar de trabajo", "adaptaciones laborales", "entorno laboral"],
            "respuestas": [
                "Existen diferentes adaptaciones que pueden facilitar tu trabajo.",
                "Puedes hablar con tu empleador sobre tus necesidades y solicitar adaptaciones."
            ]
        }
    },
    "familiares": {
        "palabras_claves": ["familia", "ayudar a mi hijo", "mi familiar tiene TEA"],
        "respuestas": [
            "La paciencia y el amor son fundamentales en el apoyo familiar.",
            "Busca grupos de apoyo para compartir experiencias."
        ]
    },
    "plataformas": {
        "palabras_claves": ["plataformas", "recomendaciones de plataformas", "recursos online"],
        "respuestas": [
            "Hay plataformas online con información y recursos para personas con TEA. https://ligautismo.org/",
            "Fundación Adecco Colombia: Su programa Plan Familia ofrece orientación laboral, formación y apoyo para la inserción laboral de personas con discapacidad, incluyendo TEA. Fundación Adecco Colombia. https://fundacionadecco.org/ "
        ]
    },
    "barreras_sensoriales": {
        "palabras_claves": ["sonidos fuertes", "sensibilidad sensorial", "mucho ruido", "ruido", "luces", "texturas", "olores", "ansiedad sensorial"],
        "respuestas": [
            "Las barreras sensoriales pueden causar malestar o sobrecarga sensorial.",
            "Es importante identificar tus necesidades sensoriales y buscar adaptaciones.",
            "Identificar los estímulos sensoriales que te causan malestar y desarrollar estrategias para regularlos.",
            "Crear un kit sensorial con objetos que te ayuden a calmarte o a estimular tus sentidos de forma positiva.",
            "Utilizar herramientas como auriculares con cancelación de ruido o gafas de sol para reducir la sobrecarga sensorial en entornos ruidosos o con mucha luz.",
            "Practicar técnicas de relajación, como la respiración profunda o la meditación, para reducir la ansiedad sensorial",
            "Adaptar el entorno para que sea más amigable con tus necesidades sensoriales, como ajustar la iluminación o la temperatura.",
        ]
    }
}

# **2. Preparación del modelo de aprendizaje automático**
# Inicializar el modelo Naive Bayes y el vectorizador para transformar texto en datos numéricos.
vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=2, max_df=0.8)
model_nb = MultinomialNB()
model_svm = SVC(kernel='linear', probability=True, C=1.0)
model_dt = DecisionTreeClassifier(max_depth=5, min_samples_split=5)

# Dataset inicial que contiene ejemplos representativos de cada categoría.
dataset = {
    "saludo": [
        "hola", "buenos días", "¿cómo estás?",
        "hola!", "hey!", "¿qué tal?",
        "buenas tardes", "buenas noches",
        "hola de nuevo", "me alegra verte",
        "¿qué me cuentas?", "¿cómo te encuentras hoy?",
        "¿Cómo estás?", "¿Qué hay de nuevo?", "¿Cómo te va?",
        "Hola, ¿qué tal?", "Buenos días, ¿cómo amaneciste?"
    ],
    "despedida": [
        "adiós", "chao", "hasta luego",
        "nos vemos", "bye", "hasta pronto",
        "cuídate", "que te vaya bien", "hasta la próxima"
    ],
    "bienestar_emocional": {
        "motivacion": [
            "necesito motivación", "me siento desmotivado", "dame consejos",
            "me siento abrumado", "mis fortalezas", "en qué soy bueno",
            "me siento diferente", "no sé qué hacer con mi vida",
            "quiero superarme", "quiero lograr mis metas",
            "aconsejame", "motivame", "diferente", "triste", "tengo baja autoestima"  # Palabras clave de "categorias"
        ],
        "emociones": [
            "emociones", "sentimientos", "cómo manejar mis emociones",
            "triste", "ansioso", "miedo", "ira", "frustración",
            "no me acepto", "me siento mal conmigo mismo"  # Palabras clave de "categorias"
        ],
        "ansiedad_laboral": [
            "ansiedad laboral", "estrés en el trabajo", "asiedad en el trabajo", "la ansiedad",
            "presión", "nervios", "estrés",
            "ansiedad laboral", "estrés en el trabajo"  # Palabras clave de "categorias"
        ]
    },
    "habilidades_sociales": {
        "socializacion": [
            "estrategias para la vida diaria", "cómo puedo mejorar",
            "me cuesta socializar", "tengo problemas para comunicarme",
            "me siento incomprendido", "cómo hacer amigos", "cómo entender a los demás",
            "estrategias", "como puedo ayudarme", "metodos para mejorar", "incomprendido", "socializar", "conversar", "interacción social", "hacer amigos", "entender a los demás"  # Palabras clave de "categorias"
        ],
        "habilidades_sociales": [
            "habilidades sociales", "como interactuar", "socializar",
            "comunicación", "conversación", "relaciones", "amistad",
            "habilidades sociales", "como interactuar", "socializar"  # Palabras clave de "categorias"
        ],
        "comunicacion_laboral": [
            "comunicacion laboral", "comunicarse en el trabajo",
            "habilidades de comunicación", "asertividad", "claridad",
            "comunicacion laboral", "comunicarse en el trabajo"  # Palabras clave de "categorias"
        ],
        "barreras_sociales": [
            "barreras sociales", "dificultades sociales", "interacción social",
            "aceptación", "inclusión", "comprensión",
            "barreras sociales", "dificultades sociales", "interacción social"  # Palabras clave de "categorias"
        ],
        "barreras_comunicativas": [
            "barreras comunicativas", "dificultades de comunicación",
            "comunicación", "lenguaje", "expresión", "comprensión",
            "barreras comunicativas", "dificultades de comunicación", "comunicación"  # Palabras clave de "categorias"
        ]
    },
    "aprendizaje": {
        "estrategias_aprendizaje": [
            "tengo ansiedad", "me siento abrumado",
            "no sé cómo manejar mis emociones", "cómo controlar mis emociones",
            "aprendizaje", "estudiar", "concentrarse", "atención", "memoria",
            "cómo puedo aprender mejor", "técnicas de estudio",
            "cómo puedo ser más organizado", "cómo puedo gestionar mi tiempo",
            "me siento abrumado", "no sé cómo manejar mis emociones", "frustración", "ira", "tristeza", "autocontro", "aprendizaje", "estudiar", "concentrarse", "atención", "memoria", "comprensión"  # Palabras clave de "categorias"
        ]
    },
    "vida_laboral": {
        "orientacion_vocacional": [
            "orientacion vocacional", "que carrera estudiar",
            "encontrar mi vocación", "qué quiero ser de mayor",
            "mis intereses", "mis habilidades", "tests vocacionales",
            "orientacion vocacional", "que carrera estudiar", "encontrar mi vocación"  # Palabras clave de "categorias"
        ],
        "insercion_laboral": [
            "insercion laboral", "encontrar trabajo", "recursos de apoyo",
            "trabajo", "empleo", "oportunidades laborales",
            "insercion laboral", "encontrar trabajo", "recursos de apoyo"  # Palabras clave de "categorias"
        ],
        "barreras_laborales": [
            "barreras a la inclusión", "dificultades laborales", "discriminación",
            "desigualdad", "prejuicios", "estereotipos",
            "barreras a la inclusión", "dificultades laborales", "discriminación"  # Palabras clave de "categorias"
        ],
        "barreras_organizacionales": [
            "barreras organizacionales", "entorno laboral", "adaptaciones laborales",
            "flexibilidad", "accesibilidad", "apoyos",
            "organizacionales", "entorno laboral", "adaptaciones laborales"  # Palabras clave de "categorias"
        ],
        "preparacion_entrevistas": [
            "preparacion para entrevistas", "entrevista de trabajo",
            "consejos para entrevistas", "cómo prepararme", "qué decir",
            "preparacion para entrevistas", "entrevista de trabajo", "consejos para entrevistas"  # Palabras clave de "categorias"
        ],
        "busqueda_empleo": [
            "busqueda de empleo", "encontrar trabajo", "como buscar trabajo",
            "currículum", "carta de presentación", "portales de empleo",
            "busqueda de empleo", "encontrar trabajo", "como buscar trabajo"  # Palabras clave de "categorias"
        ],
        "adaptacion_laboral": [
            "adaptacion laboral", "nuevo trabajo", "integrarse al trabajo",
            "compañeros", "jefe", "entorno", "tareas",
            "adaptacion laboral", "nuevo trabajo", "integrarse al trabajo"  # Palabras clave de "categorias"
        ],
        "adaptaciones_lugar_trabajo": [
            "adaptaciones en el lugar de trabajo", "adaptaciones laborales",
            "entorno laboral", "herramientas", "tecnología", "espacio",
            "adaptaciones en el lugar de trabajo", "adaptaciones laborales", "entorno laboral"  # Palabras clave de "categorias"
        ]
    },
    "familiares": [
        "mi hijo tiene TEA", "ayuda para familiares",
        "como ayudar a un familiar", "como puedo ayudar a mi hijo",
        "familia", "padres", "hermanos",
        "familia", "como puedo ayudar a mi hijo", "mi familiar tiene TEA"  # Palabras clave de "categorias"
    ],
    "plataformas": [
        "plataformas", "recomendaciones de plataformas", "recursos online",
        "páginas web", "aplicaciones", "información útil",
        "plataformas", "recomendaciones de plataformas", "recursos online"  # Palabras clave de "categorias"
    ],
    "barreras_sensoriales": [
        "barreras sensoriales", "sensibilidad sensorial", "sobrecarga sensorial",
        "ruido", "luces", "texturas", "olores", "ansiedad sensorial",
        "sonidos fuertes", "sensibilidad sensorial", "mucho ruido", "ruido", "luces", "texturas", "olores", "ansiedad sensorial"  # Palabras clave de "categorias"
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
        if isinstance(datos, dict):  # Verificar si es una categoría anidada
            if categoria not in original_dataset:
                original_dataset[categoria] = {}  # Inicializar la categoría como un diccionario
            for subcategoria, subdatos in datos.items():
                if subcategoria in original_dataset[categoria]:
                    original_dataset[categoria][subcategoria].extend(subdatos["palabras_claves"])
                else:
                    original_dataset[categoria][subcategoria] = subdatos["palabras_claves"]
        else:  # Si no es anidada, mantener el comportamiento anterior
            if categoria in original_dataset:
                original_dataset[categoria].extend(datos["palabras_claves"])
            else:
                original_dataset[categoria] = datos["palabras_claves"]
    return original_dataset

# **5. Entrenamiento del modelo Naive Bayes**
@app.post("/train")
def train_model():
    # Recopilar frases y etiquetas de todas las categorías para entrenar el modelo.
    all_phrases = []
    all_labels = []
    for categoria, datos in dataset.items():
        if isinstance(datos, dict):  # Manejar categorías anidadas
            for subcategoria, frases in datos.items():
                all_phrases.extend(frases)
                all_labels.extend([f"{categoria}/{subcategoria}"] * len(frases))
        else:  # Manejar categorías no anidadas
            all_phrases.extend(datos)
            all_labels.extend([categoria] * len(datos))

    # Vectorizar las frases y entrenar el modelo Naive Bayes.
    X = vectorizer.fit_transform(all_phrases)
    model_nb.fit(X, all_labels)
    model_svm.fit(X, all_labels)
    model_dt.fit(X, all_labels)

    # Verificar si el vocabulario se ha creado correctamente (opcional)
    if len(vectorizer.vocabulary_) == 0:  # Verificar si el diccionario está vacío
        print("Error: El vocabulario no se ha creado correctamente.")

    # Devolver una respuesta indicando que el modelo se ha entrenado exitosamente.
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
    prediction = model_nb.predict(X)[0]  # Usar el modelo Naive Bayes para la predicción

    # Dividir la predicción en categoría y subcategoría (si existe)
    partes_prediccion = prediction.split("/")
    categoria = partes_prediccion[0]
    subcategoria = partes_prediccion[1] if len(partes_prediccion) > 1 else None

    # Generar respuestas predefinidas según la categoría y subcategoría.
    if categoria in categorias:
        if subcategoria:  # Si se predijo una subcategoría
            respuestas = []
            for _ in range(input.cantidad_respuestas):
                respuestas.append(random.choice(categorias[categoria][subcategoria]["respuestas"]))
            return {"categoria": categoria, "subcategoria": subcategoria, "respuestas": respuestas}
        else:  # Si no hay subcategoría
            respuestas = []
            for _ in range(input.cantidad_respuestas):
                respuestas.append(random.choice(categorias[categoria]["respuestas"]))
            return {"categoria": categoria, "respuestas": respuestas}
    
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
    return {"mensaje": "Bienvenido al asistente virtual TEABot → for Luisfer-Javi-Nelson-Anderson-Jorge-Neiver-valentina"}

# **10.Función para mostrar la GUI con el cuadro de preguntas**def ejecutar_gui():
def ejecutar_gui(texto_pregunta):
    import gui  # Importa el archivo gui.py que contiene el código de la GUI
    print("GUI iniciada en un hilo separado.")

# **Modificar la ruta /predict**
@app.post("/predict")
def predict(input: UserInput):
    # Crear un hilo para ejecutar la GUI
    hilo_gui = threading.Thread(target=ejecutar_gui, args=(input.mensaje,)) 
    hilo_gui.start()

    return {"mensaje": "Procesando pregunta..."}
