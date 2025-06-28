import os
import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import ReviewCommitsGUI
from PyQt6.QtGui import QFontDatabase, QFont

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set heebo font
    path = os.path.join(os.path.dirname(__file__), './gui/fonts/Heebo-Bold.ttf')
    font_id = QFontDatabase.addApplicationFont(path)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

    app.setFont(QFont(font_family))
    gui = ReviewCommitsGUI()
    gui.show()
    sys.exit(app.exec())
