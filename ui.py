from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy
)

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

class ColorSquare(QPushButton):
    """
    Один квадрат развертки кубика.
    При нажатии цвет переключается.
    """

    COLORS = [
        ("W", "#FFFFFF"),
        ("Y", "#FFFF00"),
        ("R", "#FF0000"),
        ("O", "#FF8800"),
        ("G", "#00AA00"),
        ("B", "#0066FF")
    ]

    def __init__(self, color="W"):
        super().__init__()

        self.setFixedSize(40, 40)

        self.index = 0

        for i, c in enumerate(self.COLORS):
            if c[0] == color:
                self.index = i

        self.update_color()

        self.clicked.connect(self.next_color)

    def update_color(self):

        letter, rgb = self.COLORS[self.index]

        self.letter = letter

        self.setStyleSheet(f"""
            QPushButton {{
                background-color:{rgb};
                border:1px solid black;
            }}
        """)

    def next_color(self):

        self.index += 1

        if self.index >= len(self.COLORS):
            self.index = 0

        self.update_color()

    def get_color(self):

        return self.letter

class FaceWidget(QWidget):
    """
    Одна грань кубика.
    """

    def __init__(self, center_color):

        super().__init__()

        layout = QGridLayout()

        layout.setSpacing(2)

        self.squares = []

        for i in range(3):

            row = []

            for j in range(3):

                square = ColorSquare(center_color)

                if i == 1 and j == 1:
                    square.setEnabled(False)

                layout.addWidget(square, i, j)

                row.append(square)

            self.squares.append(row)

        self.setLayout(layout)

    def get_face(self):

        result = []

        for row in self.squares:

            r = []

            for cell in row:

                r.append(cell.get_color())

            result.append(r)

        return result
class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Rubik Cube Solver")

        self.resize(1400, 800)

        self.seconds = 0

        central = QWidget()

        self.setCentralWidget(central)

        root = QHBoxLayout()

        central.setLayout(root)

        left = QVBoxLayout()

        root.addLayout(left, 3)

        self.timerLabel = QLabel("00:00")

        self.timerLabel.setAlignment(Qt.AlignCenter)

        self.timerLabel.setStyleSheet("""
            font-size:42px;
            font-weight:bold;
        """)

        left.addWidget(self.timerLabel)

        self.statusLabel = QLabel("Ожидание")

        self.statusLabel.setAlignment(Qt.AlignCenter)

        self.statusLabel.setStyleSheet("""
            font-size:20px;
        """)

        left.addWidget(self.statusLabel)

        cubeLayout = QGridLayout()

        cubeLayout.setSpacing(20)

        left.addLayout(cubeLayout)

        self.faceU = FaceWidget("W")
        self.faceL = FaceWidget("O")
        self.faceF = FaceWidget("G")
        self.faceR = FaceWidget("R")
        self.faceB = FaceWidget("B")
        self.faceD = FaceWidget("Y")

        cubeLayout.addWidget(self.faceU,0,1)

        cubeLayout.addWidget(self.faceL,1,0)

        cubeLayout.addWidget(self.faceF,1,1)

        cubeLayout.addWidget(self.faceR,1,2)

        cubeLayout.addWidget(self.faceB,1,3)

        cubeLayout.addWidget(self.faceD,2,1)

        buttons = QHBoxLayout()

        left.addLayout(buttons)

        self.scanButton = QPushButton("Scan")

        self.solveButton = QPushButton("Solve")

        self.scrambleButton = QPushButton("Scramble")

        self.resetButton = QPushButton("Reset")

        buttons.addWidget(self.scanButton)

        buttons.addWidget(self.solveButton)

        buttons.addWidget(self.scrambleButton)

        buttons.addWidget(self.resetButton)

        right = QVBoxLayout()

        root.addLayout(right,2)

        title = QLabel("Камера")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        right.addWidget(title)

        self.cameraLabel = QLabel()

        self.cameraLabel.setMinimumSize(640,480)

        self.cameraLabel.setAlignment(Qt.AlignCenter)

        self.cameraLabel.setStyleSheet("""
            border:2px solid gray;
            background:black;
            color:white;
            font-size:22px;
        """)

        self.cameraLabel.setText("Изображение камеры")

        right.addWidget(self.cameraLabel)

        self.moveLabel = QLabel("Следующий ход: -")

        self.moveLabel.setAlignment(Qt.AlignCenter)

        self.moveLabel.setStyleSheet("""
            font-size:28px;
        """)

        right.addWidget(self.moveLabel)

        self.timer = QTimer()

        self.timer.timeout.connect(self.updateTimer)

        self.scanButton.clicked.connect(self.scan)

        self.solveButton.clicked.connect(self.solve)

        self.scrambleButton.clicked.connect(self.scramble)

        self.resetButton.clicked.connect(self.resetCube)

    def updateTimer(self):

        self.seconds += 1

        minutes = self.seconds // 60

        seconds = self.seconds % 60

        self.timerLabel.setText(f"{minutes:02}:{seconds:02}")

    def scan(self):

        self.statusLabel.setText("Сканирование...")

        self.seconds = 0

        self.timer.start(1000)

    def solve(self):

        self.statusLabel.setText("Поиск решения...")

        cube = self.getCube()

    def scramble(self):

        self.statusLabel.setText("Перемешивание")

    def resetCube(self):

        self.seconds = 0

        self.timer.stop()

        self.timerLabel.setText("00:00")

        self.statusLabel.setText("Ожидание")

        self.moveLabel.setText("Следующий ход: -")

    def getCube(self):

        cube = {

            "U": self.faceU.get_face(),

            "R": self.faceR.get_face(),

            "F": self.faceF.get_face(),

            "D": self.faceD.get_face(),

            "L": self.faceL.get_face(),

            "B": self.faceB.get_face()

        }

        return cube

    def setCube(self, cube):

        mapping = {

            "U": self.faceU,

            "R": self.faceR,

            "F": self.faceF,

            "D": self.faceD,

            "L": self.faceL,

            "B": self.faceB

        }

        for face in mapping:

            widget = mapping[face]

            data = cube[face]

            for i in range(3):

                for j in range(3):

                    color = data[i][j]

                    square = widget.squares[i][j]

                    for index, info in enumerate(square.COLORS):

                        if info[0] == color:

                            square.index = index

                            square.update_color()

                            break
