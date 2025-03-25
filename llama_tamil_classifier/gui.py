import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QCheckBox
)
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Qt
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from llama_tamil_classifier.model import LlamaClassifier  

class LlamaClassifierApp(QWidget):
    def __init__(self):
        super().__init__()
        self.transliteration_enabled = True  
        self.classifier = LlamaClassifier()  
        self.initUI()

    def initUI(self):
        self.setWindowTitle("LLaMA Tamil Classifier")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)

        layout = QVBoxLayout()

        self.label = QLabel("Enter Tamil or Tanglish (Press SPACE to convert):")
        layout.addWidget(self.label)

        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Type here...")
        self.text_box.setMinimumHeight(100)  
        self.text_box.textChanged.connect(self.transliterate_on_space)
        layout.addWidget(self.text_box)

        button_layout = QHBoxLayout()

        # ✅ Transliteration Checkbox
        self.translit_checkbox = QCheckBox("Enable transliteration (English to Tamil)")
        self.translit_checkbox.setChecked(True)
        self.translit_checkbox.stateChanged.connect(self.toggle_transliteration)
        button_layout.addWidget(self.translit_checkbox)

        self.classify_button = QPushButton("Classify")
        self.classify_button.clicked.connect(self.classify_text)
        button_layout.addWidget(self.classify_button)

        layout.addLayout(button_layout)

        self.result_label = QLabel("Prediction:")
        layout.addWidget(self.result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(120)  
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def toggle_transliteration(self):
        """Enable or disable transliteration based on checkbox state."""
        self.transliteration_enabled = self.translit_checkbox.isChecked()

    def transliterate_on_space(self):
        if not self.transliteration_enabled:
            return

        text = self.text_box.toPlainText()
        if text.endswith(" "):
            words = text.split()
            if words:
                last_word = words[-1]
                transliterated_word = transliterate(last_word, sanscript.ITRANS, sanscript.TAMIL)
                words[-1] = transliterated_word
                updated_text = " ".join(words) + " "

                self.text_box.blockSignals(True)
                self.text_box.setPlainText(updated_text)
                self.text_box.moveCursor(QTextCursor.End)
                self.text_box.blockSignals(False)

    def classify_text(self):
        user_input = self.text_box.toPlainText().strip()
        if user_input:
            prediction = self.classifier.classify(user_input)
            self.result_text.setPlainText(prediction)

def main():
    app = QApplication(sys.argv)
    window = LlamaClassifierApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
