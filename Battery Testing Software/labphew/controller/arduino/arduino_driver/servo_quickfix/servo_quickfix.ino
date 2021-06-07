#include <Servo.h>
String Comm = "";
bool isData;

Servo servo;

void setup() {
  Serial.begin(19200);
  servo.attach(13);
  servo.write(15);
  while (!Serial);
}

void loop() {
  while (Serial.available() > 0 ) {
    char value = Serial.read();
    Comm += value;
    if (value == '\n') {
      isData = true;
    }
  }
  if (isData) {
    isData = false;
    if (Comm.startsWith("ON")) {
      servo.write(1);
      Serial.println("ON");
    } else {
      servo.write(10);
      Serial.println("OFF");
    }
    Comm = "";
    delay(5);
  }
}
