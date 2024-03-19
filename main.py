import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QTextEdit, QLineEdit, QHBoxLayout, QMessageBox
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
from PyQt6.QtGui import QPixmap, QImage, QClipboard, QGuiApplication
from PyQt6.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lecteur et Générateur de QR Code")

        tabs = QTabWidget()
        tabs.addTab(self.create_lecteur_tab(), "Lecteur")
        tabs.addTab(self.create_generateur_tab(), "Générateur")

        self.setCentralWidget(tabs)

    def create_lecteur_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        btn_importer = QPushButton("Importer le QR")
        btn_importer.clicked.connect(self.importer_qr)

        self.image_label = QLabel()
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)

        layout.addWidget(btn_importer)
        layout.addWidget(self.image_label)
        layout.addWidget(self.text_display)

        tab.setLayout(layout)
        return tab

    def create_generateur_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.text_input = QTextEdit()
        btn_generer = QPushButton("Générer QR")
        btn_generer.clicked.connect(self.generer_qr)

        self.qr_image_label = QLabel()
        self.enregistrer_btn = QPushButton("Enregistrer")
        self.enregistrer_btn.clicked.connect(self.enregistrer_image)
        self.copier_btn = QPushButton("Copier dans le presse-papiers")
        self.copier_btn.clicked.connect(self.copier_image)

        layout.addWidget(self.text_input)
        layout.addWidget(btn_generer)
        layout.addWidget(self.qr_image_label)
        layout.addWidget(self.enregistrer_btn)
        layout.addWidget(self.copier_btn)

        tab.setLayout(layout)
        return tab

    def importer_qr(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Importer une image", "", "Images (*.png *.jpg *.jpeg *.bmp)")

        if file_path:
            img = Image.open(file_path)
            result = decode(img)

            if result:
                self.image_label.setPixmap(QPixmap(file_path))
                self.text_display.setPlainText(result[0].data.decode('utf-8'))
            else:
                self.image_label.clear()
                self.text_display.setPlainText("Aucun code QR n'a été trouvé dans l'image.")

    def generer_qr(self):
        text = self.text_input.toPlainText()
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_path = "generated_qr.png"
        img.save(img_path)

        self.qr_image_label.setPixmap(QPixmap(img_path))

        self.img = img

    def copier_image(self):
        # Code pour rechercher l'image
        image_path = "generated_qr.png"  # Remplacez ceci par le chemin de votre image

        if image_path:
            image = QImage(image_path)
            pixmap = QPixmap.fromImage(image)

            # Copier l'image dans le presse-papiers
            clipboard = QGuiApplication.clipboard()
            clipboard.setPixmap(pixmap)

            messageBox = QMessageBox(self)
            messageBox.setText("L'image a été copiée dans le presse-papiers")
            messageBox.show()

            # Fermer la notification après deux secondes
            timer = QTimer()
            timer.timeout.connect(messageBox.close)
            timer.start(2000)

    def enregistrer_image(self):
        try:
            img = self.img
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, "Enregistrer l'image", "", "Images (*.png *.jpg *.jpeg *.bmp)")

            if file_path:
                # Code pour enregistrer l'image au chemin spécifié
                img.save(file_path)
                print("L'image a été enregistrée à l'emplacement :", file_path)

        except:
            pass

            

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
