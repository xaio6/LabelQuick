import sys
from PyQt5.QtWidgets import QApplication

from GUI.main import (MainFunc)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainFunc()
    main.show()
    sys.exit(app.exec_())