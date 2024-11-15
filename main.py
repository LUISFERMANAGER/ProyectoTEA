from fastapi import FastAPI 
from fastapi import FastAPI,Query # Importamos la libreria FastAPI
from fastapi.responses import JSONResponse # Importamos la libreria JSONResponse
from fastapi.responses import HTMLResponse
from typing import Optional
import nltk # Importamos la libreria Optional para volver parametros opcionales

app = FastAPI() #Crea una instancia de la clase FastAPI 
app.title = "App Categorización de Trastornos de Espectro Autista con FastAPI - Javier, Nelson, Anderson, Luis"
app.version = "0.0.1"

listapregunta = [
    {
        "id": 11,
        "Pregunta?": "¿Te cuesta interpretar las señales sociales no verbales, como el lenguaje corporal o el tono de voz?",
        "Respueta": "Si / No",
        "Categoria": 1,       
    },
    {
        "id": 12,
        "Pregunta?": "¿Prefieres actividades solitarias o en grupos pequeños?",
        "Respueta": "Si / No",
        "Categoria": 1,       
    },
    {
        "id": 13,
        "Pregunta?": "¿Tienes dificultades para iniciar o mantener conversaciones?",
        "Respueta": "Si / No",
        "Categoria": 1,       
    },
    {
        "id": 14,
        "Pregunta?": "¿Te resulta difícil entender las emociones de los demás y expresar las tuyas propias?",
        "Respueta": "Si / No",
        "Categoria": 1,       
    },
    {
        "id": 15,
        "Pregunta?": "¿A menudo te sientes incómodo en situaciones sociales o en grupos grandes?",
        "Respueta": "Si / No",
        "Categoria": 1,       
    },
    {
        "id": 21,
        "Pregunta?": "¿Tienes intereses intensos y duraderos en temas específicos?",
        "Respueta": "Si / No",
        "Categoria": 2,       
    },
    {
        "id": 22,
        "Pregunta?": "¿Sientes la necesidad de seguir rutinas o rituales muy específicos?",
        "Respueta": "Si / No",
        "Categoria": 2,       
    },
    {
        "id": 23,
        "Pregunta?": "¿Te molestan los cambios en tu entorno o en tus rutinas diarias?",
        "Respueta": "Si / No",
        "Categoria": 2,       
    },
    {
        "id": 24,
        "Pregunta?": "¿Tienes movimientos repetitivos, como balancearte o hacer clic con los dedos?",
        "Respueta": "Si / No",
        "Categoria": 2,       
    },
    {
        "id": 25,
        "Pregunta?": "¿Te sientes abrumado por ciertos estímulos sensoriales, como los ruidos fuertes o las luces brillantes?",
        "Respueta": "Si / No",
        "Categoria": 2,       
    },
    {
        "id": 31,
        "Pregunta?": "¿Tuviste dificultades en el desarrollo del lenguaje o del habla cuando eras niño?",
        "Respueta": "Si / No",
        "Categoria": 3,       
    },
    {
        "id": 32,
        "Pregunta?": "¿Te costaba hacer amigos o jugar con otros niños cuando eras pequeño?",
        "Respueta": "Si / No",
        "Categoria": 3,       
    },
    {
        "id": 33,
        "Pregunta?": "¿Tenías intereses inusuales o comportamientos repetitivos en la infancia?",
        "Respueta": "Si / No",
        "Categoria": 3,       
    },
    {
        "id": 34,
        "Pregunta?": "¿Has tenido dificultades en el ámbito laboral o académico debido a problemas de comunicación o interacción social?",
        "Respueta": "Si / No",
        "Categoria": 3,       
    },
    {
        "id": 41,
        "Pregunta?": "¿Tienes dificultades para entender el sarcasmo o el humor?",
        "Respueta": "Si / No",
        "Categoria": 4,       
    },
    {
        "id": 42,
        "Pregunta?": "¿Te cuesta seguir instrucciones complejas o multipasos?",
        "Respueta": "Si / No",
        "Categoria": 4,       
    },
    {
        "id": 43,
        "Pregunta?": "¿Tienes problemas para organizar tu tiempo o tus tareas?",
        "Respueta": "Si / No",
        "Categoria": 4,       
    },
    {
        "id": 44,
        "Pregunta?": "¿Te sientes diferente o aislado de los demás?",
        "Respueta": "Si / No",
        "Categoria": 4       
    }
]

@app.get('/', tags=["Home"])#Definimos una ruta
def message(): # Definimos una función de la ruta
    return HTMLResponse ('<h1>Categorizacion de Trastornos de Espectro Autista</h1>') # Devolvemos un string en la respuesta de la ruta

@app.get('/categoria', tags=["Categoria"])#Definimos una ruta de la clase FastAPI
def get_listapregunta(): 
    return listapregunta

@app.get('/categoria/{id}', tags=["Categoria"])#Definimos una ruta de la clase FastAPI
def get_lista_pregunta(id: int):
    for item in listapregunta:
        if item['id'] == id:
            return item
    return []

#Tokenizar
@app.post("/tokenizar") # Decorador para indicar que es una ruta de la API
def tokenize(text:str): # Funcion que retorna un mensaje
    return preprocessar(text)

def preprocessar(text):
    import json  # Importamos la librería json para trabajar con archivos json
    from nltk.tokenize import word_tokenize
    import nltk
    nltk.download('punkt')
    tokens = word_tokenize(text)
    result = {word: True for word in tokens}
    print(result)
    return JSONResponse(content={"message":result})
    