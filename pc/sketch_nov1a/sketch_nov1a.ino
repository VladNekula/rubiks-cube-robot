#include <ESP32Servo.h>

Servo leftServo[2];   // [0] поворот, [1] зажим
Servo rightServo[2];  // [0] поворот, [1] зажим

const int leftPins[2]  = {17, 18};
const int rightPins[2] = {19, 21};

const int CENTER = 90;
const int TURN_CW = 180;
const int TURN_CCW = 0;

const int OPEN_ANGLE = 180;
const int CLOSE_ANGLE = 160;

int leftAngle[2]  = {CENTER, OPEN_ANGLE};
int rightAngle[2] = {CENTER, OPEN_ANGLE};

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < 2; i++) {
    leftServo[i].attach(leftPins[i]);
    rightServo[i].attach(rightPins[i]);
  }

  setLeft(0, CENTER);
  delay(300);
  setLeft(1, OPEN_ANGLE);
  delay(300);
  setRight(0, CENTER);
  delay(300);
  setRight(1, OPEN_ANGLE);
  delay(300);
}

void loop() {
  if (Serial.available() > 0) {
    String algorithm = Serial.readStringUntil('\n');
    algorithm.trim();

    if (algorithm.length() == 0) {
      return;
    }

    // Команда открытия клешней
    if (algorithm == "OPEN") {
      setLeft(1, OPEN_ANGLE);
      setRight(1, OPEN_ANGLE);
      delay(300);
      Serial.println("Клешни открыты.");
      return;
    }

    // Команда закрытия клешней
    if (algorithm == "CLOSE") {
      setLeft(1, CLOSE_ANGLE);
      setRight(1, CLOSE_ANGLE);
      delay(300);
      Serial.println("Клешни закрыты.");
      return;
    }

    Serial.print("Получен алгоритм: ");
    Serial.println(algorithm);

    for (int i = 0; i < algorithm.length(); i++) {
      char move = algorithm[i];

      if (move == ' ') {
        continue;
      }

      bool reverse = false;
      int repetitions = 1;

      if (i + 1 < algorithm.length()) {
        if (algorithm[i + 1] == '\'') {
          reverse = true;
          i++;
        } else if (algorithm[i + 1] == '2') {
            repetitions = 2;
            i++;
        }
      }

      for (int j = 0; j < repetitions; j++) {
        if (move == 'L') {
          turnLeft(reverse);
        } else if (move == 'F') {
          turnFront(reverse);
        } else if (move == 'R') {
          turnRight(reverse);
        } else if (move == 'B') {
          turnBack(reverse);
        } else if (move == 'U') {
          turnUp(reverse);
        } else if (move == 'D') {
          turnDown(reverse);
        }
      }

      delay(300);
    }

    Serial.println("Алгоритм обработан.");
  }
}

void setLeft(int number, int angle) {
  int minAngle = (number == 0) ? 0 : 160;
  leftAngle[number] = constrain(angle, minAngle, 180);
  leftServo[number].write(leftAngle[number]);
}

void setRight(int number, int angle) {
  int minAngle = (number == 0) ? 0 : 160;
  rightAngle[number] = constrain(angle, minAngle, 180);
  rightServo[number].write(rightAngle[number]);
}

void turn_CW_or_CCW_Left(bool CW) {
  int angle;

  if (CW) {
    angle = TURN_CW;
    setRight(1, OPEN_ANGLE);
    delay(300);
  } else {
    angle = TURN_CCW;
  }

  setLeft(0, angle);
  delay(300);
  setRight(1, CLOSE_ANGLE);
  delay(300);
  setLeft(1, OPEN_ANGLE);
  delay(300);
  setLeft(0, CENTER);
  delay(300);
  setLeft(1, CLOSE_ANGLE);
  delay(300);
}

void turn_CW_or_CCW_Right(bool CW) {
  int angle;

  if (CW) {
    angle = TURN_CW;
    setLeft(1, OPEN_ANGLE);
    delay(300);
  } else {
    angle = TURN_CCW;
  }

  setRight(0, angle);
  delay(300);
  setLeft(1, CLOSE_ANGLE);
  delay(300);
  setRight(1, OPEN_ANGLE);
  delay(300);
  setRight(0, CENTER);
  delay(300);
  setRight(1, CLOSE_ANGLE);
  delay(300);
}

void turn_and_return_Right(int turnAngle) {
  setRight(0, turnAngle);
  delay(300);
  setRight(1, OPEN_ANGLE);
  delay(300);
  setRight(0, CENTER);
  delay(300);
}

void turn_and_return_Left(int turnAngle) {
  setLeft(0, turnAngle);
  delay(300);
  setLeft(1, OPEN_ANGLE);
  delay(300);
  setLeft(0, CENTER);
  delay(300);
}

void turnLeft(bool reverse) {
  int turnAngle = reverse ? TURN_CCW : TURN_CW;
  turn_and_return_Left(turnAngle);
  setLeft(1, CLOSE_ANGLE);
  delay(300);
}

void turnDown(bool reverse) {
  int turnAngle = reverse ? TURN_CCW : TURN_CW;
  turn_and_return_Right(turnAngle);
  setRight(1, CLOSE_ANGLE);
  delay(300);
}

void turnFront(bool reverse) {
  int turnAngle = reverse ? TURN_CCW : TURN_CW;
  turn_CW_or_CCW_Left(true);
  turn_and_return_Right(turnAngle);
  turn_CW_or_CCW_Left(false);
}

void turnBack(bool reverse) {
  int turnAngle = reverse ? TURN_CCW : TURN_CW;
  turn_CW_or_CCW_Right(true);
  turn_and_return_Left(turnAngle);
  turn_CW_or_CCW_Right(false);
}

void turnUp(bool reverse) {
  int turnAngle = reverse ? TURN_CCW : TURN_CW;

  turn_CW_or_CCW_Left(true);
  turn_CW_or_CCW_Left(true);

  turn_and_return_Right(turnAngle);

  turn_CW_or_CCW_Left(false);
  setRight(1, OPEN_ANGLE);
  delay(300);
  turn_CW_or_CCW_Left(false);
}

void turnRight(bool reverse) {
  int turnAngle = reverse ? TURN_CCW : TURN_CW;

  turn_CW_or_CCW_Right(true);
  turn_CW_or_CCW_Right(true);

  turn_and_return_Left(turnAngle);

  turn_CW_or_CCW_Right(false);
  setLeft(1, OPEN_ANGLE);
  delay(300);
  turn_CW_or_CCW_Right(false);
}