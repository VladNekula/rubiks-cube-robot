from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
)

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

from scan import scan_cube
from solv import solve_cube

import random

class ColorSquare(QPushButton):

    COLORS = [
        ("W", "#FFFFFF"),
        ("Y", "#FFFF00"),
        ("R", "#FF0000"),
        ("O", "#FF8800"),
        ("G", "#00AA00"),
        ("B", "#0066FF")
    ]

    def __init__(self, color="W", size=50):
        super().__init__()

        self.setFixedSize(size, size)

        self.setStyleSheet("""
            QPushButton {
                border: 1px solid black;
                margin: 0px;
                padding: 0px;}
        """)

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
                background-color: {rgb};
                border: 1px solid black;
                margin: 0px;
                padding: 0px;
            }}
        """)

    def next_color(self):
        self.index = (self.index + 1) % len(self.COLORS)
        self.update_color()

    def get_color(self):
        return self.letter

class FaceWidget(QWidget):
    def __init__(self, center_color, square_size=50, spacing=4):
        super().__init__()

        self.square_size = square_size
        self.spacing = spacing
        total_size = square_size * 3 + spacing * 2
        self.setFixedSize(total_size, total_size)

        layout = QGridLayout()
        layout.setSpacing(spacing)
        layout.setHorizontalSpacing(spacing)
        layout.setVerticalSpacing(spacing)
        layout.setContentsMargins(0, 0, 0, 0)

        self.squares = []

        for i in range(3):
            row = []
            for j in range(3):
                square = ColorSquare(center_color, square_size)
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
        left.setContentsMargins(20, 20, 20, 20)
        left.setSpacing(15)
        root.addLayout(left, 1)

        self.timerLabel = QLabel("00:00")
        self.timerLabel.setAlignment(Qt.AlignCenter)
        self.timerLabel.setStyleSheet("""
            font-size:52px;
            font-weight:bold;
        """)
        left.addWidget(self.timerLabel)

        self.statusLabel = QLabel("Ожидание")
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.statusLabel.setStyleSheet("""
            font-size:20px;
        """)
        left.addWidget(self.statusLabel)

        SQUARE_SIZE = 50
        SPACING = 4
        FACE_SPACING = 6
        face_size = SQUARE_SIZE * 3 + SPACING * 2
        cubeContainer = QWidget()

        total_width = face_size * 4 + FACE_SPACING * 3
        total_height = face_size * 3 + FACE_SPACING * 2
        cubeContainer.setFixedSize(total_width, total_height)

        cubeLayout = QGridLayout()
        cubeLayout.setSpacing(FACE_SPACING)
        cubeLayout.setHorizontalSpacing(FACE_SPACING)
        cubeLayout.setVerticalSpacing(FACE_SPACING)
        cubeLayout.setContentsMargins(0, 0, 0, 0)
        cubeContainer.setLayout(cubeLayout)

        self.faceU = FaceWidget("W", SQUARE_SIZE, SPACING)
        self.faceL = FaceWidget("O", SQUARE_SIZE, SPACING)
        self.faceF = FaceWidget("G", SQUARE_SIZE, SPACING)
        self.faceR = FaceWidget("R", SQUARE_SIZE, SPACING)
        self.faceB = FaceWidget("B", SQUARE_SIZE, SPACING)
        self.faceD = FaceWidget("Y", SQUARE_SIZE, SPACING)

        cubeLayout.addWidget(self.faceU, 0, 1)
        cubeLayout.addWidget(self.faceL, 1, 0)
        cubeLayout.addWidget(self.faceF, 1, 1)
        cubeLayout.addWidget(self.faceR, 1, 2)
        cubeLayout.addWidget(self.faceB, 1, 3)
        cubeLayout.addWidget(self.faceD, 2, 1)

        left.addWidget(cubeContainer, alignment=Qt.AlignCenter)

        buttons = QHBoxLayout()
        left.addLayout(buttons)

        self.scanButton = QPushButton("Scan")
        self.solveButton = QPushButton("Solve")
        self.scrambleButton = QPushButton("Scramble")
        self.resetButton = QPushButton("Reset")

        buttonsList = [self.scanButton, self.solveButton,
                       self.scrambleButton, self.resetButton]

        for button in buttonsList:
            button.setMinimumHeight(45)
            button.setMinimumWidth(140)
            button.setStyleSheet("""
                QPushButton{
                    font-size:18px;
                }
            """)

        buttons.addWidget(self.scanButton)
        buttons.addWidget(self.solveButton)
        buttons.addWidget(self.scrambleButton)
        buttons.addWidget(self.resetButton)

        right = QVBoxLayout()
        right.setContentsMargins(20, 20, 20, 20)
        right.setSpacing(15)

        root.addLayout(right, 1)

        self.scrambleLabel = QLabel("Scramble:")
        self.scrambleLabel.setStyleSheet("font-size:20px;")
        right.addWidget(self.scrambleLabel)

        self.moveLabel = QLabel("-")
        self.moveLabel.setAlignment(Qt.AlignCenter)
        self.moveLabel.setStyleSheet("""
            font-size:22px;
            padding:10px;
            background-color: transparent;
            border: none;
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
        cube = scan_cube()

        if cube is not None:
            cube["U"][1][1] = "W"
            cube["R"][1][1] = "R"
            cube["F"][1][1] = "G"
            cube["D"][1][1] = "Y"
            cube["L"][1][1] = "O"
            cube["B"][1][1] = "B"

            self.setCube(cube)
            self.statusLabel.setText("Сканирование завершено")
        else:
            self.statusLabel.setText("Сканирование отменено")

    def solve(self):
        self.statusLabel.setText("Решение...")
        self.seconds = 0
        self.timerLabel.setText("00:00")
        self.timer.start(1000)
        cube = self.getCube()

        solution = solve_cube(cube)
        self.moveLabel.setText(solution)
        self.statusLabel.setText("Готово")

    def scramble(self):
        moves = ["R", "L", "U", "D", "F", "B",
                "R'", "L'", "U'", "D'", "F'", "B'"]
        sequence = []
        last = ""

        for _ in range(25):
            move = random.choice(moves)
            while move[0] == last:
                move = random.choice(moves)
            sequence.append(move)
            last = move[0]
        result = " ".join(sequence)

        self.scrambleLabel.setText("Scramble: " + result)
        self.statusLabel.setText("Scramble готов")

    def resetCube(self):
        self.seconds = 0
        self.timer.stop()
        self.timerLabel.setText("00:00")
        self.statusLabel.setText("Ожидание")
        self.moveLabel.setText("-")

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
