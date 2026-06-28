import sys

from PyQt5.QtWidgets import QApplication

from ui import MainWindow

def main():
    """
    Точка входа в программу.
    """

    app = QApplication(sys.argv)

    app.setApplicationName("Rubik Cube Solver")

    window = MainWindow()

    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
