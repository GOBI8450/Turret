#include <Servo.h>

// Servos:
Servo x, y, shoot;  // Declare the shoot servo
int width = 640, height = 480;  // total resolution of the video
int targetX = width / 2, targetY = height / 2;  // target positions

// For precise speed PID:
double Kp = 0.04, Ki = 0.015, Kd = 0.01;
int prevErrorX = 0, prevErrorY = 0;
int integralX = 0, integralY = 0;

// Ultrasonic:
// const int trigPin = 13;
// const int echoPin = 12;
// long duration;
// int distance;

void setup() {
  Serial.begin(9600);
  // pinMode(trigPin, OUTPUT);
  // pinMode(echoPin, INPUT);
  x.attach(11);
  y.attach(10);
  shoot.attach(9);  // Attach the shoot servo to pin 9
  x.write(90);  // Start at 90 position for X axis
  y.write(90);  // Start at 90 position for Y axis
}

void loop() {
  char receivedChar;
  if (Serial.available() > 0) {
    receivedChar = Serial.read();

    // Ultrasonic sensor measurements
    //digitalWrite(trigPin, LOW);
    // delayMicroseconds(2);
    // digitalWrite(trigPin, HIGH);
    // delayMicroseconds(2);
    // digitalWrite(trigPin, LOW);
    // duration = pulseIn(echoPin, HIGH);
    // distance = (duration * 0.0343) / 2;\
    // Serial.print("Distance: ");
    // Serial.println(distance);

    if (receivedChar == 'X') {
      delay(10);
      int x_mid = Serial.parseInt();
      Serial.print("Received X: ");
      Serial.println(x_mid);

      if (Serial.read() == 'Y') {
        delay(10);
        int y_mid = Serial.parseInt();
        Serial.print("Received Y: ");
        Serial.println(y_mid);

        int errorX = targetX - x_mid;
        int errorY = targetY - y_mid;

        integralX += errorX;
        integralY += errorY;

        int derivativeX = errorX - prevErrorX;
        int derivativeY = errorY - prevErrorY;

        int outputX = Kp * errorX + Ki * integralX + Kd * derivativeX;
        int outputY = Kp * errorY + Ki * integralY + Kd * derivativeY;

        x.write(90 - outputX);  // 90° is the center position
        y.write(90 - outputY);  // 90° is the center position

        prevErrorX = errorX;
        prevErrorY = errorY;
      }
    }

    if (receivedChar == 'S') {
      shoot.write(360);
      delay(200);
      shoot.write(90);
      delay(100);
    }
  }
}

