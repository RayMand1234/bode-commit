from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtCore import Qt


class TitleLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('font-size: 38px; font-weight: bold;')


class SubtitleLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('font-size: 16px; color: #666; margin-bottom: 20px;')


class InputElement(QLineEdit):
    def __init__(self, placeholder):
        super().__init__()
        self.setPlaceholderText(placeholder)


class SubmitButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMaximumWidth(200)
        self.setStyleSheet('''
        background-color: 'green'
        ''')


class LogPanel(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet('font-family: monospace;')
        self.setMinimumHeight(200)
