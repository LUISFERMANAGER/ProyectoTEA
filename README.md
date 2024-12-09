Explicación del Código del Chatbot para TEA
Este código implementa un chatbot diseñado para ayudar a personas con Trastorno del Espectro Autista (TEA) en el ámbito laboral. Utiliza aprendizaje automático para comprender las preguntas de los usuarios y proporcionar respuestas relevantes.

1. Configuración Inicial:

Se definen categorías con palabras clave y respuestas asociadas.
Se crea un dataset inicial con ejemplos de frases para cada categoría.

2. Preparación del Modelo:

Se utiliza TfidfVectorizer para convertir el texto en datos numéricos.
Se inicializan tres modelos de aprendizaje automático: Naive Bayes, SVM y Decision Tree.

3. Modelo de Entrada:

Se define una clase para recibir el mensaje del usuario y la cantidad de respuestas deseadas.

4. Expansión del Dataset:

Se añade una función para expandir el dataset con las palabras clave de las categorías.

5. Entrenamiento del Modelo:

Se recopilan frases y etiquetas del dataset.
Se vectorizan las frases y se entrenan los modelos.

6. Predicción de Categoría:

Se vectoriza el mensaje del usuario.
Se utiliza el modelo Naive Bayes para predecir la categoría.
Se generan respuestas predefinidas según la categoría.

7. Funcionalidades Adicionales:

Se incluyen rutas para listar categorías, obtener detalles de una categoría y añadir nuevas frases.

8. Cálculo de Frecuencia de Palabras:

Se implementa una función para calcular la frecuencia de palabras en un texto.

9. Verificación del Servicio:

Se define una ruta principal para verificar el funcionamiento del servicio.

10. Interfaz Gráfica:

Se utiliza la librería Tkinter para crear una interfaz gráfica.
Se ejecuta la interfaz en un hilo separado.

Puntos Clave:

El código utiliza técnicas de procesamiento del lenguaje natural (NLP) para comprender el significado de las preguntas.
El aprendizaje automático permite al chatbot mejorar sus respuestas con el tiempo.
La interfaz gráfica facilita la interacción con el usuario.
El chatbot está diseñado para ser flexible y extensible, con la capacidad de añadir nuevas categorías y respuestas.
