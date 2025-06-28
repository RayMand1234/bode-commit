import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import ReviewCommitsGUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ReviewCommitsGUI()
    gui.show()
    sys.exit(app.exec()) 