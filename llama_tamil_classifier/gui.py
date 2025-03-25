import sys
import os
# Allow relative imports when running as a script
from llama_tamil_classifier.model import LlamaClassifier  # Package execution
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout
)
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Qt
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from .model import LlamaClassifier  # Import your LLaMA Tamil classifier

class LlamaClassifierApp(QWidget):
    def __init__(self):
        super().__init__()
        self.transliteration_enabled = True  # Toggle for transliteration
        self.classifier = LlamaClassifier()  # Load classifier model
        self.initUI()

    def initUI(self):
        self.setWindowTitle("LLaMA Tamil Classifier")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)

        layout = QVBoxLayout()

        self.label = QLabel("Enter Tamil or Tanglish (Press SPACE to convert):")
        layout.addWidget(self.label)

        # **Text Box**
        self.text_box = QTextEdit()
        self.text_box.textChanged.connect(self.transliterate_on_space)
        layout.addWidget(self.text_box)

        # **Controls: Toggle Transliteration + Classify**
        button_layout = QHBoxLayout()

        self.translit_button = QPushButton("Disable Transliteration")
        self.translit_button.clicked.connect(self.toggle_transliteration)
        button_layout.addWidget(self.translit_button)

        self.classify_button = QPushButton("Classify")
        self.classify_button.clicked.connect(self.classify_text)
        button_layout.addWidget(self.classify_button)

        layout.addLayout(button_layout)

        self.result_label = QLabel("Prediction: ")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def toggle_transliteration(self):
        """Enable/Disable Transliteration."""
        self.transliteration_enabled = not self.transliteration_enabled
        self.translit_button.setText(
            "Enable Transliteration" if not self.transliteration_enabled else "Disable Transliteration"
        )

    def transliterate_on_space(self):
        """Transliterate last word after pressing space, if enabled."""
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
        """Run LLaMA classification."""
        user_input = self.text_box.toPlainText().strip()
        if user_input:
            prediction = self.classifier.classify(user_input)
            self.result_label.setText(f"Prediction: {prediction}")

def main():
    app = QApplication(sys.argv)
    window = LlamaClassifierApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()