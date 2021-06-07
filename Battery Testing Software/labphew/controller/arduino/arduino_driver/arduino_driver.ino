#include <DallasTemperature.h>
#include <OneWire.h>
#include <DHT.h>
#include <Servo.h>

#define ONE_WIRE_BUS 4
#define DHTPIN 6     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor for normal 16mhz Arduino
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DeviceAddress insideThermometer;
Servo servo;

bool isData;

String Comm = "";

float temp;
float hum_dht;
int temp_channel;
int output = DAC0;
int input;
int val;
String inData;
String tempValue;
String channel;
int sensorPin = A0;    // select the input pin for the potentiometer
int sensorValue;
int i = 0;
int Laser_LED = 49;
int Fiber_LED = 26;
int Power_LED = 30;
int Top_LED = 42;
int Servo_PIN = 13;
int Servo_ON = 1;
int Servo_OFF = 15;
int Measure_LED = 50;
byte rx_byte = 0;        // stores received byte

int piezo_delay = 25; // delay before stopping the movement of the piezo in milliseconds

void setup() {
  for (i = 2; i <= 13; i++) {
    pinMode(i, OUTPUT);
  }
  for (i = 22; i <= 53; i++) {
    pinMode(i, OUTPUT);
  }
  digitalWrite(Measure_LED, HIGH);
  digitalWrite(Power_LED, HIGH);
  digitalWrite(Laser_LED, HIGH);
  digitalWrite(Fiber_LED, LOW);
  digitalWrite(Top_LED, LOW);
  servo.attach(Servo_PIN);
  servo.write(Servo_OFF);

  // Load serial monitor
  Serial.begin(19200);
  Serial1.begin(19200);   // serial port 1
  Serial2.begin(19200);   // serial port 2
  analogWriteResolution(12);
  analogWrite(DAC0, 0);
  analogWrite(DAC1, 0);
  digitalWrite(Laser_LED, LOW);
  sensors.begin();
  dht.begin();
  sensors.getAddress(insideThermometer, 0);
  sensors.setResolution(insideThermometer, 11);
  for (i = 0; i < 5; i++) {
    digitalWrite(Power_LED, HIGH);
    delay(500);
    digitalWrite(Power_LED, LOW);
    delay(500);
  }
  digitalWrite(Power_LED, HIGH);

  while (!Serial);
  Serial.flush();
  Serial1.flush();
  Serial2.flush();
  digitalWrite(Measure_LED, LOW);
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
    if (Comm.startsWith("LED")) {
      int val = Comm.substring(4, 5).toInt();
      int mode = Comm.substring(6, 7).toInt();

      switch (val) {
        case 0:
          digitalWrite(Fiber_LED, mode);
          break;
        case 1:
          digitalWrite(Measure_LED, mode);
          break;
        case 2:
          digitalWrite(Laser_LED, mode);
          break;
        case 3:
          digitalWrite(Power_LED, mode);
          break;
        case 4:
          digitalWrite(Top_LED, mode);
          break;
      }
      Serial.println("LED changed");
    }
    else if (Comm.startsWith("serv")) {
      int val = Comm.substring(5, 6).toInt();
      if (val == 1) {
        servo.write(Servo_ON);
        Serial.println("Servo ON");
      } else {
        servo.write(Servo_OFF);
        Serial.println("Servo OFF");
      }

    }
    else if (Comm.startsWith("mot1")) {
      Serial.println("Waiting for input mot 1");
      while (Serial.available() <= 0) {
        delay(1);
      }
      rx_byte = Serial.read();
      Serial1.write(rx_byte);

      bool is_step = true;
      for (int bits = 5; bits > 0; bits--) {
        if (rx_byte & (1 << bits)) {
          is_step = false;
        }
      }
      if (!(rx_byte & (1 << 0))) {
        is_step = false;
      }
      if (!(rx_byte & (1 << 7)) && is_step) {
        delay(piezo_delay / 2);
        Serial1.write(rx_byte);
        printOut1(rx_byte);
      }
      if (!is_step) {
        delay(piezo_delay);
        rx_byte = 0;
        Serial1.write(rx_byte);
      }
      Serial.println("OK");
    }
    else if (Comm.startsWith("mot2")) {
      Serial.println("Waiting for input mot 2");
      while (Serial.available() <= 0) {
        delay(1);
      }
      rx_byte = Serial.read();
      Serial2.write(rx_byte);
      bool is_step = true;
      for (int bits = 5; bits > 0; bits--) {
        if (rx_byte & (1 << bits)) {
          is_step = false;
        }
      }
      if (!(rx_byte & (1 << 0))) {
        is_step = false;
      }
      if (!(rx_byte & (1 << 7)) && is_step) {
        delay(piezo_delay / 2);
        Serial2.write(rx_byte);
        printOut1(rx_byte);
      }
      if (!is_step) {
        delay(piezo_delay);
        rx_byte = 0;
        Serial2.write(rx_byte);
      }
      Serial.println("OK");
    }
    else if (Comm.startsWith("OUT")) {
      for (i = 4; i <= Comm.length(); i++) {
        tempValue += Comm[i];
      }
      val = tempValue.toInt();
      tempValue = "";
      analogWrite(DAC0, val);
      Serial.println(val);
    }
    else if (Comm.startsWith("TEM")) { // Read the temp
      temp_channel = Comm.substring(4, 5).toInt();
      if (temp_channel == 0) {
        temp = dht.readTemperature();
        Serial.println(temp);
      } else if (temp_channel == 1) {
        sensors.requestTemperatures(); // Send the command to get temperature readings
        delay(100);
        temp = sensors.getTempCByIndex(0);
        Serial.println(temp);
      }
    }
    else if (Comm.startsWith("HUM")) {
      float humidity = dht.readHumidity();
      Serial.println(humidity);
    }
    else if (Comm.startsWith("IDN")) {
      Serial.println("Dispertech device 1.0");
    }
    delay(1);
    Comm = "";
  }
  delay(2);
}

void printOut1(int c) {
  for (int bits = 7; bits > -1; bits--) {
    // Compare bits 7-0 in byte
    if (c & (1 << bits)) {
      Serial.print ("1");
    }
    else {
      Serial.print ("0");
    }
  }
}
