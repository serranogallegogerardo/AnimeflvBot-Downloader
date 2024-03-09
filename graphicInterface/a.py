import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class CombinedWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Combined Window")
        self.setGeometry(100, 100, 400, 500)  # Ajustar según sea necesario
        self.setMinimumSize(200, 200)  # Establecer tamaño mínimo para evitar ventanas demasiado pequeñas

        # Aplicar fondo oscuro translúcido
        self.setStyleSheet("background-color: rgba(0, 0, 0, 150); border: 1px solid black;")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Añadir imagen de anime
        anime_image = QLabel(self)
        pixmap = QPixmap('anime.jpg')
        anime_image.setPixmap(pixmap)
        anime_image.setScaledContents(True)
        layout.addWidget(anime_image)

        # Añadir algo de espacio entre la imagen y los campos blancos
        layout.addSpacing(20)

        # Añadir campos blancos desde el primer código
        self.add_white_fields(layout)

        # Añadir algo de espacio debajo del segundo campo blanco
        layout.addStretch(1)

        # Añadir música de fondo
        self.add_background_music()

        # Añadir botón de silencio
        self.add_mute_button()

    def add_white_fields(self, layout):
        # Añadir el primer campo blanco (QLineEdit para la entrada del usuario)
        self.anime_name_input = QLineEdit(self)
        self.anime_name_input.setPlaceholderText("Nombre del anime")
        self.anime_name_input.returnPressed.connect(self.print_anime_name)
        # Aplicar estilo para centrar el texto del marcador de posición
        self.anime_name_input.setStyleSheet("background-color: white; border-radius: 10px; border: 2px solid rgb(0, 150, 255); padding: 5px; text-align: center;")
        self.anime_name_input.setFixedSize(280, 35)  # Establecer dimensiones
        # Establecer fuente de anime
        anime_font = QFont("TuFuenteDeAnime", 12)  # Reemplazar "TuFuenteDeAnime" con el nombre de tu fuente de anime
        self.anime_name_input.setFont(anime_font)
        layout.addWidget(self.anime_name_input, alignment=Qt.AlignmentFlag.AlignCenter)

        # Añadir algo de espacio entre los campos blancos
        layout.addSpacing(20)


    def print_anime_name(self):
        anime_name = self.anime_name_input.text()
        print("Nombre del anime:", anime_name)

    def add_background_music(self):
        self.background_music = QMediaPlayer()
        self.background_music.setMedia(QMediaContent(QUrl.fromLocalFile("audio.wav")))
        self.background_music.setVolume(35)  # Establecer volumen al 35%
        self.background_music.play()

    def add_mute_button(self):
        mute_button = QPushButton("Silenciar", self)
        mute_button.setStyleSheet("background-color: red; color: white; border-radius: 5px; padding: 5px;")
        mute_button.clicked.connect(self.toggle_mute)
        layout = QVBoxLayout()
        layout.addWidget(mute_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        layout.setContentsMargins(20, 0, 0, 20)  # Izquierda, Arriba, Derecha, Abajo

        # Crear un widget contenedor para el diseño y agregarlo al layout principal
        widget = QWidget()
        widget.setLayout(layout)
        self.centralWidget().layout().addWidget(widget)

    def toggle_mute(self):
        if self.background_music.volume() == 0:
            self.background_music.setVolume(35)  # Desmutear, volver a establecer el volumen al 35%
        else:
            self.background_music.setVolume(0)   # Silenciar

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CombinedWindow()
    window.show()
    sys.exit(app.exec_())
