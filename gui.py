import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import requests

class ChatbotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Asistente Virtual TEAbot")
        self.setGeometry(100, 100, 600, 400)
        
        # --- Diseño ---
        vbox = QVBoxLayout()

        # Historial de conversación
        self.historial = QTextEdit()
        self.historial.setReadOnly(True)
        vbox.addWidget(self.historial)

        # Entrada del usuario
        hbox_input = QHBoxLayout()
        label_input = QLabel("Pregunta:")
        self.input_usuario = QLineEdit()
        hbox_input.addWidget(label_input)
        hbox_input.addWidget(self.input_usuario)
        vbox.addLayout(hbox_input)

        # Botón enviar
        self.boton_enviar = QPushButton("Enviar")
        self.boton_enviar.clicked.connect(self.enviar_pregunta)
        vbox.addWidget(self.boton_enviar)

        self.setLayout(vbox)

        # --- Ajustes adicionales ---
        font = QFont("Italic", 16)
        self.setFont(font)
        self.historial.setFont(QFont("Italic", 14))

        print("GUI iniciada")
        
    def enviar_pregunta(self):
        print("Enviando pregunta...")
        pregunta = self.input_usuario.text()
        if not pregunta.strip():
            QMessageBox.critical(self, "Error", "El texto proporcionado está vacío.")  # Se usa QMessageBox
            return

        self.historial.append(f"Tú: {pregunta}")  # Añade pregunta al historial
        self.input_usuario.clear()

        try:
            response = requests.post("http://127.0.0.1:8000/predict", json={"mensaje": pregunta})
            response.raise_for_status()
            data = response.json()
            print("Respuesta de la API:", data)

            categoria = data.get("categoria")
            respuestas = data.get("respuestas")
            if categoria and respuestas:
                respuesta_bot = "\n".join(respuestas)
                self.historial.append(f"TEAbot: {respuesta_bot}")
                print("Categoría:", categoria) 
                print("Respuestas:", respuestas)
            else:
                self.historial.append("TEAbot: No se encontró una respuesta adecuada.")
                print("Disculpa, podemos empezar de nuevo.") 
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Error al comunicarse con la API: {e}")  # Se usa QMessageBox

if __name__ == '__main__':
    app_gui = QApplication(sys.argv)  # <-- Se cambia el nombre de la variable a app_gui
    ex = ChatbotGUI()
    ex.show()
    sys.exit(app_gui.exec_())  # <-- Se usa app_gui
